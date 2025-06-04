import openai
import os
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv()

# mini lm nit llm
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
openai.api_key = os.getenv("OPENAI_API_KEY")

def compare_texts(resume_text, job_description):

    #embeddings are used for the compuyter to understand the text better
    #convert to tensor is good for similirarity stuff
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    return {
        "similarity_score": round(similarity_score, 2),
        "match": interpret_score(similarity_score),
    }

def interpret_score(score):
    if score > 0.8:
        return "Strong Match"
    elif score > 0.6:
        return "Moderate Match"
    else:
        return "Weak Match"

def gen_feedback(resume_text, job_description):
    prompt = f"""
    You are a resume analysis assistant. Based on the following resume and job description, provide specific, constructive
    feedback to improve the resume. Be helpful and professional.

    Resume:
    \"\"\"{resume_text}\"\"\"

    Job description:
    \"\"\"{job_description}\"\"\"

    Respond with:
    1. Key mismatches or missing skills
    2. Suggestions for improvement
    3. Tone or formatting tips if relevant
    """
    
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": prompt}],
            temperature = 0.7,
            max_tokens = 300,
            request_timeout = 15
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating feedback: {str(e)}"
