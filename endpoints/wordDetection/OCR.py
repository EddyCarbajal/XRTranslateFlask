# # app.py
import os
from flask import Flask, request, jsonify, Blueprint
from PIL import Image
# import torch
# import torchvision.transforms as transforms
import pytesseract


def ocr(file):
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Check if the file is a JPEG
    if file and file.filename.endswith(('.jpeg', '.jpg', '.png')):
        # try:
            # Save the uploaded image temporarily
            image_path = "temp.jpg"
            file.save(image_path)

            # Load the image using PIL
            img = Image.open(image_path)

            # Perform OCR using pytesseract
            pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
            #pllsss
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            print("before tess")
            text = pytesseract.image_to_string(img)
            print("after tess")

            # You can also perform additional processing using PyTorch and other libraries here
            # For more advanced OCR, consider using a dedicated OCR library like Tesseract

            # Clean up the temporary image
            os.remove(image_path)

            return text
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format. Please upload a JPEG image."}), 400
