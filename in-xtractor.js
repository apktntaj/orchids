import fs from "fs-extra";
import path from "path";
import Tesseract from "tesseract.js";
import {createRequire} from "module";

const require = createRequire(import.meta.url)
const pdf = require("pdf-parse")

const INPUT_DIR = "./input";
const OUTPUT = [];

async function extractText(filePath) {
  if (filePath.endsWith(".pdf")) {
    const data = await pdf(await fs.readFile(filePath));
    return data.text;
  }

  const result = await Tesseract.recognize(filePath, "eng");
  return result.data.text;
}

function parseBOL(text) {
  const bolNo = text.match(/Bill of Lading\s+No\.?\s*(\d{4})/i)?.[1];
  const date = text.match(/Date\s*[:\-]?\s*(\d{1,2}\/\d{1,2}\/\d{4})/)?.[1];

  const shipTo = text.match(/SHIP TO:\s*([\s\S]*?)\n\n/i)?.[1]?.trim();
  const billTo = text.match(/BILL TO:\s*([\s\S]*?)\n\n/i)?.[1]?.trim();

  const palletIds = [...text.matchAll(/PALLET ID:\s*(\d+)/gi)].map(m => m[1]);

  return {
    bolNo,
    date,
    shipTo,
    billTo,
    palletIds
  };
}

async function run() {
  const files = await fs.readdir(INPUT_DIR);
  console.log(files)

  for (const file of files) {
    const filePath = path.join(INPUT_DIR, file);
    const text = await extractText(filePath);
    const data = parseBOL(text);

    if (data.bolNo) {
      OUTPUT.push({
        file,
        ...data
      });
    }

    console.log(OUTPUT)
  }

  await fs.writeJson("./output/index.json", OUTPUT, { spaces: 2 });
  console.log("Extraction done");
}

run();
