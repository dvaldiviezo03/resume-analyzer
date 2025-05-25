# handles ai processing
from sentence_transformers import SentenceTransformer, util

# load pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compare_texts(resume_text, job_description):

    #embeddings are used for the compuyter to understand the text better
    #convert to tensor is good for similirarity stuff
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)

    similarity_score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    return {
        "similarity_score": similarity_score,
        "match": interpret_score(similarity_score)
    }

def interpret_score(score):
    if score > 0.8:
        return "Strong Match"
    elif score > 0.6:
        return "Moderate Match"
    else:
        return "Weak Match"