import pytesseract
from pdf2image import convert_from_path

# ตั้งค่าเส้นทางไปยัง Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # ปรับตามที่ติดตั้ง

def pdf_to_text(pdf_path):
    # แปลง PDF เป็นภาพ
    images = convert_from_path(pdf_path)
    
    # ถอดข้อความจากภาพแต่ละหน้า
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image, lang='tha')  # ใช้ภาษาไทย
    
    return text

# ตัวอย่างการใช้ฟังก์ชัน
if __name__ == "__main__":
    pdf_path = 'pdf_files/sample.pdf'
    extracted_text = pdf_to_text(pdf_path)
    print(extracted_text)
