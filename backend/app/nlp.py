import spacy
import re
from collections import defaultdict

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

# Simple skill list for keyword matching (extend this)
COMMON_SKILLS = [
    "python","java","c++","javascript","react","node.js","node","django","flask",
    "fastapi","sql","mongodb","postgres","aws","azure","docker","kubernetes",
    "nlp","spacy","pytorch","tensorflow","pandas","numpy"
]

EDUCATION_KEYWORDS = ["bachelor", "master", "b.sc", "beng", "b.tech", "phd", "msc", "mba", "degree", "hs", "high school"]

PHONE_REGEX = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

def extract_emails(text):
    return list(set(re.findall(EMAIL_REGEX, text)))

def extract_phones(text):
    phones = re.findall(PHONE_REGEX, text)
    # flatten tuples from groups and join to form phone-like strings
    out = set()
    for tup in phones:
        out.add("".join(tup))
    # filter short
    return [p for p in out if len(re.sub(r'\D', '', p)) >= 7]

def extract_skills(text):
    text_low = text.lower()
    found = []
    for s in COMMON_SKILLS:
        if s.lower() in text_low:
            found.append(s)
    return sorted(set(found))

def extract_education(text):
    lines = text.lower().splitlines()
    edu = []
    for line in lines:
        for kw in EDUCATION_KEYWORDS:
            if kw in line:
                edu.append(line.strip())
    return list(set(edu))[:5]

def extract_experience(text):
    # naive: look for years or 'experience' sections
    # return paragraphs mentioning "years" or "experience" or job titles
    exps = []
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    for p in paragraphs:
        if re.search(r'\bexperience\b', p, flags=re.I) or re.search(r'\b([0-9]{1,2}\+?)\s+years\b', p, flags=re.I):
            exps.append(p)
    # fallback: first 2 paragraphs as experience summary
    if not exps:
        exps = paragraphs[:2]
    return exps

def extract_name(doc):
    # Use spaCy: PERSON entity with highest probability or first PERSON
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # fallback: first line if it looks like a name (two words capitalized)
    first_line = doc.text.strip().splitlines()[0]
    if len(first_line.split()) <= 4:
        return first_line
    return None

def parse_resume(text):
    doc = nlp(text)
    name = extract_name(doc)
    emails = extract_emails(text)
    phones = extract_phones(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    # collect entities from spaCy (ORG, GPE, LOC)
    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)

    return {
        "name": name,
        "emails": emails,
        "phones": phones,
        "skills": skills,
        "education": education,
        "experience": experience,
        "entities": {k: list(set(v)) for k, v in entities.items()}
    }
