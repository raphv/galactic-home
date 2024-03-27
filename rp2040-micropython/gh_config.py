#WIFI CONFIG

SSID = "WiFi-SSID"
PSK = "WiFi-Password"

HA_HOSTNAME = '192.168.1.200'
HA_PORT = 8123
HA_TOKEN = ""
# Check https://www.home-assistant.io/docs/authentication/#your-account-profile to get a token

HA_ENTITY = 'sensor.galactic_home'

LISTEN_PORT = 80

TZ = "Europe/Amsterdam"
TIME_SERVER = "worldtimeapi.org"
TIME_PATH = "/api/timezone/%s"%TZ

WEEKDAY_SOUNDS = (
    None, None, None, None, None, None, None, # 0, 1, 2, 3, 4, 5, 6am
    'clock/07.wav', 'clock/08.wav',
    'clock/09.wav', 'clock/10.wav', 'clock/11.wav', 'clock/noon.wav',
    'clock/01.wav', 'clock/02.wav', 'clock/03.wav', 'clock/04.wav',
    'clock/05.wav', 'clock/06.wav', 'clock/07.wav', 'clock/08.wav',
    None, None, None, # 9, 10, 11pm
    )

WEEKEND_SOUNDS = (
    None, None, None, None, None, None, None, None, None, # 0, 1, 2, 3, 4, 5, 6, 7, 8am
    'clock/09.wav', 'clock/10.wav', 'clock/11.wav', 'clock/noon.wav',
    'clock/01.wav', 'clock/02.wav', 'clock/03.wav', 'clock/04.wav',
    'clock/05.wav', 'clock/06.wav', 'clock/07.wav', 'clock/08.wav',
    None, None, None, # 9, 10, 11pm
    )

WEEK_SOUNDS = [ WEEKDAY_SOUNDS, ] * 5 + [ WEEKEND_SOUNDS, ] * 2
RINGTONE = 'bell.wav'
SONG_LOOP_COUNT = 2
WAV_FREQ = 8

GRAPHICS_REFRESH_TIME = 100
LINE_DISPLAY_TIME = 5_500
HA_REFRESH_TIME = 30_000
