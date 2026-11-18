"""Career-profile matching helpers independent of the Streamlit interface."""
from __future__ import annotations
from typing import Mapping, Iterable


def _skill_weights(profile: Mapping) -> dict[str, float]:
    raw = profile.get("skills", {}) or {}
    if isinstance(raw, dict):
        return {str(k).casefold(): max(0.0, float(v)) for k, v in raw.items()}
    return {str(k).casefold(): 1.0 for k in raw}


def match_careers(resume_skills: Iterable[str], career_profiles: Mapping[str, Mapping], top_n: int = 5) -> list[dict]:
    """Rank profiles by weighted overlap with extracted resume skills.

    Scores are profile-compatibility estimates, not hiring probabilities.
    The existing career_predictor remains the primary recommendation engine.
    """
    candidate = {str(s).casefold() for s in (resume_skills or []) if str(s).strip()}
    ranked = []
    for name, profile in (career_profiles or {}).items():
        weights = _skill_weights(profile)
        if not weights:
            continue
        matched = [skill for skill in weights if skill in candidate]
        missing = [skill for skill in weights if skill not in candidate]
        total_weight = sum(weights.values())
        score = (sum(weights[s] for s in matched) / total_weight * 100) if total_weight else 0.0
        ranked.append({"career": name, "category": profile.get("category", "Other"),
                       "match_score": round(score, 1), "matched_skills": matched,
                       "missing_skills": missing, "matched_skill_count": len(matched)})
    ranked.sort(key=lambda x: (x["match_score"], x["matched_skill_count"]), reverse=True)
    return ranked[:max(0, int(top_n))]


def calculate_career_match(resume_skills: Iterable[str], career_profile: Mapping) -> dict:
    """Return one profile's weighted match details."""
    return match_careers(resume_skills, {"Career": career_profile}, top_n=1)[0] if career_profile else {
        "career": "Career", "category": "Other", "match_score": 0.0,
        "matched_skills": [], "missing_skills": [], "matched_skill_count": 0}
