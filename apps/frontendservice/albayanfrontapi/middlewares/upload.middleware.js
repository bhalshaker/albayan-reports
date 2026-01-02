import multer from "multer";
import path from "path";
import crypto from "crypto";
import { config } from "../configs/config.js";

// Configure storage settings for multer
const storage = multer.diskStorage({
  // Define destination folder for uploads
  destination: (request, file, callback) => {
    // Set the upload folder from config
    callback(null, config.UPLOAD_FOLDER);
  },
  // Define filename for uploaded files
  filename: (request, file, callback) => {
    // Validate file extension
    const extention = path.extname(file.originalname).toLowerCase();
    if (extention !== ".odt") {
      return callback(new Error("File extension should be .odt"));
    }
    // Generate a unique filename
    const newFileName = `${crypto.randomUUID()}.odt`;
    // Return the new filename
    callback(null, newFileName);
  },
});

// File filter to accept only .odt files
const fileFilter = (request, file, callback) => {
  // Check the file extension
  const extention = path.extname(file.originalname).toLowerCase();
  // Accept the file if it is .odt
  if (extention === ".odt") {
    callback(null, true);
  } else {
    callback(new Error("File extension should be .odt"));
  }
};

// Initialize multer with the defined storage and file filter
const upload = multer({ storage, fileFilter });

export { upload };
