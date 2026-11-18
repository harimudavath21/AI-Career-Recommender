# CareerCompass AI

CareerCompass AI is a resume-based career exploration application. The current project includes a Streamlit application, a career prediction module, a JSON occupation catalogue, and supporting modules for resume processing, skill extraction, career matching, skill-gap analysis, learning-roadmap generation, semantic text embeddings, and optional MySQL connectivity.

> **Integration note:** The supporting modules documented below are standalone reusable helpers. They are not automatically used by the current `app.py` merely because the files exist. The current application workflow continues to use its existing imports and functions. The existing `modules/career_predictor.py` remains the primary career recommendation engine.

## Features and components

- Resume upload and analysis through the Streamlit application.
- Career recommendations from the existing career predictor, including its semantic matching capability when available.
- A JSON-based occupation catalogue at `data/occupation_profiles.json`.
- Supporting resume parsers for PDF, DOCX, and TXT files.
- Rule-based skill extraction for technical and business skills.
- Independent career-profile matching and skill-gap analysis helpers.
- A reusable three-stage learning-roadmap generator.
- An optional Sentence Transformers wrapper using `sentence-transformers/all-MiniLM-L6-v2`.
- Optional MySQL connection helper and starter schema. MySQL is not required for the current JSON-based career catalogue.

## Project structure

```text
CareerCompass-AI/
├── app.py
├── requirements.txt
├── .env                  # Optional local configuration; do not commit secrets
├── data/
│   └── occupation_profiles.json
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   └── schema.sql
├── models/
│   ├── __init__.py
│   └── semantic_model.py
├── modules/
│   ├── __init__.py
│   ├── career_predictor.py
│   ├── job_matcher.py
│   ├── resume_parser.py
│   ├── roadmap_generator.py
│   ├── skill_extractor.py
│   └── skill_gap_analyzer.py
├── scripts/
│   └── import_esco.py
└── utils/
    ├── __init__.py
    └── preprocessing.py
```

## Technology stack

- **Language:** Python
- **Web application:** Streamlit
- **Data processing:** Pandas and NumPy (where used by the application)
- **Semantic NLP:** Sentence Transformers, `all-MiniLM-L6-v2`
- **Resume formats:** PyMuPDF for PDF, `python-docx` for DOCX, and Python text decoding for TXT
- **Career data:** JSON
- **Optional database:** MySQL via `mysql-connector-python`

## Setup

Use the Python environment in which the project dependencies are installed.

```powershell
cd D:\hackathon
python -m pip install -r requirements.txt
```

If `sentence-transformers` is not already included in `requirements.txt`, install it with:

```powershell
python -m pip install sentence-transformers
```

Start the application:

```powershell
python -m streamlit run app.py
```

Then open the local URL printed by Streamlit, normally `http://localhost:8501`.

The first use of the Sentence Transformer model may take longer because the model files may need to be downloaded. Later runs can reuse the local model cache.

## Supporting module reference

### `modules/resume_parser.py`

- `extract_text(source, filename=None)` extracts text from PDF, DOCX, or TXT input.
- `extract_resume_text(source, filename=None)` is an alias for `extract_text`.
- `source` may be a path, bytes, or a file-like/uploaded object.

### `modules/skill_extractor.py`

- `extract_skills(text, extra_skills=None)` returns canonical skill names explicitly found in the text.
- `extract_skills_with_evidence(text)` returns each detected skill with the alias phrase(s) that matched.
- This is rule-based extraction; it should not be interpreted as proof of proficiency.

### `modules/job_matcher.py`

- `match_careers(resume_skills, career_profiles, top_n=5)` ranks career profiles by weighted skill overlap.
- `calculate_career_match(resume_skills, career_profile)` evaluates one profile.
- Scores are profile-compatibility estimates, not hiring probabilities.
- The current `career_predictor.py` remains the primary recommendation engine unless the application is explicitly updated to call these helpers.

### `modules/skill_gap_analyzer.py`

- `analyze_skill_gap(resume_skills, career_profile)` returns matched skills, missing skills, and skill coverage.
- `analyze_multiple_careers(resume_skills, recommendations, career_profiles)` adds gap details to a recommendation list.

### `modules/roadmap_generator.py`

- `generate_roadmap(missing_skills, career_name="Target career", weeks_per_stage=2)` returns a three-stage learning plan.
- Resource suggestions are general hints. Review links and course availability before presenting them as verified recommendations.

### `models/semantic_model.py`

- `get_semantic_encoder(model_name=DEFAULT_MODEL_NAME)` returns a cached encoder wrapper.
- `SemanticEncoder.encode(texts)` generates normalized embeddings.
- `SemanticEncoder.similarities(query, candidates)` calculates cosine similarities.
- `get_model_status()` reports whether the model has been loaded without loading it.
- This helper is separate from `modules/career_predictor.py`; it is not automatically called by `app.py`.

### `utils/preprocessing.py`

- `clean_text(text)` normalizes Unicode and whitespace.
- `normalize_for_matching(text)` creates a lowercase matching representation while retaining useful technical symbols.
- `split_sentences(text)` splits text into sentence/line fragments.

### `database/db_connection.py` and `database/schema.sql`

MySQL support is optional. The current JSON career catalogue does not require MySQL. To use the optional connection helper, install `mysql-connector-python` and configure the following environment variables in a local `.env` file:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=careercompass
```

Do not commit real credentials. The starter schema can be executed in MySQL Workbench or a MySQL client only if you intentionally choose to enable database storage. The existing application is not automatically migrated to MySQL by adding these files.

## Important notes

1. Keep `app.py` and `modules/career_predictor.py` unchanged if you only intend to add the supporting modules described here.
2. Adding a module does not automatically connect it to the Streamlit workflow. Integration requires explicit imports and calls from the application.
3. The occupation catalogue is a local JSON data file. Do not describe it as an official ESCO dataset unless you separately import and verify official ESCO data.
4. Career compatibility scores are estimates based on available resume/profile evidence. They are not guarantees of employment or hiring outcomes.
5. Resume text may contain personal information. Avoid logging or sharing uploaded resumes unnecessarily, and keep credentials out of source control.

## Development checks

Compile the Python source files:

```powershell
python -m compileall app.py database models modules utils
```

Check for zero-byte files:

```powershell
Get-ChildItem -Recurse -File |
Where-Object { $_.Length -eq 0 } |
Select-Object FullName
```

Run the Streamlit application:

```powershell
python -m streamlit run app.py
```
