import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.corpus import words

# โหลดคำในพจนานุกรม
valid_words = set(words.words())

def check_text_validity(text):
    words_in_text = text.split()
    invalid_words = [word for word in words_in_text if word.lower() not in valid_words]
    return invalid_words

def on_submit():
    input_text = text_input.get("1.0", tk.END).strip()
    invalid_words = check_text_validity(input_text)

    if invalid_words:
        result = f"Invalid words found: {', '.join(invalid_words)}"
    else:
        result = "All words are valid."

    messagebox.showinfo("Check Result", result)

# สร้างหน้าต่าง GUI
window = tk.Tk()
window.title("Text Validity Checker")

label = tk.Label(window, text="Enter your text below:")
label.pack(pady=10)

text_input = scrolledtext.ScrolledText(window, width=40, height=10)
text_input.pack(pady=10)

submit_button = tk.Button(window, text="Check Validity", command=on_submit)
submit_button.pack(pady=10)

# เริ่มต้น loop ของ GUI
window.mainloop()
