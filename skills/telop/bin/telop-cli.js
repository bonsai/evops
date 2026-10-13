#!/usr/bin/env node
// telop-cli.js — telop スキル用 CLI
// Usage: node scripts/telop-cli.js --input <video> --spec <spec.json> --output <output>

import { program } from 'commander';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

program
  .requiredOption('--input <path>', 'Input video path')
  .requiredOption('--spec <path>', 'telop_spec.json path')
  .requiredOption('--output <path>', 'Output video path')
  .option('--font <family>', 'Font family for text', 'IPAexGothic')
  .option('--font-size <size>', 'Font size in pixels', '40')
  .option('--color <hex>', 'Text color in hex', '#ffffff')
  .parse();

const opts = program.opts();

if (!fs.existsSync(opts.input)) {
  console.error(`Input not found: ${opts.input}`);
  process.exit(1);
}
if (!fs.existsSync(opts.spec)) {
  console.error(`Spec not found: ${opts.spec}`);
  process.exit(1);
}

const spec = JSON.parse(fs.readFileSync(opts.spec, 'utf-8'));
const inputPath = opts.input;
const outputPath = opts.output;

// Build ffmpeg filter complex for telop/overlay generation
let filterArgs = [];

// Opening title
if (spec.opening) {
  const { title, subtitle, duration, font = 'IPAexGothic', color = '#ffffff' } = spec.opening;
  const t = duration || 3;
  filterArgs.push(
    `drawtext=text='${title}':fontfile=/usr/share/fonts/truetype/fonts-japanese-mincho.ttf:fontsize=${opts.font_size}:fontcolor=${color}:box=1:boxcolor=0x000000AA:x=(w-text_w)/2:y=50`
  );
  
  if (subtitle) {
    filterArgs.push(
      `drawtext=text='${subtitle}':fontfile=/usr/share/fonts/truetype/fonts-japanese-mincho.ttf:fontsize=${opts.font_size-10}:fontcolor=${color}:box=1:boxcolor=0x000000AA:x=(w-text_w)/2:y=100`
    );
  }
}

// Panel overlays
spec.panels?.forEach((p, i) => {
  const duration = p.duration || 12;
  // Simplified: show panel text at specified position
  const x = p.position === 'top' ? 50 : p.position === 'center' ? (w - text_w) / 2 : 50;
  const y = p.position === 'top' ? 50 : p.position === 'center' ? (h + text_h) / 2 : h - 100;
  filterArgs.push(
    `drawtext=text='${p.overlay}':fontfile=/usr/share/fonts/truetype/fonts-japanese-mincho.ttf:fontsize=${opts.font_size}:fontcolor=${color}:box=1:boxcolor=0x000000AA:x:${x}:y:${y}`
  );
});

// Ending credits
if (spec.ending) {
  const { credits, duration, font, fade } = spec.ending;
  const t = duration || 5;
  // Credit roll implementation (simplified)
  credits.forEach((c, idx) => {
    const y = h - 100 + idx * 40;
    filterArgs.push(
      `drawtext=text='${c}':fontfile=/usr/share/fonts/truetype/fonts-japanese-mincho.ttf:fontsize=${opts.font_size}:fontcolor=${color}:box=1:boxcolor=0x000000AA:x=(w-text_w)/2:y=${y}`
    );
  });
}

// Subtitle track
if (spec.subtitle_track) {
  // Would generate WebVTT/ASS and use ffmpeg's subtitle filter
  // For now, just log
  console.log('Subtitle track specified, will generate VTT/ASS');
}

// Build the full ffmpeg command
const filterComplex = filterArgs.join(';');
const cmd = `ffmpeg -y -i "${inputPath}" -vf "${filterComplex}" -c:a copy "${outputPath}"`;

try {
  execSync(cmd, { stdio: 'inherit' });
  console.log(`Success: ${outputPath}`);
} catch (err) {
  console.error(`FFmpeg error: ${err.message}`);
  process.exit(1);
}