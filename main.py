import os
import joblib
import pandas as pd
from nltk.corpus import words
from train_model import extract_text_from_pdfs, train_model

# โหลดคำในพจนานุกรม
valid_words = set(words.words())

def check_text_validity(text):
    words_in_text = text.split()
    invalid_words = [word for word in words_in_text if word.lower() not in valid_words]
    return invalid_words

if __name__ == "__main__":
    pdf_folder = 'pdf_files'  # ที่อยู่ของโฟลเดอร์ PDF
    round_number = 1
    previous_accuracy = None  # ตัวแปรสำหรับเก็บความแม่นยำก่อนหน้า

    while True:
        print(f"Training round {round_number}...")
        current_accuracy = train_model(pdf_folder, round_number)

        if previous_accuracy is not None and current_accuracy <= previous_accuracy:
            print("Accuracy did not improve. Consider improving text extraction.")

        previous_accuracy = current_accuracy  # อัปเดตความแม่นยำก่อนหน้า
        round_number += 1

        user_input = input("Do you want to continue training? (yes/no): ")
        if user_input.lower() != 'yes':
            break
