-- Optional starter schema for CareerCompass AI.
-- The current JSON-based career catalogue does not require this database.
-- Run only if you intentionally decide to use MySQL.

CREATE DATABASE IF NOT EXISTS careercompass
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE careercompass;

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NULL,
    email VARCHAR(254) NULL,
    resume_filename VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_candidates_email (email)
);

CREATE TABLE IF NOT EXISTS resume_analyses (
    analysis_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    candidate_id BIGINT UNSIGNED NULL,
    ats_score DECIMAL(5,2) NULL,
    extracted_skills JSON NULL,
    recommendations JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_analysis_candidate FOREIGN KEY (candidate_id)
      REFERENCES candidates(candidate_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS career_profiles (
    career_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    career_name VARCHAR(180) NOT NULL UNIQUE,
    category VARCHAR(120) NULL,
    skills JSON NOT NULL,
    description TEXT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
      ON UPDATE CURRENT_TIMESTAMP
);
