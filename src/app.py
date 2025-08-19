import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import main  # import your backend pipeline


def resource_path(filename):
    """Get absolute path to resource, works for dev and for PyInstaller exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def validate_float(value_str, min_val, max_val, default):
    """
    Safeguard function to validate numeric input from StringVar.
    Converts string to float and checks if it's within the allowed range.

    Args:
        value_str (str): The string value from a Tkinter StringVar.
        min_val (float): Minimum allowed float value.
        max_val (float): Maximum allowed float value.
        default (float): Default value to return if validation fails.

    Returns:
        float: The validated float value or the default value.
    """
    try:
        val = float(value_str)
        if min_val <= val <= max_val:
            return val
    except (ValueError, tk.TclError):
        pass
    return default


def toggle_adjust():
    """
    Toggles the visibility of the brightness/contrast adjustment frame
    and the guide text based on the state of the 'adjust_var' checkbox.
    """
    if adjust_var.get():
        adjust_frame.pack(pady=5)
        guide_label.pack(pady=10)
    else:
        adjust_frame.pack_forget()
        guide_label.pack_forget()


def select_file():
    """
    Opens a file dialog for image selection, processes the image using main.py,
    and displays success or error messages.
    """
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        try:
            use_blue_bg = blue_bg_var.get()
            use_adjust_checked = adjust_var.get()
            one_picture = one_picture_var.get()

            brightness = validate_float(brightness_var.get(), 0.1, 3.0, 1.0) if use_adjust_checked else 1.0
            contrast = validate_float(contrast_var.get(), 0.1, 3.0, 1.0) if use_adjust_checked else 1.0

            saved_path = main.main(
                file_path,
                use_blue_bg=use_blue_bg,
                use_adjust=use_adjust_checked,
                brightness=brightness,
                contrast=contrast,
                one_picture=one_picture    
            )
            messagebox.showinfo("Success", f"File saved to:\n{saved_path} ✅")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)} ❌")


# --- Main Application Window Setup ---

root = tk.Tk()
root.title("Zeb Photo App 📸")
root.geometry("600x500")
root.resizable(False, False)

bg_path = resource_path("bg.jpeg")
icon_path = resource_path("icon.ico")

# Load and set background image
bg_image = Image.open(bg_path).resize((600, 500))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set application icon
root.iconbitmap(icon_path)

# --- UI Elements ---

# Button to select photo and generate PDF
btn_select_photo = tk.Button(root, text="Select Photo and Generate 9 Passport Pictures", command=select_file,
                             bg="#008CFF", fg='white', font=('Arial', 12, 'bold'), relief=tk.RAISED, bd=3,
                             activebackground='#008CFF', activeforeground='white', padx=10, pady=5)
btn_select_photo.pack(pady=20)


blue_bg_var = tk.BooleanVar()
chk_blue_bg = tk.Checkbutton(root, text="Use Blue Background", variable=blue_bg_var, font=('Arial', 10))
chk_blue_bg.pack(pady=5)

one_picture_var = tk.BooleanVar()
chk_one_picture = tk.Checkbutton(root, text="Generate Single Picture", variable=one_picture_var, font=('Arial', 10))
chk_one_picture.pack(pady=5)

adjust_var = tk.BooleanVar()
chk_adjust = tk.Checkbutton(root, text="Adjust Brightness/Contrast", variable=adjust_var, command=toggle_adjust, font=('Arial', 10))
chk_adjust.pack(pady=5)

# Adjustment frame for brightness and contrast
adjust_frame = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)

# Brightness input
tk.Label(adjust_frame, text="Brightness (0.1 to 3.0):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=2, sticky='w')
brightness_var = tk.StringVar(value="1.0")
entry_brightness = tk.Entry(adjust_frame, textvariable=brightness_var, width=5, font=('Arial', 10))
entry_brightness.grid(row=0, column=1, padx=5, pady=2)

# Contrast input
tk.Label(adjust_frame, text="Contrast (0.1 to 3.0):", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=2, sticky='w')
contrast_var = tk.StringVar(value="1.0")
entry_contrast = tk.Entry(adjust_frame, textvariable=contrast_var, width=5, font=('Arial', 10))
entry_contrast.grid(row=1, column=1, padx=5, pady=2)

# Guide label for brightness and contrast usage
guide_text = (
    "Guide:\n"
    " • Brightness/Contrast values:\n"
    "   - 1.0 = normal (no change)\n"
    "   - Greater than 1.0 = increase\n"
    "   - Less than 1.0 = decrease\n"
    " • Allowed range: 0.1 to 3.0"
)
guide_label = tk.Label(root, text=guide_text, justify="left", wraplength=450, fg="gray25", font=('Arial', 10))

# Initialize the adjustment frame and guide label visibility
toggle_adjust()


# Run the application
root.mainloop()
