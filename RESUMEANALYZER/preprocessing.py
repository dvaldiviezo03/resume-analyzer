import fitz
import re
import spacy

def extract_pdf_text(pdf_path):
    doc = fitz.opn(pdf_path)
    text = ""
    for page in doc:
        text = text + page.get_text("text") + "\n" # extract text page by page
    return text

def extract_contact_info(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    linkedin_pattern = r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+" #tweak this

    # use re.findall
    #re.findall() seraches a string or text, looks for substrings that match the regex, then returns it

    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text)

    return {
        "Email": email[0] if email else None,
        "Phone": phone[0] if phone else None,
        "Linkedin": linkedin[0] if linkedin else None
    }


# converting text to a structured format (maybe png)
# store resumes with SQL