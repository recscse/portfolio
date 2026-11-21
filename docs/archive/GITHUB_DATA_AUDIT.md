# GitHub Data & Language Calculation Audit Report

**Engineer:** Brijesh Yadav  
**Date:** July 2026  
**Focus:** Linguist Byte Aggregation, Static Data Caching, Removal of Trophy Noise, and Skill vs GitHub Distinctions.  

---

## 1. Audit of Previous Implementation

### Flaws Identified
- **Inaccurate Metric**: The old script fetched `GET /users/recscse/repos?per_page=100` and summed `repo.size` by `repo.language`.
- **Why it was wrong**:
  1. `repo.size` represents disk space in kilobytes (including git history, binary objects, images), NOT lines or bytes of code written.
  2. `repo.language` only identifies the single primary language of a repository, ignoring multi-language repositories (e.g. Python repos containing C/C++ or JavaScript).
  3. Third-party trophy widgets (`github-profile-trophy`, `github-readme-streak-stats`) added visual noise without engineering substance.

---

## 2. Corrected Architecture & Implementation

### Build-Time Data Generator (`scripts/fetch-github-data.js`)
- **API Endpoint**: Uses `GET /repos/{owner}/{repo}/languages` which returns exact byte counts per language detected by GitHub Linguist.
- **Aggregation Strategy**: Aggregates Linguist byte counts across public repositories (`recscse`, `growthquantix`, `HNDS-HSCI`), excluding forks and non-source repos.
- **Static Dataset**: Outputs static `data/github.json` to prevent client-side GitHub API rate limiting (60 req/hr unauthenticated limit).
- **Labeling Discipline**: The section is explicitly labeled *"Languages across public GitHub repositories"* to maintain a clear boundary between curated engineering skills and public repository Linguist byte distributions.

---

## 3. Linguist Distribution Snapshot (`data/github.json`)

| Language | Aggregated Bytes | Percentage |
| :--- | :--- | :--- |
| **Python** | 245,100 B | **45.20%** |
| **Java** | 185,400 B | **34.20%** |
| **JavaScript** | 62,400 B | **11.50%** |
| **HTML** | 28,100 B | **5.18%** |
| **CSS** | 15,300 B | **2.82%** |
| **Shell** | 5,890 B | **1.10%** |

*Total Aggregated Linguist Bytes:* **542,190 Bytes (~529 KB)**
