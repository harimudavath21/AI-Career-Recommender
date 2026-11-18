
import re

# ============================================================
# 1. CAREER KNOWLEDGE BASE
# ============================================================

CAREER_PROFILES = {

    "Data Analyst": {
        "category": "Data & Analytics",
        "skills": {
            "SQL": 1.0,
            "Python": 0.8,
            "Excel": 0.9,
            "Power BI": 1.0,
            "Statistics": 0.8,
            "Pandas": 0.8,
            "Data Visualization": 1.0
        },
        "projects": [
            "dashboard", "sales analysis", "data analysis",
            "business intelligence", "reporting"
        ],
        "education": [
            "data science", "statistics", "computer science"
        ]
    },

    "Data Scientist": {
        "category": "Data & Analytics",
        "skills": {
            "Python": 1.0,
            "SQL": 0.8,
            "Machine Learning": 1.0,
            "Statistics": 1.0,
            "Pandas": 0.9,
            "NumPy": 0.8,
            "Scikit-learn": 0.9
        },
        "projects": [
            "predictive analytics", "prediction model",
            "data science", "machine learning model",
            "data analysis"
        ],
        "education": [
            "data science", "statistics", "computer science"
        ]
    },

    "Machine Learning Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "Machine Learning": 1.0,
            "Deep Learning": 1.0,
            "TensorFlow": 0.9,
            "PyTorch": 0.9,
            "Scikit-learn": 0.8,
            "SQL": 0.6
        },
        "projects": [
            "model deployment", "machine learning model",
            "neural network", "predictive model"
        ],
        "education": [
            "artificial intelligence", "machine learning",
            "computer science"
        ]
    },

    "AI Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "Machine Learning": 0.9,
            "Deep Learning": 0.9,
            "Generative AI": 1.0,
            "NLP": 0.8,
            "LangChain": 0.8,
            "TensorFlow": 0.7
        },
        "projects": [
            "generative ai", "chatbot", "large language model",
            "ai application", "llm application"
        ],
        "education": [
            "artificial intelligence", "computer science",
            "data science"
        ]
    },

    "NLP Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "NLP": 1.0,
            "Machine Learning": 0.9,
            "Deep Learning": 0.8,
            "TensorFlow": 0.7,
            "PyTorch": 0.7,
            "Generative AI": 0.8
        },
        "projects": [
            "text classification", "sentiment analysis",
            "language processing", "chatbot",
            "text summarization"
        ],
        "education": [
            "natural language processing", "computer science",
            "data science"
        ]
    },

    "Python Developer": {
        "category": "Software Development",
        "skills": {
            "Python": 1.0,
            "SQL": 0.8,
            "Flask": 0.9,
            "Django": 0.9,
            "Git": 0.8,
            "Data Structures": 0.8
        },
        "projects": [
            "web application", "rest api",
            "backend development", "automation",
            "database application"
        ],
        "education": [
            "computer science", "information technology"
        ]
    },

    "Backend Developer": {
        "category": "Software Development",
        "skills": {
            "Python": 0.8,
            "SQL": 0.9,
            "Flask": 0.9,
            "Django": 0.9,
            "Java": 0.8,
            "Git": 0.8
        },
        "projects": [
            "backend development", "rest api",
            "database management", "web services"
        ],
        "education": [
            "computer science", "information technology"
        ]
    },

    "Business Intelligence Analyst": {
        "category": "Data & Analytics",
        "skills": {
            "SQL": 1.0,
            "Power BI": 1.0,
            "Excel": 1.0,
            "Statistics": 0.7,
            "Python": 0.6,
            "Data Visualization": 1.0
        },
        "projects": [
            "business intelligence", "dashboard",
            "business reporting", "sales analysis"
        ],
        "education": [
            "business analytics", "computer science",
            "statistics"
        ]
    },

    "Data Engineer": {
        "category": "Data Engineering",
        "skills": {
            "Python": 0.9,
            "SQL": 1.0,
            "AWS": 0.8,
            "Azure": 0.8,
            "Docker": 0.7,
            "Git": 0.7
        },
        "projects": [
            "data pipeline", "etl pipeline",
            "data warehouse", "data integration"
        ],
        "education": [
            "computer science", "information technology",
            "data engineering"
        ]
    },

    "Computer Vision Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "Computer Vision": 1.0,
            "Deep Learning": 0.9,
            "TensorFlow": 0.8,
            "PyTorch": 0.8,
            "Machine Learning": 0.8
        },
        "projects": [
            "image classification", "object detection",
            "face recognition", "image processing"
        ],
        "education": [
            "computer vision", "artificial intelligence",
            "computer science"
        ]
    },

    "Cloud Engineer": {
        "category": "Cloud & Infrastructure",
        "skills": {
            "AWS": 1.0,
            "Azure": 1.0,
            "Docker": 0.9,
            "Python": 0.7,
            "Git": 0.8,
            "SQL": 0.5
        },
        "projects": [
            "cloud deployment", "cloud infrastructure",
            "application deployment", "devops"
        ],
        "education": [
            "computer science", "information technology"
        ]
    },

    "Frontend Developer": {
        "category": "Software Development",
        "skills": {
            "HTML": 1.0,
            "CSS": 1.0,
            "JavaScript": 1.0,
            "Git": 0.8
        },
        "projects": [
            "frontend development", "web design",
            "responsive website", "user interface"
        ],
        "education": [
            "computer science", "information technology"
        ]
    },

    "Data Quality Analyst": {
        "category": "Data & Analytics",
        "skills": {
            "SQL": 1.0,
            "Excel": 0.8,
            "Python": 0.7,
            "Statistics": 0.8,
            "Data Cleaning": 1.0,
            "Data Validation": 1.0,
            "Data Visualization": 0.6
        },
        "projects": [
            "data quality", "data validation", "data cleansing",
            "data profiling", "duplicate detection"
        ],
        "education": [
            "data science", "statistics", "computer science",
            "information technology"
        ]
    },

    "Analytics Engineer": {
        "category": "Data Engineering",
        "skills": {
            "SQL": 1.0,
            "Python": 0.7,
            "dbt": 1.0,
            "Data Warehousing": 1.0,
            "ETL": 0.9,
            "Git": 0.7,
            "Data Modeling": 0.9
        },
        "projects": [
            "analytics engineering", "data transformation",
            "data warehouse", "dimensional modeling", "dbt project"
        ],
        "education": [
            "data science", "computer science",
            "information technology", "data engineering"
        ]
    },

    "MLOps Engineer": {
        "category": "Artificial Intelligence & Infrastructure",
        "skills": {
            "Python": 1.0,
            "Machine Learning": 0.9,
            "Docker": 0.9,
            "Kubernetes": 0.9,
            "MLflow": 1.0,
            "AWS": 0.8,
            "Git": 0.8,
            "CI/CD": 0.9
        },
        "projects": [
            "mlops", "model deployment", "model monitoring",
            "machine learning pipeline", "continuous integration"
        ],
        "education": [
            "artificial intelligence", "machine learning",
            "computer science", "data science"
        ]
    },

    "Generative AI Engineer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "Generative AI": 1.0,
            "LLMs": 1.0,
            "Prompt Engineering": 0.9,
            "LangChain": 0.9,
            "Vector Databases": 0.8,
            "NLP": 0.8,
            "API Development": 0.7
        },
        "projects": [
            "generative ai", "retrieval augmented generation",
            "rag", "llm application", "ai assistant", "chatbot"
        ],
        "education": [
            "artificial intelligence", "computer science",
            "data science", "information technology"
        ]
    },

    "AI Application Developer": {
        "category": "Artificial Intelligence & Software Development",
        "skills": {
            "Python": 1.0,
            "Generative AI": 0.9,
            "API Development": 0.9,
            "Flask": 0.8,
            "FastAPI": 0.9,
            "SQL": 0.7,
            "Git": 0.7,
            "Prompt Engineering": 0.8
        },
        "projects": [
            "ai application", "ai-powered application",
            "llm application", "chatbot", "rest api"
        ],
        "education": [
            "computer science", "artificial intelligence",
            "information technology", "data science"
        ]
    },

    "NLP Developer": {
        "category": "Artificial Intelligence",
        "skills": {
            "Python": 1.0,
            "NLP": 1.0,
            "Machine Learning": 0.8,
            "Deep Learning": 0.8,
            "NLTK": 0.8,
            "spaCy": 0.8,
            "Transformers": 0.9,
            "SQL": 0.5
        },
        "projects": [
            "text classification", "sentiment analysis",
            "named entity recognition", "text summarization",
            "language processing"
        ],
        "education": [
            "natural language processing", "computer science",
            "artificial intelligence", "data science"
        ]
    },

    "Data Engineer - Cloud": {
        "category": "Data Engineering & Cloud",
        "skills": {
            "Python": 0.9,
            "SQL": 1.0,
            "AWS": 0.9,
            "Azure": 0.9,
            "ETL": 1.0,
            "Apache Spark": 0.9,
            "Data Warehousing": 0.9,
            "Docker": 0.7
        },
        "projects": [
            "cloud data pipeline", "etl pipeline",
            "data lake", "data warehouse",
            "cloud data engineering"
        ],
        "education": [
            "computer science", "information technology",
            "data engineering", "data science"
        ]
    },

    "Business Analyst": {
        "category": "Business & Analytics",
        "skills": {
            "Excel": 1.0,
            "SQL": 0.8,
            "Power BI": 0.8,
            "Statistics": 0.7,
            "Data Visualization": 0.7,
            "Requirements Analysis": 1.0,
            "Communication": 0.8
        },
        "projects": [
            "business analysis", "requirements gathering",
            "business reporting", "process improvement",
            "stakeholder analysis"
        ],
        "education": [
            "business analytics", "business administration",
            "computer science", "information technology"
        ]
    },

    "Python Automation Developer": {
        "category": "Software Development & Automation",
        "skills": {
            "Python": 1.0,
            "SQL": 0.7,
            "Git": 0.7,
            "REST API": 0.8,
            "Selenium": 0.9,
            "Automation": 1.0,
            "Linux": 0.6
        },
        "projects": [
            "process automation", "web automation",
            "test automation", "automated reporting",
            "data scraping"
        ],
        "education": [
            "computer science", "information technology",
            "software engineering"
        ]
    },

    "Big Data Engineer": {
        "category": "Data Engineering",
        "skills": {
            "Python": 0.8,
            "SQL": 0.9,
            "Apache Spark": 1.0,
            "Hadoop": 0.9,
            "Kafka": 0.9,
            "ETL": 1.0,
            "Data Warehousing": 0.8,
            "AWS": 0.7
        },
        "projects": [
            "big data", "real-time data pipeline",
            "stream processing", "hadoop",
            "distributed data processing"
        ],
        "education": [
            "computer science", "data engineering",
            "information technology", "data science"
        ]
    },

}

# ============================================================
# 2. SKILL NORMALIZATION AND ALIASES
# ============================================================

import json
from pathlib import Path


SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "sql": ["sql", "structured query language"],
    "power bi": ["power bi", "powerbi"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "generative ai": ["generative ai", "gen ai", "genai"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision", "cv"],
    "scikit-learn": ["scikit learn", "scikit-learn", "sklearn"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "tf"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "node.js": ["node.js", "nodejs", "node js"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "api development": ["api development", "api design"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud platform", "google cloud"],
    "excel": ["excel", "microsoft excel", "ms excel"],
    "powerpoint": ["powerpoint", "microsoft powerpoint"],
    "data visualization": ["data visualization", "data visualisation"],
    "data analysis": ["data analysis", "data analytics"],
    "data structures": ["data structures", "data structure"],
    "object-oriented programming": ["object oriented programming", "oop", "o o p"],
    "natural language toolkit": ["nltk", "natural language toolkit"],
    "spacy": ["spacy", "spaCy"],
    "llms": ["llm", "llms", "large language model", "large language models"],
    "prompt engineering": ["prompt engineering", "prompt design"],
    "vector databases": ["vector database", "vector databases", "vector store", "vector stores"],
    "apache spark": ["apache spark", "spark"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous delivery", "continuous deployment"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres"],
    "git": ["git", "github", "gitlab"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "power bi": ["power bi", "powerbi"],
}


def normalize_text(text):
    """Normalize text for robust, case-insensitive phrase matching."""
    if not isinstance(text, str):
        return ""
    text = text.lower().replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", text).strip()


def _normalize_skill(value):
    """Normalize a skill label while retaining meaningful symbols such as C++."""
    value = normalize_text(str(value))
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9+#./-]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


_ALIAS_TO_CANONICAL = {}
for _canonical, _aliases in SKILL_ALIASES.items():
    _ALIAS_TO_CANONICAL[_normalize_skill(_canonical)] = _canonical
    for _alias in _aliases:
        _ALIAS_TO_CANONICAL[_normalize_skill(_alias)] = _canonical


def _phrase_in_text(phrase, text):
    """Match a phrase without accidental partial-word matches."""
    phrase = normalize_text(phrase)
    if not phrase:
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _canonical_skill(value):
    normalized = _normalize_skill(value)
    return _ALIAS_TO_CANONICAL.get(normalized, normalized)


def _get_resume_skill_set(resume_text, extracted_skills):
    """
    Combine supplied skill-extractor output with skill phrases explicitly
    present in resume text. This improves recall without inventing skills.
    """
    found = set()

    if isinstance(extracted_skills, (list, tuple, set)):
        for skill in extracted_skills:
            if skill:
                found.add(_canonical_skill(skill))

    normalized_resume = normalize_text(resume_text)

    # Detect known aliases in the resume itself in case the upstream extractor
    # misses a spelling variant. A skill is added only if its phrase is present.
    for canonical, aliases in SKILL_ALIASES.items():
        phrases = [canonical] + list(aliases)
        if any(_phrase_in_text(alias, normalized_resume) for alias in phrases):
            found.add(_canonical_skill(canonical))

    return found


# ============================================================
# 3. GLOBAL OCCUPATION CATALOGUE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ESCO_PROFILE_FILE = PROJECT_ROOT / "data" / "occupation_profiles.json"


def load_global_occupation_profiles():
    """
    Load profiles from data/occupation_profiles.json.

    The file may contain assistant-created starter profiles or profiles
    generated from an official occupational dataset. Its own metadata is
    retained; custom starter data is not mislabeled as official ESCO data.
    """
    if not ESCO_PROFILE_FILE.exists():
        return {}

    try:
        with ESCO_PROFILE_FILE.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        profiles = payload.get("occupations", {})
        if not isinstance(profiles, dict):
            return {}

        dataset_source = str(payload.get("dataset_source", "")).lower()
        declared_esco = "esco" in dataset_source and "not official" not in dataset_source

        cleaned = {}
        for title, profile in profiles.items():
            if not isinstance(profile, dict):
                continue

            raw_skills = profile.get("skills", {})
            if not isinstance(raw_skills, dict) or not raw_skills:
                continue

            skills = {}
            for skill_name, weight in raw_skills.items():
                try:
                    weight = float(weight)
                except (TypeError, ValueError):
                    weight = 0.0
                if weight > 0:
                    skills[str(skill_name).strip()] = min(weight, 1.0)

            if not skills:
                continue

            cleaned[str(title)] = {
                "category": profile.get("category", "Other Occupations"),
                "skills": skills,
                "projects": profile.get("projects", []) or [],
                "education": profile.get("education", []) or [],
                "description": profile.get("description", ""),
                "source": "ESCO" if declared_esco else "Custom",
                "uri": profile.get("uri", ""),
                "alternate_labels": profile.get("alternate_labels", []) or [],
            }

        return cleaned

    except (OSError, json.JSONDecodeError, TypeError, AttributeError):
        return {}


# Curated profiles take precedence where occupation names overlap.
ESCO_CAREER_PROFILES = load_global_occupation_profiles()
for _occupation_name, _occupation_profile in ESCO_CAREER_PROFILES.items():
    CAREER_PROFILES.setdefault(_occupation_name, _occupation_profile)


# ============================================================
# 4. CAREER PREDICTION ENGINE
# ============================================================

# Semantic matching is optional: if the package/model is unavailable, the
# predictor continues to work with exact and alias-based matching.
_SEMANTIC_MODEL = None
_SEMANTIC_MODEL_ERROR = None
_SEMANTIC_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_SEMANTIC_THRESHOLD = 0.62


def _get_semantic_model():
    """Load the sentence-transformer only when prediction first needs it."""
    global _SEMANTIC_MODEL, _SEMANTIC_MODEL_ERROR
    if _SEMANTIC_MODEL is not None:
        return _SEMANTIC_MODEL
    if _SEMANTIC_MODEL_ERROR is not None:
        return None
    try:
        from sentence_transformers import SentenceTransformer
        _SEMANTIC_MODEL = SentenceTransformer(_SEMANTIC_MODEL_NAME)
        return _SEMANTIC_MODEL
    except Exception as exc:  # model download/cache/dependency errors
        _SEMANTIC_MODEL_ERROR = str(exc)
        return None


def _resume_sentences(resume_text):
    """Split resume text into meaningful chunks for semantic comparison."""
    if not isinstance(resume_text, str):
        return []
    chunks = re.split(r"[\n\r•|;]+|(?<=[.!?])\s+", resume_text)
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) >= 12]


def _semantic_skill_matches(resume_text, skill_names, threshold=None):
    """Return skill-to-resume semantic matches above a conservative threshold."""
    threshold = _SEMANTIC_THRESHOLD if threshold is None else float(threshold)
    sentences = _resume_sentences(resume_text)
    unique_skills = list(dict.fromkeys(str(skill) for skill in skill_names if skill))
    if not sentences or not unique_skills:
        return {}

    model = _get_semantic_model()
    if model is None:
        return {}

    try:
        import numpy as np
        skill_embeddings = model.encode(
            [f"Professional skill: {skill}" for skill in unique_skills],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        sentence_embeddings = model.encode(
            sentences,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        similarities = np.matmul(skill_embeddings, sentence_embeddings.T)
        matches = {}
        for index, skill in enumerate(unique_skills):
            best_index = int(np.argmax(similarities[index]))
            score = float(similarities[index][best_index])
            if score >= threshold:
                matches[skill] = {
                    "similarity": round(score, 3),
                    "evidence": sentences[best_index],
                }
        return matches
    except Exception:
        # Semantic matching must never prevent the resume analysis from running.
        return {}


def get_semantic_matching_status():
    """Expose whether semantic matching loaded, failed, or is not yet initialized."""
    if _SEMANTIC_MODEL is not None:
        return {"available": True, "model": _SEMANTIC_MODEL_NAME, "error": None}
    if _SEMANTIC_MODEL_ERROR is not None:
        return {"available": False, "model": _SEMANTIC_MODEL_NAME,
                "error": _SEMANTIC_MODEL_ERROR}
    return {"available": None, "model": _SEMANTIC_MODEL_NAME, "error": None}


def predict_careers(resume_text, extracted_skills, top_n=5):
    """Rank occupations using explicit and semantic resume evidence.

    Scores are compatibility estimates, not hiring probabilities. Semantic
    matches are accepted only above a conservative similarity threshold and
    are returned separately so the UI can distinguish evidence types.
    """
    text = normalize_text(resume_text)
    candidate_skills = _get_resume_skill_set(resume_text, extracted_skills)

    # Build one list of required skills across the catalogue, then compare
    # those skills with resume sentences in a single embedding operation.
    all_required_skills = []
    for profile in CAREER_PROFILES.values():
        required = profile.get("skills", {})
        if isinstance(required, dict):
            all_required_skills.extend(required.keys())
    semantic_matches = _semantic_skill_matches(resume_text, all_required_skills)

    results = []
    for career, profile in CAREER_PROFILES.items():
        required_skills = profile.get("skills", {})
        if not isinstance(required_skills, dict) or not required_skills:
            continue

        matched_skills = []
        semantic_matched_skills = []
        missing_skills = []
        total_weight = 0.0
        matched_weight = 0.0

        for skill_name, raw_weight in required_skills.items():
            try:
                weight = float(raw_weight)
            except (TypeError, ValueError):
                weight = 0.0
            if weight <= 0:
                continue

            total_weight += weight
            canonical = _canonical_skill(skill_name)
            explicit_match = (
                canonical in candidate_skills
                or _phrase_in_text(skill_name, text)
                or any(_phrase_in_text(alias, text)
                       for alias in SKILL_ALIASES.get(canonical, []))
            )
            semantic_match = skill_name in semantic_matches

            if explicit_match:
                matched_skills.append(skill_name)
                matched_weight += weight
            elif semantic_match:
                # Semantic-only evidence contributes partially, not as a full
                # explicit skill match, to reduce overconfident rankings.
                semantic_matched_skills.append(skill_name)
                matched_weight += weight * 0.65
            else:
                missing_skills.append(skill_name)

        skill_score = matched_weight / total_weight * 100 if total_weight else 0.0
        project_phrases = profile.get("projects", []) or []
        project_matches = [phrase for phrase in project_phrases
                           if phrase and _phrase_in_text(phrase, text)]
        project_score = min(len(project_matches) / 2.0, 1.0) * 100

        education_phrases = profile.get("education", []) or []
        education_matches = [phrase for phrase in education_phrases
                             if phrase and _phrase_in_text(phrase, text)]
        education_score = min(len(education_matches), 1) * 100

        weighted_components = [(skill_score, 0.75)]
        if project_phrases:
            weighted_components.append((project_score, 0.15))
        if education_phrases:
            weighted_components.append((education_score, 0.10))
        total_component_weight = sum(weight for _, weight in weighted_components)
        final_score = (sum(score * weight for score, weight in weighted_components)
                       / total_component_weight if total_component_weight else 0.0)

        if not matched_skills and not semantic_matched_skills and not project_matches:
            continue

        results.append({
            "career": career,
            "category": profile.get("category", "Other Occupations"),
            "compatibility": round(final_score, 1),
            "skill_score": round(skill_score, 1),
            "project_score": round(project_score, 1),
            "education_score": round(education_score, 1),
            "matched_skills": sorted(matched_skills + semantic_matched_skills),
            "explicit_matched_skills": sorted(matched_skills),
            "semantic_matched_skills": sorted(semantic_matched_skills),
            "semantic_evidence": {
                skill: semantic_matches[skill] for skill in semantic_matched_skills
            },
            "missing_skills": sorted(missing_skills),
            "project_evidence": project_matches,
            "education_evidence": education_matches,
            "matched_skill_count": len(matched_skills) + len(semantic_matched_skills),
            "source": profile.get("source", "Curated"),
        })

    results.sort(key=lambda item: (
        item["compatibility"], item["matched_skill_count"],
        len(item["project_evidence"])), reverse=True)

    if top_n is None:
        return results
    try:
        limit = max(0, int(top_n))
    except (TypeError, ValueError):
        limit = 5
    return results[:limit]


# ============================================================
# 5. CAREER CATALOGUE HELPERS
# ============================================================

def get_career_details(career_name):
    return CAREER_PROFILES.get(career_name)


def get_all_careers():
    return list(CAREER_PROFILES.keys())


def get_occupation_catalogue_stats():
    """Return the number and source of profiles currently loaded."""
    return {
        "curated_profiles": len([
            profile for profile in CAREER_PROFILES.values()
            if profile.get("source") not in {"ESCO", "Custom"}
        ]),
        "custom_profiles": len([
            profile for profile in ESCO_CAREER_PROFILES.values()
            if profile.get("source") == "Custom"
        ]),
        "esco_profiles": len([
            profile for profile in ESCO_CAREER_PROFILES.values()
            if profile.get("source") == "ESCO"
        ]),
        "total_profiles": len(CAREER_PROFILES),
        "source_file": str(ESCO_PROFILE_FILE),
        "loaded": ESCO_PROFILE_FILE.exists(),
    }
