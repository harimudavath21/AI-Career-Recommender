"""Rule-based skill extraction for technical and business resumes."""
from __future__ import annotations
import re

SKILL_ALIASES = {
    "Python": ["python", "python programming"], "SQL": ["sql", "structured query language"],
    "Excel": ["excel", "microsoft excel", "ms excel"], "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"], "Statistics": ["statistics", "statistical analysis"],
    "Machine Learning": ["machine learning", "ml", "predictive modeling"],
    "Deep Learning": ["deep learning", "dl", "neural networks"],
    "NLP": ["nlp", "natural language processing"], "Generative AI": ["generative ai", "genai", "gen ai"],
    "TensorFlow": ["tensorflow"], "PyTorch": ["pytorch"], "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"], "NumPy": ["numpy"], "Data Visualization": ["data visualization", "data visualisation"],
    "MySQL": ["mysql"], "PostgreSQL": ["postgresql", "postgres"], "Git": ["git", "github"],
    "AWS": ["aws", "amazon web services"], "Azure": ["azure", "microsoft azure"], "GCP": ["gcp", "google cloud platform"],
    "Java": ["java programming", "java"], "JavaScript": ["javascript", "js"], "TypeScript": ["typescript"],
    "C++": ["c++"], "C#": ["c#", "c sharp"], "HTML": ["html"], "CSS": ["css"],
    "Flask": ["flask"], "Django": ["django"], "Streamlit": ["streamlit"], "REST APIs": ["rest api", "restful api", "apis"],
    "Recruitment": ["recruitment", "talent acquisition", "candidate sourcing"],
    "Interview Scheduling": ["interview scheduling", "interview coordination"],
    "Onboarding": ["onboarding", "new hire orientation"], "Employee Engagement": ["employee engagement"],
    "HR Operations": ["hr operations", "human resources operations"], "Payroll": ["payroll", "salary processing"],
    "Financial Accounting": ["financial accounting", "accounting"], "Bookkeeping": ["bookkeeping", "ledger maintenance"],
    "Accounts Payable": ["accounts payable", "payables"], "Accounts Receivable": ["accounts receivable", "receivables"],
    "Budgeting": ["budgeting", "budget preparation"], "Financial Reporting": ["financial reporting", "financial statements"],
    "Bank Reconciliation": ["bank reconciliation", "bank reconciliations"], "Taxation": ["taxation", "tax accounting"],
    "Digital Marketing": ["digital marketing", "online marketing"], "SEO": ["seo", "search engine optimization", "search engine optimisation"],
    "Social Media Marketing": ["social media marketing", "social media management"],
    "Content Writing": ["content writing", "copywriting", "content creation"],
    "Market Research": ["market research", "marketing research"], "Competitor Analysis": ["competitor analysis", "competitive analysis"],
    "Customer Segmentation": ["customer segmentation", "market segmentation"], "Campaign Planning": ["campaign planning", "marketing campaigns"],
    "Communication": ["communication", "written communication", "verbal communication"],
    "Leadership": ["leadership", "team leadership"], "Project Management": ["project management", "project coordination"],
    "Problem Solving": ["problem solving", "problem-solving"], "Microsoft Office": ["microsoft office", "ms office"],
}


def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def extract_skills(text: str, extra_skills: list[str] | None = None) -> list[str]:
    """Return canonical skills explicitly mentioned in resume text."""
    if not isinstance(text, str) or not text.strip():
        return []
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_phrase(text, alias) for alias in aliases):
            found.append(canonical)
    if extra_skills:
        lower_found = {x.lower() for x in found}
        for skill in extra_skills:
            if isinstance(skill, str) and skill.strip() and skill.lower() not in lower_found:
                found.append(skill.strip())
                lower_found.add(skill.lower())
    return sorted(found, key=str.casefold)


def extract_skills_with_evidence(text: str) -> dict[str, list[str]]:
    """Return canonical skill -> matched alias evidence for transparency."""
    result = {}
    for canonical, aliases in SKILL_ALIASES.items():
        hits = [alias for alias in aliases if _contains_phrase(text or "", alias)]
        if hits:
            result[canonical] = hits
    return result
