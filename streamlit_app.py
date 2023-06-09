import streamlit as st
import cv2
import pytesseract
import os
import pyautogui
from PIL import Image, ImageDraw, ImageFont

def convert_to_handwritten_text(image):
    # Save the uploaded image temporarily
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as file:
        file.write(image.getbuffer())

    # Load the image using OpenCV
    img = cv2.imread(temp_image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(threshold)

    # Delete the temporary image file
    os.remove(temp_image_path)

    return text

def convert_to_handwritten_image(text):
    # Create a blank canvas
    image = Image.new("RGB", (500, 500), color="white")
    draw = ImageDraw.Draw(image)

    # Set the initial position for writing
    x, y = 10, 10

    # Set the font size and style
    font_size = 30
    font = ImageFont.truetype("/Users/adityadeore/Documents/Lucida Handwriting Italic.ttf", font_size)  # Replace "arial.ttf" with the path to your desired font file

    # Write the text in a handwriting style
    draw.text((x, y), text, font=font, fill="black")

    # Save the handwritten image
    temp_image_path = "handwritten_text.png"
    image.save(temp_image_path)

    return temp_image_path

def main():
    st.title("Digital to Handwritten Text Converter")

    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Convert image to handwritten text on button click
        if st.button("Convert"):
            text = convert_to_handwritten_text(uploaded_file)
            temp_image_path = convert_to_handwritten_image(text)

            # Display the handwritten text image
            st.image(temp_image_path, caption='Handwritten Text', use_column_width=True)

            # Delete the temporary image file
            os.remove(temp_image_path)

if __name__ == "__main__":
    main()
