// Portraits with Meta Muse Image (same API and key as cocoverse). node gen.mjs id [id...]
// Fictional job archetypes and fictional applicants, no real people.
import fs from 'node:fs';
const env = Object.fromEntries(fs.readFileSync('/Users/aisandbox/Documents/coco/.env.local', 'utf8').split('\n').filter((l) => /^[A-Z_]+=/.test(l)).map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1).trim().replace(/^"|"$/g, '')]));
const KEY = env.MODEL_API_KEY || env.META_API_KEY;
const BASE = env.META_API_BASE_URL || 'https://api.meta.ai/v1';
const STYLE = 'Warm hand-drawn editorial illustration, colored pencil and soft gouache, gentle cross-hatching, friendly and dignified, head-and-shoulders portrait slightly off-center, soft natural light, a light airy background scene that says what this person does. An invented person, not any real individual. No text, no letters, no logos, no border.';
const P = JSON.parse(fs.readFileSync(new URL('./prompts.json', import.meta.url)));
for (const id of process.argv.slice(2)) {
  const r = await fetch(`${BASE}/images/generations`, { method: 'POST', headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'muse-image-1.0', n: 1, prompt: `${P[id]} ${STYLE}` }) });
  const j = await r.json().catch(() => null);
  if (!r.ok) { console.log('fail', id, r.status, JSON.stringify(j).slice(0, 300)); continue; }
  const d = j.data?.[0];
  const buf = d?.b64_json ? Buffer.from(d.b64_json, 'base64') : d?.url ? Buffer.from(await (await fetch(d.url)).arrayBuffer()) : null;
  if (!buf) { console.log('no image', id); continue; }
  fs.writeFileSync(new URL(`./gen/${id}.png`, import.meta.url), buf);
  console.log('ok', id, buf.length);
}
