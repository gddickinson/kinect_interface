// JS port of depth_display.colorize_depth (the Depth window of test_kinect.py): cv2.normalize(NORM_MINMAX, 8-bit)
// then cv2.applyColorMap(JET). The JET table itself comes from OpenCV via the API (/jet_lut). depth_engine.test.mjs
// checks every pixel against the Python on the synthetic frames (tests/fixtures/depth_cases.json).

// cvRound: round half to even.
const roundEven = v => { const f = Math.floor(v), d = v - f; return d > 0.5 ? f + 1 : d < 0.5 ? f : (f % 2 === 0 ? f : f + 1); };

export function normalizeDepth(depth) {
  let lo = Infinity, hi = -Infinity;
  for (const v of depth) { if (v < lo) lo = v; if (v > hi) hi = v; }
  const out = new Uint8Array(depth.length);
  if (!(hi > lo)) return { out, lo, hi };                     // flat frame: OpenCV gives all zeros
  const scale = 255 / (hi - lo), shift = -lo * scale;
  for (let i = 0; i < depth.length; i++) out[i] = Math.max(0, Math.min(255, roundEven(depth[i] * scale + shift)));
  return { out, lo, hi };
}

// RGBA pixels for a canvas ImageData (lut rows are [r, g, b]).
export function colorizeDepth(depth, lut) {
  const { out, lo, hi } = normalizeDepth(depth);
  const rgba = new Uint8ClampedArray(depth.length * 4);
  out.forEach((v, i) => { const c = lut[v]; rgba.set([c[0], c[1], c[2], 255], i * 4); });
  return { rgba, norm: out, lo, hi };
}
