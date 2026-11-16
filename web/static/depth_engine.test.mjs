// Node test: the JS normalisation + JET colouring equals depth_display.py (OpenCV) pixel for pixel on the synthetic
// frames in tests/fixtures/depth_cases.json. Run: node web/static/depth_engine.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { normalizeDepth, colorizeDepth } from './depth_engine.js';

const fx = JSON.parse(readFileSync(new URL('../../tests/fixtures/depth_cases.json', import.meta.url)));
let px = 0;
for (const c of fx.cases) {
  const { out: norm } = normalizeDepth(c.depth);
  assert.deepEqual([...norm], c.norm, c.name + ' normalised');
  const { rgba } = colorizeDepth(c.depth, fx.lut);
  c.rgb.forEach((p, i) => assert.deepEqual([rgba[i * 4], rgba[i * 4 + 1], rgba[i * 4 + 2]], p, `${c.name} pixel ${i}`));
  px += c.depth.length;
}
assert.deepEqual([...normalizeDepth([7, 7, 7]).out], [0, 0, 0]);
console.log(`depth engine ok (${fx.cases.length} synthetic frames, ${px} pixels identical to OpenCV)`);
