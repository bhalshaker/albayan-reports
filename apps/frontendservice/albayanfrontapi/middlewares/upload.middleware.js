import multer from "multer";
import path from "path";
import crypto from "crypto";
import { config } from "../configs/config.js";

const storage = multer.diskStorage({
  destination: (request, file, callback) => {
    callback(null, config.UPLOAD_FOLDER);
  },
  filename: (request, file, callback) => {
    const extention = path.extname(file.originalname).toLowerCase();
    if (extention !== ".odt") {
      return cb(new Error("File extension should be .odt"));
    }
    const newFileName = `${crypto.randomUUID()}.odt`;
    callback(null, newFileName);
  },
});

const fileFilter = (request, file, callback) => {
  const extention = path.extname(file.originalname).toLowerCase();
  if (extention === ".odt") {
    callback(null, true);
  } else {
    callback(new Error("File extension should be .odt"));
  }
};

const upload = multer({ storage, fileFilter });

export { upload };
