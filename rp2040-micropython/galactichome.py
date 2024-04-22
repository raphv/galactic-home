import uasyncio
import json
import machine
import time
import network
import gc
import sys
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
from wave_player import WavePlayer

import gh_config as CONFIG
from gh_visual_assets import DIGITS, BASE_COLORS, HTML_HOME

graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()
graphics.set_font('bitmap8')

PENS = [ graphics.create_pen(*color) for color in BASE_COLORS ]
BLACK  = PENS[0]
WHITE  = PENS[15]
ICON_WIDTH = 9
ICON_HEIGHT = gu.HEIGHT

ICON_LEFT = 18
TEXT_LEFT_WITH_ICON = 28
TEXT_LEFT_WITHOUT_ICON = 18

isconnected = False
last_time_update = 0
tz_offset = 0
text_to_display = None
ringing = False
all_lines = []
error_log = []

def exception_to_message(exc):
    return '%s: %s'%(exc.__class__.__name__, exc)

def log_error(*messages):
    year, month, day, hour, minute,second, _, _ = time.localtime(time.time() + tz_offset)
    full_message = ' '.join(messages)
    if len(error_log) > 15:
        del error_log[0]
    error_log.append('[%04d-%02d-%02d %02d:%02d:%02d] %s'%(year, month, day, hour, minute,second,full_message))
    print(full_message)

@micropython.native
def draw_digit(i, offset_x, offset_y):
    digit = DIGITS[i]
    for y in range(5):
        ypos = offset_y + y
        if (ypos >= 0) or (ypos < HEIGHT):
            line = (digit >> y*3) & 7
            for x in range(3):
                xpos = offset_x + x
                if line & 1:
                    graphics.pixel(xpos, ypos)
                line = (line >> 1)
    
@micropython.native
def draw_icon(icon, offset_x, offset_y):
    for y in range(ICON_HEIGHT):
        ypos = offset_y + y
        for x in range(ICON_WIDTH):
            xpos = offset_x + x
            pixelvalue = int(icon[ICON_WIDTH * y + x],16)
            if pixelvalue:
                graphics.set_pen(PENS[pixelvalue])
                graphics.pixel(xpos, ypos)

def is_available(state):
    text = state.get('text', None)
    if not text:
        return False
    return not state.get('hidden', False)

def make_response(content_type, content, status='200 OK'):
    return '\r\n'.join([
        'HTTP/1.0 %s'%status,
        'Connection: close',
        'Content-Type: %s'%content_type,
        '', '',
        content
    ]).encode()

def build_status_json():
    local_now = time.time() + tz_offset
    year, month, day, hour, minute,second, _, _ = time.localtime(local_now)
    return json.dumps({
        'time': '%02d/%02d/%04d %02d:%02d:%02d'%(day, month, year, hour, minute, second),
        'data': all_lines
    })

async def server_callback(reader, writer):
    global ringing
    request_info = ''
    try:
        request = await reader.read(1024)
        request_info = request.decode().split('\r\n')[0].split(' ')
        print(request_info)
        path = request_info[1] if len(request_info) > 1 else ''
        if path == '/':
            response = make_response(
                'text/html',
                HTML_HOME
            )
        elif path == '/data':
            response = make_response(
                'application/json',
                build_status_json()
            )
        elif path == '/ring':
            response = make_response(
                'text/plain',
                'Ding dong.'
            )
            ringing = True
        elif path == '/errors':
            response = make_response(
                'text/plain',
                '\r\n'.join(error_log)
            )
        else:
            response = make_response(
                'text/plain',
                'Not found.',
                '404 Not Found'
            )
        writer.write(response)
        await writer.drain()
    except Exception as e:
        log_error(
            "[Web server] Error while responding to request",
            ' '.join(request_info),
            exception_to_message(e)
        )
    finally:
        writer.close()
        reader.close()
        await writer.wait_closed()
        await reader.wait_closed()
        
async def connect_loop():
    print('Starting Connect Loop')
    global isconnected
    while True:
        sta = network.WLAN(network.STA_IF)
        isconnected = sta.isconnected()
        if not isconnected:
            log_error("Disconnected")
            sta.active(True)
            sta.connect(CONFIG.SSID,CONFIG.PSK)
            while not isconnected:
                isconnected = sta.isconnected()
                await uasyncio.sleep_ms(1_000)
            log_error("Connected",sta.ifconfig()[0])
        await uasyncio.sleep_ms(60_000)

async def get_time():
    global tz_offset, last_time_update
    try:
        print('Retrieving time from http://%s%s'%(CONFIG.TIME_SERVER,CONFIG.TIME_PATH))
        reader, writer = await uasyncio.open_connection(
            CONFIG.TIME_SERVER,
            80,
        )
        headlines = [
            'GET %s HTTP/1.0'%CONFIG.TIME_PATH,
            '', ''
        ]
        writer.write("\r\n".join(headlines).encode())
        await writer.drain()
        resp = await reader.read()
        json_data = resp.decode().split('\r\n')[-1]
        time_data = json.loads(json_data)
        tz_offset = time_data.get("raw_offset",0) + time_data.get("dst_offset",0)
        utc_str = time_data["utc_datetime"]
        time_tuple = tuple(
            int(utc_str[a:b])
            for (a, b) in (
                (0,4),(5,7),(8,10), (1,2), # Year, Month, Day, Fake Weekday
                (11,13),(14,16),(17,19), (1,2), # Hour, Minute, Second, Fake Subsecond
                )
            )
        machine.RTC().datetime(time_tuple)
        last_time_update = time.ticks_ms()
        print('UTC time is %s'%(utc_str[:19]))
    except Exception as e:
        log_error(
            "[Get Time] Error", exception_to_message(e)
        )
    finally:
        reader.close()
        writer.close()
        await reader.wait_closed()
        await writer.wait_closed()

async def time_update_loop():
    print('Starting Time Update Loop')
    while True:
        while not isconnected:
            await uasyncio.sleep_ms(500)
        if last_time_update:
            freshness = time.ticks_diff(
                time.ticks_ms(),
                last_time_update
            )
        else:
            freshness = 20_000_000
        if (freshness > 18_000_000):
            await get_time()
        await uasyncio.sleep_ms(20_000)

async def get_ha_data():
    global all_lines
    try:
        reader, writer = await uasyncio.open_connection(
            CONFIG.HA_HOSTNAME,
            CONFIG.HA_PORT,
        )
        headlines = [
            'GET /api/states/%s HTTP/1.0'%CONFIG.HA_ENTITY,
            'Authorization: Bearer %s'%CONFIG.HA_TOKEN,
            '', ''
        ]
        writer.write("\r\n".join(headlines).encode())
        await writer.drain()
        resp = await reader.read()
        json_data = json.loads(resp.decode().split('\r\n')[-1])
        all_lines = json_data['attributes']['display'] or []
        if not all_lines:
            log_error("Home Assistant returned empty data")
        print('Updated ', json_data['state'])
    except Exception as e:
        log_error(
            "[Home Assistant] Error while fetching data",
            exception_to_message(e)
        )
    finally:
        reader.close()
        writer.close()
        await reader.wait_closed()
        await writer.wait_closed()


async def ha_update_loop():
    print('Start HA update loop')
    while True:
        while not isconnected:
            await uasyncio.sleep_ms(500)
        await get_ha_data()
        await uasyncio.sleep_ms(CONFIG.HA_REFRESH_TIME)

async def text_loop():
    print('Starting text loop')
    global text_to_display
    current_line_index = -1
    while True:
        try:
            visible_lines = [s for s in all_lines if s.get('visible',True)]
            display_time = CONFIG.LINE_DISPLAY_TIME
            if visible_lines:
                current_line_index = (1 + current_line_index) % len(visible_lines)
                current_line = visible_lines[current_line_index]
                text = current_line.get('text', '')
                text_width = graphics.measure_text(text, scale = .5)
                display_time = max(display_time, int(1.1 * text_width * CONFIG.GRAPHICS_REFRESH_TIME) )
                text_to_display = [
                    text, # 0 = text
                    text_width, # 1 = full width
                    0, # 2 = current scroll
                    -1, # 3 = scroll direction
                    5, # 4 = countdown
                    current_line.get('icon',None), # 5 = icon
                ]
                print("Showing '%s' for %.2fs"%(text,display_time/1000))
            else:
                text_to_display = None
                display_time = 500
            del visible_lines
        except Exception as e:
            log_error(
                "[Text processing loop]",
                exception_to_message(e)
                )    
        await uasyncio.sleep_ms(display_time)
        
async def display_loop():
    while True:
        local_now = time.time() + tz_offset
        _, month, day, hour, minute, _, weekday, _ = time.localtime(local_now)
        parity = (time.ticks_ms()//500)&1
        
        graphics.set_pen(BLACK)
        graphics.clear()
        
        if text_to_display:
            text_left = TEXT_LEFT_WITHOUT_ICON
            if text_to_display[5]:
                text_left = TEXT_LEFT_WITH_ICON
            text_width = gu.WIDTH - text_left   
            graphics.set_pen(WHITE)
            graphics.text(text_to_display[0], text_left + text_to_display[2], 2, scale = .5)
            if text_to_display[1] > (2+text_width):
                #only scroll if text is bigger than screen + 2 pixel tolerance
                if text_to_display[4]:
                    #if in countdown mode, do nothing
                    text_to_display[4] -= 1
                else:
                    if text_to_display[3] == -1 and text_to_display[2] < (text_width - text_to_display[1] + 1):
                        # if moving left and reaching the end of the screen, change direction and reset countdown
                        text_to_display[3] = 1
                        text_to_display[4] = 5
                    elif text_to_display[3] == 1 and text_to_display[2] >= 0:
                        # if moving right and reaching the end of the screen too
                        text_to_display[3] = -1
                        text_to_display[4] = 5
                    else:
                        text_to_display[2] += text_to_display[3]
            graphics.set_pen(BLACK)
            graphics.rectangle(0, 0, text_left, 11)
            if text_to_display[5]:
                draw_icon(text_to_display[5], ICON_LEFT, 0)
                
        graphics.set_pen(PENS[9])
        draw_digit(day//10,0,0)
        draw_digit(day%10,4,0)
        draw_digit(month//10,10,0)
        draw_digit(month%10,14,0)
        graphics.set_pen(PENS[10])
        draw_digit(hour//10,0,6)
        draw_digit(hour%10,4,6)
        draw_digit(minute//10,10,6)
        draw_digit(minute%10,14,6)
        graphics.set_pen(WHITE)
        if parity:
            graphics.pixel(8,7)
            graphics.pixel(8,9)
        gu.update(graphics)
        await uasyncio.sleep_ms(CONFIG.GRAPHICS_REFRESH_TIME)

async def sound_loop():
    print('Starting sound loop')
    global ringing
    wp = WavePlayer(gu)
    last_hour = -1
    while True:
        if ringing:
            ringing = False
            gc.collect()
            wp.play(CONFIG.RINGTONE, loop=CONFIG.SONG_LOOP_COUNT, freq=CONFIG.WAV_FREQ)
        else:
            local_now = time.time() + tz_offset
            _, _, _, hour, minute, _, weekday, _ = time.localtime(local_now)
            if hour != last_hour and minute == 0:
                last_hour = hour
                track = CONFIG.WEEK_SOUNDS[weekday][hour]
                if (track): #But not at night
                    gc.collect()
                    wp.play('%s'%track, loop=CONFIG.SONG_LOOP_COUNT, freq=CONFIG.WAV_FREQ)
        await uasyncio.sleep_ms(500)

async def display_brightness_loop():
    while True:
        gu.set_brightness(max(.15,min(1.,gu.light()/600)))
        await uasyncio.sleep_ms(500)

async def main():
    await uasyncio.start_server(
            server_callback,
            '0.0.0.0',
            CONFIG.LISTEN_PORT
        )
    uasyncio.create_task(connect_loop())
    uasyncio.create_task(time_update_loop())
    uasyncio.create_task(ha_update_loop())
    uasyncio.create_task(text_loop())
    uasyncio.create_task(display_loop())
    uasyncio.create_task(sound_loop())
    await uasyncio.create_task(display_brightness_loop())

log_error("Starting up", sys.version)
uasyncio.run(main())
