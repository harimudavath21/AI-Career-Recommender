"""Generate a practical three-stage learning roadmap from a skill gap."""
from __future__ import annotations
from typing import Iterable

RESOURCE_HINTS = {
    "python": "Official Python tutorial and beginner coding exercises",
    "sql": "SQLBolt and the PostgreSQL or MySQL documentation",
    "excel": "Microsoft Excel training and spreadsheet practice projects",
    "power bi": "Microsoft Learn: Power BI learning paths",
    "machine learning": "Scikit-learn user guide and introductory ML exercises",
    "statistics": "Khan Academy statistics and probability lessons",
    "communication": "Practice structured presentations and business writing",
    "recruitment": "HR recruitment process case studies and interview practice",
    "financial accounting": "Accounting fundamentals and worked journal-entry exercises",
    "digital marketing": "Google Skillshop and practical campaign-planning exercises",
}


def generate_roadmap(missing_skills: Iterable[str], career_name: str = "Target career", weeks_per_stage: int = 2) -> list[dict]:
    """Create a generic three-stage plan; customize resources where known."""
    skills = [str(s).strip() for s in (missing_skills or []) if str(s).strip()]
    if not skills:
        return [
            {"stage": "Stage 1 – Strengthen foundations", "duration": f"{weeks_per_stage} weeks", "focus": ["Review core concepts for " + career_name], "deliverable": "A short revision summary"},
            {"stage": "Stage 2 – Apply your skills", "duration": f"{weeks_per_stage} weeks", "focus": ["Complete a practical task related to " + career_name], "deliverable": "One practical exercise or mini-project"},
            {"stage": "Stage 3 – Build your portfolio", "duration": f"{weeks_per_stage} weeks", "focus": ["Document your work and prepare to explain your decisions"], "deliverable": "A portfolio-ready project summary"},
        ]
    chunks = [skills[0::3], skills[1::3], skills[2::3]]
    titles = ["Stage 1 – Learn the fundamentals", "Stage 2 – Practise and apply", "Stage 3 – Build and demonstrate"]
    actions = ["Study the concepts and complete guided exercises", "Solve practical exercises and combine related skills", "Build a small project demonstrating the skills"]
    roadmap = []
    for index, group in enumerate(chunks):
        if not group:
            group = [skills[min(index, len(skills)-1)]]
        resources = [RESOURCE_HINTS.get(skill.casefold(), f"Use a reputable course and official documentation for {skill}") for skill in group]
        roadmap.append({"stage": titles[index], "duration": f"{weeks_per_stage} weeks", "focus": group,
                        "activities": actions[index], "resources": resources,
                        "deliverable": ["Concept notes and exercises", "Completed practice tasks", f"A portfolio mini-project for {career_name}"][index]})
    return roadmap
