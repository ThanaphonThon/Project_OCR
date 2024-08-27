import os
import joblib
import pandas as pd
from pdf2image import convert_from_path
import pytesseract
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import words
from PyPDF2 import PdfReader  # นำเข้า PyPDF2 ที่นี่

# โหลดคำในพจนานุกรม
valid_words = set(words.words())

def extract_text_from_pdfs(pdf_folder):
    texts = []  # รายการข้อความที่ถูกถอดออก
    labels = []  # รายการ label ที่เกี่ยวข้อง
    pages = []  # รายการหน้าที่ถูกอ่าน

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            reader = PdfReader(pdf_path)  # ใช้ PdfReader แทนที่ PdfReader
            for page_number, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    texts.append(text)
                    labels.append('Your label here')  # กำหนด label ตามความเหมาะสม
                    pages.append(page_number + 1)

            # หากไม่พบข้อความ ให้ใช้ OCR
            if not texts:
                images = convert_from_path(pdf_path)
                for page_number, image in enumerate(images):
                    text = pytesseract.image_to_string(image)
                    if text.strip():  # ตรวจสอบข้อความที่ถอดออก
                        texts.append(text)
                        labels.append('Your label here')  # กำหนด label ตามความเหมาะสม
                        pages.append(page_number + 1)

    return texts, labels, pages

def augment_text(text):
    # ฟังก์ชันนี้จะทำการเพิ่มข้อมูล (อาจจะใช้เทคนิคต่างๆ เพื่อสร้างข้อมูลใหม่)
    return [text]  # คืนค่าข้อความเดิมในตัวอย่างนี้

def train_model(pdf_folder, round_number):
    texts, labels, pages = extract_text_from_pdfs(pdf_folder)

    augmented_texts = []
    augmented_labels = []

    for text, label in zip(texts, labels):
        augmented = augment_text(text)
        augmented_texts.extend(augmented)
        augmented_labels.extend([label] * len(augmented))

    texts.extend(augmented_texts)
    labels.extend(augmented_labels)

    # ตรวจสอบและกำจัดข้อความว่างเปล่า
    texts = [text for text in texts if text.strip()]
    labels = [label for text, label in zip(texts, labels) if text.strip()]

    if not texts:
        raise ValueError("No valid text data extracted from the PDFs.")

    vectorizer = TfidfVectorizer(stop_words=None, min_df=1)
    X = vectorizer.fit_transform(texts)

    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Accuracy for round {round_number}: {accuracy * 100:.2f}%")

    model_file = f'models/decision_tree_model_round_{round_number}.pkl'
    vectorizer_file = f'models/vectorizer_round_{round_number}.pkl'
    joblib.dump(model, model_file)
    joblib.dump(vectorizer, vectorizer_file)

    results_df = pd.DataFrame({'Text': texts, 'Label': labels, 'Page': pages})
    results_file = f'results/results_round_{round_number}.csv'
    results_df.to_csv(results_file, index=False)
    print(f"Results saved to {results_file}")

    return accuracy  # ส่งคืนความแม่นยำ
