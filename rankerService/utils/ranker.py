from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

def skill_score(resume_skills, job_text):
    job_text = job_text.lower()
    matches = 0
    for skill in resume_skills:
        if skill.lower() in job_text:
            matches += 1
    if len(resume_skills) == 0:
        return 0
    return matches / len(resume_skills)

def semantic_score(resume_text, job_text):
    embeddings = model.encode([resume_text, job_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(score)

def rank_jobs(resume_data, jobs, skills):
    resume_text = resume_data["raw_text"][:2000]
    resume_skills = skills
    ranked_jobs = []
    for job in jobs:
        job_text = job.get("description", "")
        if not job_text:
            continue
        sem_score = semantic_score(resume_text, job_text)
        skl_score = skill_score(resume_skills, job_text)
        final_score = (0.7 * sem_score) + (0.3 * skl_score)
        job["semantic_score"] = round(sem_score, 3)
        job["skill_score"] = round(skl_score, 3)
        job["final_score"] = round(final_score, 3)
        ranked_jobs.append(job)
    ranked_jobs.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked_jobs


