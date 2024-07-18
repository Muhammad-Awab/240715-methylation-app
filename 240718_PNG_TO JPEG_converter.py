import os
from PIL import Image
import streamlit as st


def convert_and_save(uploaded_file):
    if uploaded_file is not None:
        # Open the uploaded file as an image
        img = Image.open(uploaded_file)
        rgb_img = img.convert('RGB')
        # Construct the new file name
        file_name = os.path.splitext(uploaded_file.name)[0] + '.jpeg'
        # Save the image in JPEG format in the same folder as the uploaded file
        save_path = os.path.join(os.path.dirname(uploaded_file.name), file_name)
        rgb_img.save(save_path, 'JPEG')
        return save_path
    return None


def main():
    st.title("PNG to JPEG Converter")

    # File uploader for multiple PNG files
    uploaded_files = st.file_uploader("Choose PNG files", type="png", accept_multiple_files=True)

    if st.button("Convert to JPEG"):
        for uploaded_file in uploaded_files:
            save_path = convert_and_save(uploaded_file)
            if save_path:
                st.success(f"Converted and saved to {save_path}")
            else:
                st.error("Failed to convert the file")


if __name__ == "__main__":
    main()