from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance

# ---------------------------- CONSTANTS ------------------------------- #
BROWN = "#964B00"
WHITE = "#FFFFFF"
BLACK = "#000000"
FONT_NAME = "Manrope"
DEFAULT_FONT_SIZE = 30
IMAGE_PATH = None  # To store the path of the uploaded image
original_image = None
watermarked_image = None
# ---------------------------- FUNCTIONS ------------------------------- #
def upload_image():
    global IMAGE_PATH, original_image
    # Open file dialog to pick an image
    IMAGE_PATH = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )

    if IMAGE_PATH:
        # Open a new window showing the image
        original_image = Image.open(IMAGE_PATH)
        open_image_window()

def open_image_window():
    global original_image

    new_window = Toplevel(window)
    new_window.title("Image Preview")
    new_window.config(padx=50, pady=50, bg=WHITE)

    # Resize the image to fit within the window for display purposes
    image_display = original_image.copy()
    image_display.thumbnail((500, 500))  # Create a smaller display image

    img_tk = ImageTk.PhotoImage(image_display)

    canvas = Canvas(new_window, width=image_display.width, height=image_display.height)
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.grid(row=0, column=0, columnspan=2)
    canvas.image = img_tk  # Keep reference to avoid garbage collection

    # Watermark text entry field
    watermark_label = Label(new_window, text="Watermark Text:", font=FONT_NAME, bg=WHITE)
    watermark_label.grid(row=1, column=0, sticky="e")

    watermark_entry = Entry(new_window, width=20)
    watermark_entry.grid(row=1, column=1, sticky="w")

    # Place watermark button
    watermark_button = Button(new_window, text="Place Watermark", font=FONT_NAME, highlightthickness=0,
                              command=lambda: place_watermark(canvas, watermark_entry.get()))
    watermark_button.grid(row=2, column=0, columnspan=2, sticky="ew")

    # Save button
    save_button = Button(new_window, text="Save Image", font=FONT_NAME, highlightthickness=0,
                         command=save_image)
    save_button.grid(row=3, column=0, columnspan=2, sticky="ew")

    new_window.mainloop()


def place_watermark(canvas, watermark_text):
    global original_image, watermarked_image

    # Create the watermark layer with transparency
    watermarked_image = original_image.copy()
    txt_layer = Image.new('RGBA', watermarked_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Set font for watermark
    font = ImageFont.truetype("arial.ttf", DEFAULT_FONT_SIZE)

    # Define transparency level for text and background
    transparency_text = 100  # Transparency for text
    transparency_background = 50  # Transparency for background
    text_color = (0, 0, 0, transparency_text)  # Black text with transparency
    background_color = (255, 255, 255, transparency_background)  # White transparent background

    # Get image dimensions
    width, height = watermarked_image.size

    # Define the spacing between each watermark instance
    spacing = 300  # Adjust this value to increase/decrease spacing

    # Repeat watermark text diagonally across the image with transparency and background
    for x in range(0, width, spacing):
        for y in range(0, height, spacing):
            # Get text bounding box to calculate width and height of the text
            bbox = draw.textbbox((x, y), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Draw a transparent white rectangle behind the text
            draw.rectangle(
                [(x, y), (x + text_width, y + text_height)],
                fill=background_color
            )

            # Draw the watermark text on top of the transparent rectangle
            draw.text((x, y), watermark_text, font=font, fill=text_color)

    # Rotate the watermark layer diagonally
    txt_layer = txt_layer.rotate(45, expand=1)

    # Crop or resize the rotated layer to match the original image size
    txt_layer = txt_layer.crop((0, 0, width, height))

    # Composite the watermark onto the original image
    watermarked_image = Image.alpha_composite(watermarked_image.convert('RGBA'), txt_layer)

    # Resize the watermarked image for display
    display_image = watermarked_image.copy()
    display_image.thumbnail((500, 500))  # Keep the display size small

    # Update the canvas with the watermarked image
    watermarked_img_tk = ImageTk.PhotoImage(display_image.convert('RGB'))
    canvas.create_image(0, 0, anchor=NW, image=watermarked_img_tk)
    canvas.image = watermarked_img_tk  # Keep reference to avoid garbage collection


def save_image():
    global watermarked_image
    if watermarked_image:
        # Save the watermarked image
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]
        )
        if save_path:
            # Save in the same format as the original
            watermarked_image.convert('RGB').save(save_path)
            print(f"Image saved at {save_path}")


# ---------------------------- MAIN UI SETUP ------------------------------- #

window = Tk()
window.title("Watermark Stamper")
window.config(padx=100, pady=50, bg=WHITE)

# Configuring grid weights for centering elements
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

# Title label
title_label = Label(text="Watermark Stamper", fg=BROWN, bg=WHITE, font=(FONT_NAME, 30))
title_label.grid(column=0, row=0, columnspan=3, sticky="nsew")

# Adjusting canvas size to match the image size
canvas = Canvas(width=282, height=274, bg=WHITE, highlightthickness=0)
stamper_img = PhotoImage(file="stamper.png")  # Replace with your image path
canvas.create_image(141, 137, image=stamper_img)  # Center the image in the canvas
canvas.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=60)

# Upload image button
button_start = Button(text="Upload image", font=FONT_NAME, highlightthickness=0, command=upload_image)
button_start.grid(column=1, row=2, sticky="nsew", padx=60)

window.mainloop()
