from functools import lru_cache
from openai import OpenAI
import os
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@lru_cache(maxsize=1)

def get_model():
    # mini lm not llm
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compare_texts(resume_text, job_description):
    #embeddings are used for the compuyter to understand the text better
    #convert to tensor is good for similirarity stuff
    model = get_model()
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
    print("Prompt sent to ai...")
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
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": prompt}],
            temperature = 0.7,
            max_tokens = 300,
            timeout = 15
        )
        print("Openai response received...")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in gen_feedback: {str(e)}")
        return f"Error generating feedback: {str(e)}"
