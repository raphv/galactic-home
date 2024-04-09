const DIGITS = [
    0o35556, 0o72232, //0,1
    0o71243, 0o34347, //2,3
    0o44755, 0o34717, //4,5
    0o35716, 0o11247, //6,7
    0o35256, 0o34756, //8,9
];
const SVG_SCALE = 10,
    UNICORN_WIDTH = 53,
    UNICORN_HEIGHT = 11,
    textinput = document.getElementById('display-text');

const grid_data = Array.from(Array(UNICORN_HEIGHT)).map(x => Array.from(Array(UNICORN_WIDTH)).map(y => 0)),
    svg_header = `<svg xmlns="http://www.w3.org/2000/svg" width="${(1+UNICORN_WIDTH)*SVG_SCALE}" height="${(1+UNICORN_HEIGHT)*SVG_SCALE}" viewBox="-.5 -.5 ${1+UNICORN_WIDTH} ${1+UNICORN_HEIGHT}">
    ${PIXEL_DEF}
    <rect x="-.5" y="-.5" width="${1+UNICORN_WIDTH}" height="${1+UNICORN_HEIGHT}" fill="#202020" />`,
    svg_footer = '</svg>';

function makeUnicornSvg() {
    return svg_header
        + grid_data.map((line, y) => {
            return line.map( (colour_code, x) => {
                    return `<use href="#sc" transform="translate(${x} ${y})" fill="${BASE_COLOURS[colour_code]}" />`;
                }).join('');
        }).join('')
        + '</svg>';
}

function getImageUrl() { // based on https://github.com/heyallan/svg-to-data-uri/
    let svg = makeUnicornSvg().replace(/>\s+</g, '><').replace(/[%#<>?\[\\\]^`{|}]/g, encodeURIComponent);
    return `data:image/svg+xml,${svg}`;
}

function setPixel(x, y, colour_code = 0xf) {
    if (x >= 0 && x < UNICORN_WIDTH && y >= 0 && y < UNICORN_HEIGHT) {
        grid_data[y][x] = colour_code;
    }
}

function rect(left, top, width, height, colour_code = 0xf) {
    for (let x = Math.max(0,left), right = Math.min(UNICORN_WIDTH, left + width); x < right; x++) {
        for (let y = Math.max(0, top), bottom = Math.min(UNICORN_HEIGHT, top + height); y < bottom; y++) {
            setPixel(x, y, colour_code);
        }
    }
}

function drawDigit(digit, left = 0, top = 0, colour_code = 0xf) {
    let digit_data = DIGITS[digit];
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 5; y++) {
            if ((digit_data >> (3*y + x)) & 1) {
                setPixel(left + x, top + y, colour_code);
            }
        }
    }
}

function getLetter(letter) {
    if (letter in characters) return (
      characters[letter].map(column => column << 2)
    );
    if (letter in accented_characters) {
      let acc_char = accented_characters[letter],
          base_letter = getLetter(acc_char[0]),
          accent = accents[acc_char[1]],
          shift = accent[acc_char[2]];
      return base_letter.map( (letter_col, i) => {
        let shifted_accent_col = (accent[i+2]) << (shift - 5);
        return (letter_col | shifted_accent_col);
      });
    }
    return getLetter('?');
}

function drawTime() {
    let now = new Date(),
        day = now.getDate(),
        month = 1+now.getMonth(),
        hour = now.getHours(),
        minute = now.getMinutes();
    drawDigit(Math.floor(day/10), 0, 0, 9);
    drawDigit(day % 10, 4, 0, 9);
    drawDigit(Math.floor(month/10), 10, 0, 9);
    drawDigit(month % 10, 14, 0, 9);
    drawDigit(Math.floor(hour/10), 0, 6, 10);
    drawDigit(hour % 10, 4, 6, 10);
    drawDigit(Math.floor(minute/10), 10, 6, 10);
    drawDigit(minute % 10, 14, 6, 10);
    setPixel(8, 7, 0xf);
    setPixel(8, 9, 0xf);
}

function writeText(text, offset_x = 0, colour_code = 0xf) {
    let columns = Array.from(text).reduce((prev, letter) => {
        return prev.concat(getLetter(letter),[0])
      },[]);
    columns.forEach( (coldata, x) => {
        let current_x = offset_x + x;
        if (current_x >= 0 && current_x < grid_data[0].length) {
            for (let y = 0; y < 11; y++) {
                let dot = ((coldata >> y) & 1) * colour_code;
                setPixel(current_x, y, dot);
            }
        }
    } );
}

function drawIcon(icon, offset_x = 0, offset_y = 0) {
    for (let x = 0; x < ICON_WIDTH; x++) {
        for (let y = 0; y < ICON_HEIGHT; y++) {
            setPixel(x + offset_x, y + offset_y, parseInt(icon[x + ICON_WIDTH * y],16));
        }
    }
}

let current_icon = "4".repeat(ICON_HEIGHT * ICON_WIDTH);

function updateDisplay() {
    rect(0,0,UNICORN_WIDTH,UNICORN_HEIGHT,0);
    drawTime();
    drawIcon(current_icon, 18);
    writeText(textinput.value, 28);
    document.getElementById('test').src = getImageUrl();
}

Array.from(document.getElementById('examples').childNodes).forEach( e => {
    e.addEventListener('click', function() {
        current_icon = e.getAttribute('title');
        updateDisplay();
    });
});

updateDisplay();
textinput.addEventListener('change', updateDisplay);
textinput.addEventListener('keyup', updateDisplay);
