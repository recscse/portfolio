# Information Architecture Audit Report

**Engineer:** Brijesh Yadav  
**Date:** July 2026  
**Focus:** Site Navigation, Project Discovery, Dedicated Case Studies, and Recruiter User Journeys.  

---

## 1. Information Architecture Overview

The portfolio uses a 3-tier navigation hierarchy:
1. **Executive Homepage (`index.html`)**: Acts as a concise 10-second summary answering who Brijesh is (Backend Software Engineer), core tracks (Distributed Systems, Real-Time Infrastructure, AI Systems), experience (ArisGlobal), selected flagship work, writing, open-source highlights, and contact methods.
2. **Project Index & Dedicated Case Studies (`projects.html` & `projects/`)**:
   - `projects.html`: Filterable index across 4 clear categories (*Featured Engineering*, *AI Systems & Research*, *Backend & Platform Engineering*, *Experiments / Utilities*).
   - Dedicated Project Pages (`projects/growth-quantix.html`, `projects/hsci.html`, `projects/aitos.html`, `projects/upstox-auth-pro.html`): High-density engineering case studies detailing system problem, constraints, Mermaid topology, tech stack by role, design decision matrix, and links.
3. **Engineering Writing (`blog/index.html` & `blog/`)**: Deep architectural case studies and design guides with Mermaid flowcharts, sequence diagrams, and Z3 verification state machines.

---

## 2. Recruiter User Journey Verification

1. **Homepage Scan (10s)**: Reads Backend Software Engineer identity, 4+ years experience, and core tech stack (Java, Spring Boot, Python, FastAPI, PostgreSQL, Redis, Z3, ONNX).
2. **Project Inspection**: Clicks project card (e.g. HSCI) → Navigates to `projects/hsci.html` case study detailing system bounds, AST working memory, and 206 passing tests.
3. **Deep Technical Verification**: Clicks "Read Architecture Case Study" → Opens `blog/building-self-verifying-cognitive-architecture-hsci.html` to inspect SMT solver rollbacks and Z3 verification code.
4. **Source Inspection**: Clicks "GitHub Repository" → Reaches source code repository (`github.com/HNDS-HSCI/ai-model`).
