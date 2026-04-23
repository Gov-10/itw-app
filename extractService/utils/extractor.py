import boto3
import json, os, fitz
from dotenv import load_dotenv
load_dotenv()
s3=boto3.client('s3', region_name=os.getenv("COGNITO_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
bucket_name=os.getenv("S3_BUCKET_NAME")
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
    found = set()
    for skill in SKILL_SET:
        if skill in text:
            found.add(skill)
    return list(found)

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

def extra(file_key:str):
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_bytes = obj["Body"].read()
    tex= extract_normal(file_bytes)
    if len(tex.strip()) < 100:
        te=extract_ocr(file_bytes)
    text_hash = hash_text(text)
    skills = extract_skills(text)
    year = extract_year(text)
    domain = detect_domain(skills)
    return skills, year, domain, text_hash, text[:3000]







