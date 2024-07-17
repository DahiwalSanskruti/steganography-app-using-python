import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_message_in_image(image_path, message, save_path):
    try:
        img = Image.open(image_path)
        encoded_img = img.copy()
        width, height = img.size
        index = 0

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # Add a delimiter to indicate end of message

        for row in range(height):
            for col in range(width):
                if index < len(binary_message):
                    pixel = list(img.getpixel((col, row)))

                    for n in range(3):  # For each RGB channel
                        if index < len(binary_message):
                            pixel[n] = pixel[n] & ~1 | int(binary_message[index])
                            index += 1

                    encoded_img.putpixel((col, row), tuple(pixel))

        encoded_img.save(save_path)
        messagebox.showinfo("Success", f"Message encoded and saved as {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode message: {e}")

def decode_message_from_image(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        binary_message = ""
        delimiter = '1111111111111110'
        delimiter_len = len(delimiter)

        for row in range(height):
            for col in range(width):
                pixel = img.getpixel((col, row))
                for n in range(3):
                    binary_message += str(pixel[n] & 1)
                    if binary_message[-delimiter_len:] == delimiter:
                        binary_message = binary_message[:-delimiter_len]  # Remove delimiter
                        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
                        message = ''.join(chr(int(char, 2)) for char in chars)
                        return message

        return ""
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode message: {e}")
        return ""

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_var.set(file_path)

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    return file_path

def encode():
    message = message_text.get("1.0", tk.END).strip()
    image_path = image_path_var.get()
    if not message or not image_path:
        messagebox.showerror("Error", "Please provide both image and message.")
        return
    save_path = save_image()
    if save_path:
        encode_message_in_image(image_path, message, save_path)

def decode():
    image_path = image_path_var.get()
    if not image_path:
        messagebox.showerror("Error", "Please provide an image.")
        return
    message = decode_message_from_image(image_path)
    if message:
        messagebox.showinfo("Decoded Message", message)
    else:
        messagebox.showinfo("Decoded Message", "No hidden message found.")

root = tk.Tk()
root.title("Image Steganography")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

image_path_var = tk.StringVar()

tk.Label(frame, text="Image Path:").grid(row=0, column=0, pady=5)
tk.Entry(frame, textvariable=image_path_var, width=40).grid(row=0, column=1, pady=5)
tk.Button(frame, text="Browse", command=open_image).grid(row=0, column=2, pady=5)

tk.Label(frame, text="Message:").grid(row=1, column=0, pady=5)
message_text = tk.Text(frame, width=40, height=5)
message_text.grid(row=1, column=1, columnspan=2, pady=5)

tk.Button(frame, text="Encode", command=encode).grid(row=2, column=0, pady=5)
tk.Button(frame, text="Decode", command=decode).grid(row=2, column=1, pady=5)
tk.Button(frame, text="Quit", command=root.quit).grid(row=2, column=2, pady=5)

root.mainloop()
