// Depth colouring demo on SYNTHETIC frames: depth_engine.js (identical to depth_display.py / OpenCV in the tests)
// colours a frame exactly as test_kinect.py's Depth window would; hover to read the depth and the 8-bit value.
import { route, app, api, esc, list } from './core.js';
import { colorizeDepth } from './depth_engine.js';

route('demo', async () => {
  const [lut, scenes] = await Promise.all([api('/jet_lut'), api('/synthetic')]);
  app().innerHTML = `<p class="kicker">Interactive demo</p><h1>Depth colouring demo</h1>
  <p class="callout"><b>Synthetic data.</b> The repo holds no recorded Kinect frames, so these depth frames are made up
  for the demo (simple shapes, in millimetres, 160×120). The colouring is the real thing: the same min-max stretch and
  OpenCV JET map as <code>test_kinect.py</code>, matched pixel for pixel in the tests.</p>
  <div class="demo-grid">
    <div class="panel">
      <label for="k-sc">Synthetic scene</label>
      <select id="k-sc">${list(scenes, s => `<option value="${esc(s.name)}">${esc(s.name.replace(/_/g, ' '))}</option>`)}</select>
      <p id="k-doc" class="small mute"></p>
      <div id="k-kv" class="kvs"></div>
      <p id="k-probe" class="out" aria-live="polite">Hover over the image to read a pixel.</p>
      <h3>JET colour map (0 → 255)</h3><canvas id="k-bar" width="256" height="16" class="bar" aria-label="JET colour bar"></canvas>
    </div>
    <div class="stage"><canvas id="k-img" width="160" height="120" aria-label="Colourised synthetic depth frame"></canvas></div>
  </div>`;
  const $ = id => document.getElementById(id);
  const bar = $('k-bar').getContext('2d');
  lut.forEach((c, i) => { bar.fillStyle = `rgb(${c[0]},${c[1]},${c[2]})`; bar.fillRect(i, 0, 1, 16); });
  let frame = null, res = null;
  async function show(name) {
    frame = await api('/synthetic/' + name);
    res = colorizeDepth(frame.depth, lut);
    const g = $('k-img').getContext('2d');
    g.putImageData(new ImageData(res.rgba, frame.width, frame.height), 0, 0);
    $('k-doc').textContent = scenes.find(s => s.name === name).doc;
    const zeros = frame.depth.filter(v => v === 0).length;
    $('k-kv').innerHTML = list([[`${res.lo} mm`, 'frame minimum → 0 (blue)'], [`${res.hi} mm`, 'frame maximum → 255 (red)'],
      [zeros, 'pixels at 0 mm (no reading)']], ([v, k]) => `<div><b>${esc(String(v))}</b><span>${esc(k)}</span></div>`) +
      (zeros ? '<p class="small err" style="grid-column:1/-1">The 0 mm pixels set the minimum, so the real scene only uses the upper part of the colour range.</p>' : '');
  }
  $('k-img').addEventListener('mousemove', e => {
    if (!frame) return;
    const r = e.target.getBoundingClientRect();
    const x = Math.floor((e.clientX - r.left) / r.width * frame.width), y = Math.floor((e.clientY - r.top) / r.height * frame.height);
    const i = y * frame.width + x;
    if (i >= 0 && i < frame.depth.length) $('k-probe').textContent = `x ${x}, y ${y}: ${frame.depth[i]} mm → ${res.norm[i]} → rgb(${lut[res.norm[i]].join(', ')})`;
  });
  $('k-sc').addEventListener('change', e => show(e.target.value));
  await show(scenes[0].name);
});
