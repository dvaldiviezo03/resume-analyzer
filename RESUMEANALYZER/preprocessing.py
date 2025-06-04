import fitz
import re

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text = text + page.get_text("text") + "\n" # extract text page by page
    return text

def extract_contact_info(text):
    email_pattern = r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+"
    phone_pattern = r"(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(?\d{3}\)?|\d{3})(?:[.\-\s]*)\d{3}(?:[.\-\s]*)\d{4})"
    linkedin_pattern = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+"

    # use re.findall
    #re.findall() seraches a string or text, looks for substrings that match the regex, then returns it

    email = re.findall(email_pattern, text) 
    phone = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text)

    return {
        "Email": email[0] if email else None,
        "Phone": phone[0] if phone else None,
        "LinkedIn": linkedin[0] if linkedin else None
    }
