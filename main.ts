// news-image-20261122 — entry program (Node 22, standard library only).
//
// The shipped image is the entry.png beside this file: an original newspaper
// front page summing up the world news of Sunday 22 November 2026, drawn
// programmatically with Python/Pillow (see draw.py) at build time.
//
// This program validates the image against the bounty limits and then copies
// it, byte for byte, to <MAKEFUN_OUTPUT_DIR>/entry.png (default /output).
// Because it only ever copies the same validated bytes, repeated runs are
// deterministic: every run writes an identical file.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_DIMENSION = 1024; // px, width and height
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message) {
  console.error(`news-image-20261122: error: ${message}`);
  process.exit(1);
}

// Validate the raw bytes as a PNG within the bounty limits. Returns the
// image dimensions on success; exits the process with a clear error otherwise.
function validatePng(bytes) {
  if (bytes.length > MAX_BYTES) {
    fail(`entry.png is ${bytes.length} bytes, over the ${MAX_BYTES}-byte limit`);
  }
  if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail('entry.png does not start with the PNG signature');
  }
  // The first chunk must be IHDR: 4-byte length, then the type at offset 12.
  if (bytes.length < 24 || bytes.toString('ascii', 12, 16) !== 'IHDR') {
    fail('entry.png has no IHDR first chunk');
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width < 1 || height < 1) {
    fail(`entry.png has invalid dimensions ${width}x${height}`);
  }
  if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
    fail(`entry.png is ${width}x${height}, over the ${MAX_DIMENSION}x${MAX_DIMENSION} limit`);
  }
  // A complete PNG ends with an empty IEND chunk: 4-byte zero length, the
  // type "IEND" and its 4-byte CRC — 12 bytes in total. Requiring it here
  // rejects truncated files that would otherwise pass the header checks.
  const tail = bytes.subarray(bytes.length - 12);
  if (
    tail.readUInt32BE(0) !== 0 ||
    tail.toString('ascii', 4, 8) !== 'IEND' ||
    tail.readUInt32BE(8) !== 0xae426082
  ) {
    fail('entry.png does not end with a complete IEND chunk (truncated file?)');
  }
  return { width, height };
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, 'entry.png');

  let bytes;
  try {
    bytes = readFileSync(sourcePath);
  } catch {
    fail(`cannot read the shipped image at ${sourcePath}`);
  }

  const { width, height } = validatePng(bytes);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, 'entry.png');
  writeFileSync(outPath, bytes);

  console.log(
    `news-image-20261122: wrote ${outPath} (${bytes.length} bytes, ${width}x${height})`,
  );
}

main();
