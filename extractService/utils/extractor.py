import re, hashlib, io
import fitz
from PIL import Image
import pytesseract

SKILL_SET = [
    "python", "java", "c++", "django", "flask", "fastapi",
    "react", "node", "aws", "docker", "kubernetes",
    "postgresql", "mysql", "redis", "mongodb",
    "machine learning", "deep learning", "nlp",
    "html", "css", "javascript"
]


def clean_text(text: str):
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def extract_normal(file_bytes):
    text = ""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    return clean_text(text)


def extract_ocr(file_bytes):
    text = ""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))
        page_text = pytesseract.image_to_string(image)
        text += page_text
    return clean_text(text)


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def extract_skills(text):
    return [skill for skill in SKILL_SET if skill in text]


def detect_domain(skills):
    if any(s in skills for s in ["django", "flask", "fastapi", "node"]):
        return "backend"
    if any(s in skills for s in ["react", "html", "css", "javascript"]):
        return "frontend"
    if any(s in skills for s in ["machine learning", "deep learning", "nlp"]):
        return "ml"
    return "general"


def extract_year(text):
    if "first year" in text or "1st year" in text:
        return 1
    if "second year" in text or "2nd year" in text:
        return 2
    if "third year" in text or "3rd year" in text:
        return 3
    if "fourth year" in text or "4th year" in text:
        return 4
    return None

def extra(file_bytes: bytes):
    text = extract_normal(file_bytes)
    if len(text.strip()) < 100:
        text = extract_ocr(file_bytes)
    text_hash = hash_text(text)
    skills = extract_skills(text)
    year = extract_year(text)
    domain = detect_domain(skills)
    return skills, year, domain, text_hash, text[:3000]
