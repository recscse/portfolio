"""Single source of truth for the portfolio. Every fact here was checked against the resume, live
GitHub/PyPI data or the public source code (see AUDIT_2026-11.md). Nothing is invented: if a claim is
not evidenced it is not here.
"""

BASE = "https://recscse.github.io/portfolio/"

PERSON = {
    "name": "Brijesh Yadav",
    "title": "Backend Software Engineer",
    "location": "Mysore, India",
    "email": "brijeshyadav30599@gmail.com",
    "github": "https://github.com/recscse",
    "linkedin": "https://www.linkedin.com/in/brijesh-yadav-",
    "x": "https://x.com/_brijeshyadav",  # kept as in the original site; handle not independently verified
    "summary": (
        "I build backend systems in Java / Spring Boot and Python / FastAPI. For the past five years I have "
        "worked on enterprise microservices at ArisGlobal. Outside work I build Growth Quantix, an algorithmic "
        "trading platform, and open-source developer tools."
    ),
    "available": "Available for select freelance and contract projects.",
}

EXPERIENCE = [
    {
        "role": "Software Engineer",
        "company": "ArisGlobal",
        "period": "Oct 2021 - Present",
        "bullets": [
            "Developed and maintained Spring Boot microservices supporting pharmacovigilance workflows used by global pharmaceutical organizations.",
            "Designed and implemented REST APIs and backend services enabling enterprise integrations and workflow automation.",
            "Built high-volume email ingestion and document-processing pipelines capable of processing thousands of inbound emails and attachments.",
            "Integrated OCR and NLP-based pipelines to turn unstructured business data into structured records, improving processing efficiency by approximately 80% with extraction accuracy above 95%.",
            "Optimized PostgreSQL and MySQL queries, improving application performance and scalability.",
            "Investigated production issues, performed root-cause analysis and delivered reliable fixes in Agile teams.",
        ],
    }
]

# Skills as listed on the resume (Kafka removed: it appears only in design docs, never in running code),
# plus Go, evidenced by the codive repository.
SKILL_GROUPS = [
    ("Languages", [("Java", "java"), ("Python", "python"), ("JavaScript", "javascript"), ("Go", "go"), ("SQL", None)]),
    ("Frameworks", [("Spring Boot", "springboot"), ("Hibernate / JPA", "hibernate"), ("FastAPI", "fastapi"), ("React", "react")]),
    ("Data", [("PostgreSQL", "postgresql"), ("MySQL", "mysql"), ("MongoDB", "mongodb"), ("Redis", "redis")]),
    ("Infrastructure & tools", [("Docker", "docker"), ("AWS (S3)", "aws"), ("Git", "git"), ("GitHub Actions", "github"), ("Maven", "maven")]),
]
CONCEPTS = ["REST APIs", "Microservices", "WebSockets", "Event-driven architecture", "Caching", "CI/CD",
            "System design", "Concurrency", "Data structures & algorithms"]

PROJECTS = [
    {
        "slug": "growth-quantix",
        "name": "Growth Quantix",
        "tagline": "Multi-broker algorithmic trading platform",
        "status": "In development",
        "stack": ["Python", "FastAPI", "PostgreSQL", "Redis", "WebSockets", "React"],
        "bullets": [
            "Integrations with Upstox, Dhan and Fyers brokers, including the Upstox Market Feed V3 WebSocket for live prices.",
            "Paper trading, backtesting, portfolio and broker-account management modules, exposed through REST APIs.",
            "AITOS: a stage-gated pipeline that keeps AI signals separate from execution authority. Orders pass deterministic risk checks, including Kelly-fraction position sizing, before they are placed.",
            "Real-time market-data ingestion over binary WebSocket feeds with reconnection and backoff, fanned out to services through Redis Pub/Sub.",
        ],
        "links": [
            ("Source code", "https://github.com/growthquantix/tradingbot"),
            ("Website", "https://growthquantix.com"),
        ],
        "writing": ["designing-real-time-market-data-pipeline-algorithmic-trading", "kelly-criterion-risk-engine",
                    "designing-safe-ai-assisted-trading-system", "designing-an-ai-trading-system-without-model-control"],
    },
    {
        "slug": "upstox-auth-pro",
        "name": "Upstox Auth Pro",
        "tagline": "Open-source SDKs that automate Upstox OAuth2 login",
        "status": "Published",
        "stack": ["Python", "Playwright", "OAuth2", "TOTP", "Java", "GitHub Actions"],
        "bullets": [
            "Python SDK published on PyPI (v1.1.3) that automates the daily Upstox login: browser automation with Playwright and TOTP two-factor codes.",
            "Pluggable token storage, automatic token refresh, retries and diagnostic logging, plus a command-line tool.",
            "A separate Java SDK covers the same authentication workflow for JVM applications.",
        ],
        "links": [
            ("PyPI package", "https://pypi.org/project/upstox-auth-pro/"),
            ("Python SDK", "https://github.com/growthquantix/upstox-auth-pro"),
            ("Java SDK", "https://github.com/growthquantix/upstox-auth-pro-java"),
        ],
        "writing": ["building-production-ready-oauth2-automation-sdk-upstox"],
    },
    {
        "slug": "codive",
        "name": "codive",
        "tagline": "Local-first code-intelligence server for AI coding agents",
        "status": "Active",
        "stack": ["Go", "SQLite", "MCP"],
        "bullets": [
            "Indexes a repository's syntax trees, symbols and call graphs into an embedded SQLite database and serves them to AI coding tools over the Model Context Protocol.",
            "Returns file outlines and focused context instead of whole files. In its own benchmark (one repository, tokens estimated as characters / 4) output was 92.4% smaller across five operations; plain git grep still wins on simple lookups.",
        ],
        "links": [
            ("Source code", "https://github.com/recscse/codive"),
            ("Project site", "https://recscse.github.io/codive/"),
            ("Benchmark report", "https://github.com/recscse/codive/blob/main/docs/BENCHMARK_REPORT.md"),
        ],
        "writing": [],
    },
    {
        "slug": "hsci",
        "name": "HSCI",
        "tagline": "Research prototype: symbolic reasoning with formal verification",
        "status": "Research / alpha",
        "stack": ["Python", "Z3 SMT solver", "SQLite", "PyTorch"],
        "bullets": [
            "Experimental cognitive architecture (v0.1.0-alpha) that checks reasoning steps with the Microsoft Z3 SMT solver instead of trusting model output.",
            "Working memory uses transactional SQLite storage with nested savepoints for rollback.",
            "Runs locally without third-party LLM APIs; has continuous-integration checks. This is a research project, not a production system.",
        ],
        "links": [("Source code", "https://github.com/HNDS-HSCI/ai-model")],
        "writing": ["building-self-verifying-cognitive-architecture-hsci"],
    },
    {
        "slug": "prindox",
        "name": "Prindox",
        "tagline": "Online document printing platform",
        "status": "Live",
        "stack": ["Python", "FastAPI", "PostgreSQL"],
        "bullets": [
            "Backend services and REST APIs for document upload, print-order management and workflow automation.",
            "PostgreSQL schemas and optimized queries for document storage and retrieval; asynchronous background processing for validation and order handling.",
            "Source code is private.",
        ],
        "links": [("Live site", "https://prindox.com")],
        "writing": [],
    },
]

EDUCATION = {
    "school": "Rajkiya Engineering College Sonbhadra",
    "degree": "B.Tech, Computer Science & Engineering",
    "period": "2017 - 2020",
    "cgpa": "7.5 / 10",
    "extra": "Summer internship: Data Driven Computing and Networking, MNNIT Allahabad",
}

# Blog posts kept after verification. Each is backed by public source code or is a generic tutorial.
# Removed (no evidence in public code, or inconsistent with the resume): PyTorch-to-ONNX, S3 + CloudFront
# hosting, Spring Boot email pipeline (also mentioned Kafka), QR-based document handoffs.
KEEP_POSTS = [
    "building-production-ready-oauth2-automation-sdk-upstox",
    "designing-real-time-market-data-pipeline-algorithmic-trading",
    "kelly-criterion-risk-engine",
    "designing-safe-ai-assisted-trading-system",
    "designing-an-ai-trading-system-without-model-control",
    "building-self-verifying-cognitive-architecture-hsci",
    "why-an-ai-system-is-more-than-a-model",
    "market-data-generator",
    "server-sent-events-analytics",
]
REMOVED_POSTS = ["from-pytorch-to-onnx-low-latency-inference-pipeline", "s3-cloudfront-static-hosting",
                 "spring-boot-email-pipeline", "qr-document-handoffs"]
# Links inside kept posts that point to pages which do not exist; their list items are dropped.
DEAD_LINKS = ["https://growthquantix.github.io/upstox-auth-pro/"]
# Text fixes inside kept posts: (slug, old, new). Used where a sentence could not be verified.
POST_EDITS = [
    ("building-production-ready-oauth2-automation-sdk-upstox",
     "Slightly increases authentication execution time by 500ms.",
     "Adds browser start-up time to each authentication run."),
]
