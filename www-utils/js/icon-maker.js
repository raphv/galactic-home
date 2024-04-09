const colourselector = document.getElementById('colour-selector'),
    iconimage = document.getElementById('icon-image'),
    icontextinput = document.getElementById('icon-text');;

let currentPoint = -1;

function moveToCircle(i) {
    currentPoint = i;
    colourselector.style.display = 'flex';
    colourselector.style.left = (10+20*(i % ICON_WIDTH))+"px";
    colourselector.style.top = (10+20*(Math.floor(i/ICON_WIDTH)))+"px";
}
function updateInput() {
    let text = icontextinput.value;
    for (let i = 0, n = Math.min(ICON_WIDTH * ICON_HEIGHT, text.length); i < n; i++) {
        iconimage.childNodes[i].setAttribute('class','c-'+text[i])
    }
}

colourselector.innerHTML = Array.from(Array(16)).map(
    (n, i) => `<button class="c-${i.toString(16)}"></button>`
).join('');
iconimage.innerHTML = Array.from(Array( ICON_WIDTH * ICON_HEIGHT )).map(
    n => `<button></button>`
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
        if (currentPoint >= 0 && currentPoint < icontextinput.value.length) {
            icontextinput.value = icontextinput.value.substr(0, currentPoint) + i.toString(16) + icontextinput.value.substr(1+currentPoint);
            iconimage.childNodes[currentPoint].focus();
            updateInput();
        }
    });
});
Array.from(document.getElementById('examples').childNodes).forEach( e => {
    e.addEventListener('click', function() {
        icontextinput.value = e.getAttribute('title');
        updateInput();
    });
});

icontextinput.value = "0".repeat( ICON_WIDTH * ICON_HEIGHT );
updateInput();
icontextinput.addEventListener('change', updateInput);
icontextinput.addEventListener('keyup', updateInput);
document.getElementById('copy-button').addEventListener('click', e => {
    icontextinput.focus();
    icontextinput.select();
    document.execCommand('copy');
});
