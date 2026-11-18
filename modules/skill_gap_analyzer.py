"""Skill-gap analysis helpers for recommended career profiles."""
from __future__ import annotations
from typing import Mapping, Iterable


def analyze_skill_gap(resume_skills: Iterable[str], career_profile: Mapping) -> dict:
    """Compare candidate skills with a career profile's required skills."""
    candidate = {str(s).strip().casefold(): str(s).strip() for s in (resume_skills or []) if str(s).strip()}
    raw = career_profile.get("skills", {}) or {}
    required = list(raw.keys()) if isinstance(raw, dict) else list(raw)
    matched, missing = [], []
    for skill in required:
        (matched if str(skill).casefold() in candidate else missing).append(str(skill))
    return {"matched_skills": matched, "missing_skills": missing,
            "required_skill_count": len(required), "matched_skill_count": len(matched),
            "coverage_percent": round(100 * len(matched) / len(required), 1) if required else 0.0}


def analyze_multiple_careers(resume_skills: Iterable[str], recommendations: list[dict], career_profiles: Mapping) -> list[dict]:
    """Attach gap details to recommendation dictionaries without mutating inputs."""
    output = []
    for item in recommendations or []:
        name = item.get("career") or item.get("career_name") or item.get("title")
        profile = career_profiles.get(name, {}) if name else {}
        output.append({**item, **analyze_skill_gap(resume_skills, profile)})
    return output
