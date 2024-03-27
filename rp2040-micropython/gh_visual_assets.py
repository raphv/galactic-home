DIGITS = (
    0o35556, 0o72232, #0,1
    0o71243, 0o34347, #2,3
    0o44755, 0o34717, #4,5
    0o35716, 0o11247, #6,7
    0o35256, 0o34756, #8,9
)

BASE_COLORS = (
   ( 0x00, 0x00, 0x00 ), # 0 = BLACK
   ( 0xff, 0x60, 0x60 ), # 1 = RED
   ( 0x60, 0xff, 0x60 ), # 2 = GREEN
   ( 0x60, 0x60, 0xff ), # 3 = BLUE
   ( 0xff, 0xff, 0x60 ), # 4 = YELLOW
   ( 0xff, 0x60, 0xff ), # 5 = MAGENTA
   ( 0x60, 0xff, 0xff ), # 6 = CYAN
   ( 0xff, 0xa0, 0xa0 ), # 7 = RED-ISH
   ( 0xa0, 0xff, 0xa0 ), # 8 = GREEN-ISH
   ( 0xa0, 0xa0, 0xff ), # 9 = BLUE-ISH
   ( 0xff, 0xff, 0xa0 ), # a = YELLOW-ISH
   ( 0xff, 0xa0, 0xff ), # b = MAGENTA-ISH
   ( 0xa0, 0xff, 0xff ), # c = CYAN-ISH
   ( 0x80, 0x80, 0x80 ), # d = GRAY
   ( 0xcc, 0xcc, 0xcc ), # e = OFF-WHITE
   ( 0xff, 0xff, 0xff ), # f = WHITE
)

HTML_HOME = """<!doctype html>
<html>
 <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Galactic Unicorn</title>
  <style>
   body { background: black; color: white; font-family: sans-serif; }
   h1, h2 { text-align: center; }
   ul { list-style: none; max-width: 400px; margin: 1em auto; padding: 0; }
   li { background: #202020; padding: .5em; margin: .5em 0; display: flex; flex-direction: row; justify-content: flex-start; align-items: center; font-size: 1.2em; }
   circle { stroke: none }
   span { padding: .5em }
   .c-0 { fill: #404040 }
   .c-1 { fill: #ff6060 }
   .c-2 { fill: #60ff60 }
   .c-3 { fill: #6060ff }
   .c-4 { fill: #ffff60 }
   .c-5 { fill: #ff60ff }
   .c-6 { fill: #60ffff }
   .c-7 { fill: #ffa0a0 }
   .c-8 { fill: #a0ffa0 }
   .c-9 { fill: #a0a0ff }
   .c-a { fill: #ffffa0 }
   .c-b { fill: #ffa0ff }
   .c-c { fill: #a0ffff }
   .c-d { fill: #808080 }
   .c-e { fill: #cccccc }
   .c-f { fill: #ffffff }
   button { font-size: 1.5em; display: block; margin: 1em auto; color: inherit; background: #000080; border: none; border-radius: 1em; padding: .5em 5em; }
   a { color: #ffffcc; }
  </style>
 </head>
 <body>
  <h1>Galactic Unicorn</h1>
  <div id="status"></div>
  <button id="ring">Ring!</button>
  <p><a href="/errors">Show errors</a></p>
  <script>
function makeDot(c,i) {
  let y = Math.floor(i/9), x = (i%9);
  return `<circle cx=${.5+x} cy=${.5+y} r=".5" class="c-${c}"/>`;
};
function makeIcon(icon) {
   if (!icon) return '';
   return '<svg width="45" height="55" viewBox="0 0 9 11">'
   + Array.from(icon).map(makeDot).join('') + '</svg>';
}
function update() {
  fetch('/data').then((resp) => {
     return resp.json();
  }).then((data) => {
     tbl = '<ul>' + data.data.map((s) => {
       return `<li>${makeIcon(s.icon)}<span>${s.text}</span></li>`;
     }).join('') + '</ul>';
     document.getElementById('status').innerHTML = `<h2>Updated: ${data.time}</h2>${tbl}`;
 });
}
update();
window.setInterval(update, 30000);
document.getElementById('ring').addEventListener('click', e => { fetch('/ring'); });
  </script>
 </body>
</html>"""
