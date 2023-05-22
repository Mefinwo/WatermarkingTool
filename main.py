import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os
import zipfile
import shutil


def add_watermark(image_path, watermark_path, output_path):
    # Open the image and watermark
    image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    # Resize watermark to fit the image
    width, height = image.size
    watermark_width, watermark_height = watermark.size
    target_width = width // 2
    target_height = height // 2
    resized_width = min(target_width, watermark_width)
    resized_height = min(target_height, watermark_height)
    watermark = watermark.resize((resized_width, resized_height))

    # Calculate the position to place the watermark at the center
    watermark_position = ((width - watermark.width) // 2, (height - watermark.height) // 2)

    # Create a transparent layer for watermark
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    watermark_layer.paste(watermark, watermark_position, mask=watermark)

    # Apply watermark to the image
    watermarked_image = Image.alpha_composite(image, watermark_layer)

    # Convert the image to RGB mode for saving as JPEG
    watermarked_image_rgb = watermarked_image.convert("RGB")

    # Save the watermarked image
    watermarked_image_rgb.save(output_path)




def process_images(folder_path, watermark_path):
    # Create a temporary folder for storing watermarked images
    output_folder = "Watermarked_Images"
    os.makedirs(output_folder, exist_ok=True)

    # Process each PNG and JPG image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            add_watermark(image_path, watermark_path, output_path)

    # Create a zip file to store watermarked images
    zip_filename = "Watermarked_Images.zip"
    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            zip_file.write(file_path, filename)

    # Remove the temporary folder and its contents
    shutil.rmtree(output_folder)

    return zip_filename



def browse_folder():
    # Prompt user to select a folder
    folder_path = filedialog.askdirectory()
    if folder_path:
        watermark_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if watermark_path:
            # Process images and create a zip file
            zip_filename = process_images(folder_path, watermark_path)
            result_label.config(text=f"Images watermarked and saved as {zip_filename}")
        else:
            result_label.config(text="No watermark image selected.")
    else:
        result_label.config(text="No folder selected.")


# Create the main window
window = tk.Tk()
window.title("Watermark App")

# Add a label and a button for selecting a folder
folder_label = tk.Label(window, text="Select a folder:")
folder_label.pack(pady=10)

browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

# Add a label to display the result
result_label = tk.Label(window, text="")
result_label.pack(pady=10)

window.mainloop()