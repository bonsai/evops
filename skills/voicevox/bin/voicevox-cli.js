#!/usr/bin/env node
// voicevox-cli.js — ななちゃん（Nana-chan / speaker 2）で音声生成
// Usage: node bin/voicevox-cli.js --text "..." --speaker 2 --output narration.mp3

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { text: '', speaker: 2, output: '/tmp/voicevox_output.mp3', speed: 1.0, pitch: 0.0, intonation: 1.0 };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--text': args.text = argv[++i]; break;
      case '--speaker': args.speaker = parseInt(argv[++i], 10); break;
      case '--output': args.output = argv[++i]; break;
      case '--speed': args.speed = parseFloat(argv[++i]); break;
      case '--pitch': args.pitch = parseFloat(argv[++i]); break;
      case '--intonation': args.intonation = parseFloat(argv[++i]); break;
    }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.text) {
    console.error('Usage: node voicevox-cli.js --text "..." --speaker 2 [--output ...]');
    process.exit(1);
  }

  const voicevoxUrl = process.env.VOICEVOX_HOST || 'http://localhost:50021';
  const audioQueryUrl = new URL('/audio_query', voicevoxUrl);
  audioQueryUrl.search = new URLSearchParams({ text: args.text, speaker: args.speaker.toString() }).toString();

  console.log(`[voicevox-cli] Calling Voicevox (speaker: ${args.speaker}, text length: ${args.text.length})`);
  console.log(`[voicevox-cli] URL: ${audioQueryUrl.toString()}`);

  try {
    // Step 1: Generate audio query (POST /audio_query)
    const queryPayload = JSON.stringify({ text: args.text, speaker: args.speaker, core_version: '0.14.0', speed_scale: args.speed, pitch_scale: args.pitch, intonation_scale: args.intonation, volume_scale: 1.0, pre_phoneme_length: 0.1, post_phoneme_length: 0.1, output_stereo: false, kana: '' });

    execSync(`curl -s -X POST -H 'Content-Type: application/json' -d '${queryPayload}' '${audioQueryUrl.toString()}' -o /tmp/audio_query.json`, { stdio: 'inherit' });

    // Step 2: Synthesis (POST /synthesis with audio_query response)
    const synthesisUrl = new URL('/synthesis', voicevoxUrl);
    synthesisUrl.search = new URLSearchParams({ text: args.text, speaker: args.speaker.toString() }).toString();

    execSync(`curl -s -X POST -H 'Content-Type: application/json' -H 'accept: audio/wav' -d '@/tmp/audio_query.json' '${synthesisUrl.toString()}' -o '${args.output}'`, { stdio: 'inherit' });

    console.log(`[voicevox-cli] Success: ${args.output}`);
  } catch (err) {
    console.error('[voicevox-cli] Error:', err.message || err);
    process.exit(1);
  }
}

main();
