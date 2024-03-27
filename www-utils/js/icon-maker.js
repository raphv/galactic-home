const WIDTH = 9,
    HEIGHT = 11,
    COLOR_COUNT = 16,
    colourselector = document.getElementById('colour-selector'),
    iconimage = document.getElementById('icon-image'),
    textinput = document.getElementById('icon-text');

let currentPoint = -1,
    examples = [
        "000e000000eeeee000eeeeeeee00eeeeee000000000000000c0c000cccccc00cccccccccccccccccc0ccccccc0000000000",
        "000000000eee00eee00000000000eee00eee000000000eee00eee00000000000eee00eee000000000eee00eee0000000000",
        "000eee0000eeeeee00eeeeeeeee0eeeeeee0000000000000aaa000000aaa00000aaa000000aaa00000000aa00000000a000",
        "0000044000000444400004444440004444440000444400000c4c000cccccc00cccccccccccccccccc0ccccccc0000000000",
        "000eee0000eeeeee00eeeeeeeee0eeeeeee0000000000003000300300030003003000300300030003003000300300030003",
        "000eee0000eeeeee00eeeeeeeee0eeeeeee0000000000000f000000f0f0f00000fff00000f0f0f000000f00000000000000",
        "000000000000040000040444040004444400044444440444444444044444440004444400040444040000040000000000000",
        "000000110000000110000000770001000770011100dd0111110dd0000000dd0000000990000009999000003333000000330",
        "000000110000000110000000770000000770000000dd0333330dd0033300dd0003000990000009999000003333000000330",
        "030000000030000000333000000333000030030000030000000333000300333000300030003330000003330000000300000",
        "000000110000000770000000770000000dd0000a0999900a0a99990a000a330aa000aa000a000a0000a000a0000aaaaa000",
        "0000a0000000a0a00000a011a000a00770a0aa00770aa0a00dd0a00a00dd0a00a09999a00a09999a00a00330a00aaaaaaa0",
        "000040000040444040004444400444444444334444400343444340333043300000000000333033300333033300333033300",
        "000000000000888000888888888000000000088888880080808080080808080080808080080808080088888880000000000",
        "0000a0000000a40000000a4a0000000d0000000eee000000eee000044444440055555550044444440055555550044444440",
        "000000000000222000002222200022222220220222022222222222220222022022000220002222200000222000000000000",
        "000000000000444000004444400044444440440444044444444444440000044044444440004444400000444000000000000",
        "000000000000111000001111100011111110110111011111111111111000111010111010001111100000111000000000000",
    ];

function moveToCircle(i) {
    currentPoint = i;
    colourselector.style.display = 'flex';
    colourselector.style.left = (10+20*(i%WIDTH))+"px";
    colourselector.style.top = (10+20*(Math.floor(i/WIDTH)))+"px";
}
function updateInput() {
    let text = textinput.value;
    for (let i = 0, n = Math.min(WIDTH*HEIGHT,text.length); i < n; i++) {
        iconimage.childNodes[i].setAttribute('class','c-'+text[i])
    }
}
function makeSvg(iconstr) {
    return `<svg width="45" height="55" viewBox="-.5 -.5 ${WIDTH} ${HEIGHT}" title="${iconstr}">`
        + Array.from(iconstr).map(
            (c, i) => `<circle cx="${i%WIDTH}" cy="${Math.floor(i/WIDTH)}" r=".4" class="c-${c}" />` 
            ).join('')
        + '</svg>'
}

colourselector.innerHTML = Array.from(Array(COLOR_COUNT)).map(
    (n, i) => `<button class="c-${i.toString(16)}"></button>`
).join('');
iconimage.innerHTML = Array.from(Array(WIDTH*HEIGHT)).map(
    n => `<button></button>`
).join('');
document.getElementById('examples').innerHTML = examples.map(
    n => makeSvg(n)
).join('');

Array.from(iconimage.childNodes).forEach( (e, i) => {
    e.addEventListener('mouseover', function() {
        moveToCircle(i);
    });
    e.addEventListener('focus', function() {
        moveToCircle(i);
    });
    e.addEventListener('click', function() {
        moveToCircle(i);
        document.querySelector('#colour-selector button.'+e.className).focus();
    });
});
Array.from(colourselector.childNodes).forEach( (b, i) => {
    b.addEventListener('click', function() {
        if (currentPoint >= 0 && currentPoint < textinput.value.length) {
            textinput.value = textinput.value.substr(0, currentPoint) + i.toString(16) + textinput.value.substr(1+currentPoint);
            iconimage.childNodes[currentPoint].focus();
            updateInput();
        }
    });
});
Array.from(document.getElementById('examples').childNodes).forEach( e => {
    e.addEventListener('click', function() {
        textinput.value = e.getAttribute('title');
        updateInput();
    });
});

textinput.value = "0".repeat(WIDTH*HEIGHT);
updateInput();
textinput.addEventListener('change', updateInput);
textinput.addEventListener('keyup', updateInput);
document.getElementById('copy-button').addEventListener('click', e => {
    textinput.focus();
    textinput.select();
    document.execCommand('copy');
});
