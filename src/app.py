import tkinter as tk
from tkinter import filedialog, messagebox
import main  # import your backend pipeline


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
            # Get values from UI variables
            use_blue_bg = blue_bg_var.get()
            use_adjust_checked = adjust_var.get()

            # Safeguard: ensure brightness and contrast values are valid
            # Only use these values if adjustment is enabled
            brightness = validate_float(brightness_var.get(), 0.1, 3.0, 1.0) if use_adjust_checked else 1.0
            contrast = validate_float(contrast_var.get(), 0.1, 3.0, 1.0) if use_adjust_checked else 1.0

            # Call the main processing function from the backend script
            main.main(
                file_path,
                use_blue_bg=use_blue_bg,
                use_adjust=use_adjust_checked,
                brightness=brightness,
                contrast=contrast
            )
            messagebox.showinfo("Success", "Passport PDF saved as passport_pics.pdf 🎉")

        except Exception as e:
            # Display any errors that occur during processing
            messagebox.showerror("Error", f"An error occurred: {str(e)} ❌")


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
        if val < min_val or val > max_val:
            return default
        return val
    except (ValueError, tk.TclError):
        # Catch errors if the string cannot be converted to float
        return default


def toggle_adjust():
    """
    Toggles the visibility of the brightness/contrast adjustment frame
    and the guide text based on the state of the 'adjust_var' checkbox.
    """
    if adjust_var.get():
        # If checked, show the adjustment frame and guide label
        adjust_frame.pack(pady=5)
        guide_label.pack(pady=5)
    else:
        # If unchecked, hide them
        adjust_frame.pack_forget()
        guide_label.pack_forget()


# --- Main Application Window Setup ---

# Create the main window
root = tk.Tk()
root.title("Zeb Photo App 📸")
root.geometry("600x500") # Set initial window size
root.resizable(False, False) # Make window not resizable for simplicity

# --- UI Elements ---

# Checkbutton for Blue Background
blue_bg_var = tk.BooleanVar() # Variable to store the state of the checkbox
chk_blue_bg = tk.Checkbutton(root, text="Use Blue Background 🟦", variable=blue_bg_var, font=('Arial', 10))
chk_blue_bg.pack(pady=5)

# Checkbutton to toggle Brightness/Contrast adjustments
adjust_var = tk.BooleanVar() # Variable to store the state of the checkbox
chk_adjust = tk.Checkbutton(root, text="Adjust Brightness/Contrast 💡", variable=adjust_var, command=toggle_adjust, font=('Arial', 10))
chk_adjust.pack(pady=5)

# Frame to contain brightness/contrast input fields
adjust_frame = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, borderwidth=2)

# Brightness input
tk.Label(adjust_frame, text="Brightness (0.1 to 3.0):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=2, sticky='w')
brightness_var = tk.StringVar(value="1.0") # StringVar allows safe validation and initial value
entry_brightness = tk.Entry(adjust_frame, textvariable=brightness_var, width=5, font=('Arial', 10))
entry_brightness.grid(row=0, column=1, padx=5, pady=2)

# Contrast input
tk.Label(adjust_frame, text="Contrast (0.1 to 3.0):", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=2, sticky='w')
contrast_var = tk.StringVar(value="1.0")
entry_contrast = tk.Entry(adjust_frame, textvariable=contrast_var, width=5, font=('Arial', 10))
entry_contrast.grid(row=1, column=1, padx=5, pady=2)

# Guide text for brightness/contrast values
guide_text = (
    "Guide:\n"
    " • Brightness/Contrast values:\n"
    "   - 1.0 = normal (no change)\n"
    "   - Greater than 1.0 = increase\n"
    "   - Less than 1.0 = decrease\n"
    " • Allowed range: 0.1 to 3.0"
)
guide_label = tk.Label(root, text=guide_text, justify="left", wraplength=450, fg="gray25", font=('Arial', 9))


# Select photo button
btn_select_photo = tk.Button(root, text="Select Photo and Generate PDF 🖼️➡️📄", command=select_file,
                           bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), relief=tk.RAISED, bd=3,
                           activebackground='#45a049', activeforeground='white', padx=10, pady=5)
btn_select_photo.pack(pady=20)

# Initialize the state of adjustment frame and guide label
# They should be hidden by default if the checkbox is not checked
toggle_adjust()

# Run the Tkinter event loop
root.mainloop()
