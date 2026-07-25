# SEO & Structured Data Audit Report

**Engineer:** Brijesh Yadav  
**Date:** July 2026  
**Scope:** Search Engine Optimization, Structured Data (JSON-LD), OpenGraph Tags, Twitter Cards, Sitemap, and Metadata Validation.  

---

## 1. Audit Summary & Compliance

Every page in the portfolio adheres to SEO best practices:
- **Title Tags**: Unique, descriptive, non-repetitive browser titles across all pages.
- **Meta Descriptions**: Unique summary descriptions (120–160 characters) avoiding keyword stuffing.
- **OpenGraph & Twitter Cards**: `og:title`, `og:description`, `og:type`, `twitter:card`, `twitter:title`, `twitter:description`.
- **Heading Hierarchy**: Single `<h1>` tag per page followed by logical `<h2>` and `<h3>` tags.
- **Sitemap & Robots**: Standard `sitemap.xml` and `robots.txt` generated.

---

## 2. JSON-LD Structured Data Schema

### 1. Homepage (`index.html`) — `Person` Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Brijesh Yadav",
  "jobTitle": "Backend Software Engineer",
  "worksFor": {
    "@type": "Organization",
    "name": "ArisGlobal"
  },
  "url": "https://recscse.github.io",
  "sameAs": [
    "https://github.com/recscse",
    "https://linkedin.com/in/brijesh-yadav-037302196"
  ]
}
```

### 2. Engineering Articles — `BlogPosting` & `BreadcrumbList` Schema
Every flagship engineering article includes validated JSON-LD schema matching visible breadcrumbs:
- `Home` → `Writing` → `[Category]` → `[Article Title]`

---

## 3. Page Title & Meta Description Verification Matrix

| Page | Title Tag | Meta Description |
| :--- | :--- | :--- |
| `index.html` | Brijesh Yadav — Backend Software Engineer \| Java • Python • Distributed Systems | Portfolio of Brijesh Yadav, Backend Software Engineer specializing in Java, Spring Boot, Python, Distributed Systems, Real-Time Market Infrastructure, and AI Architecture. |
| `projects.html` | Engineering Projects & AI Systems \| Brijesh Yadav | Software engineering projects, distributed trading infrastructure, open-source SDKs, and cognitive AI architectures built by Brijesh Yadav. |
| `blog/index.html` | Engineering Writing & System Architecture \| Brijesh Yadav | Deep-dive engineering case studies on distributed systems, real-time market pipelines, cognitive AI architectures, and low-latency inference. |
| `projects/hsci.html` | HSCI — Hyper-Symbolic Cognitive Invention \| Brijesh Yadav | Project Case Study: Hyper-Symbolic Cognitive Invention (HSCI) v0.1.0-alpha, an experimental self-verifying cognitive architecture coupling neural search heuristics with Microsoft Z3 SMT logic solvers. |
| `projects/growth-quantix.html` | Growth Quantix — Algorithmic Trading Infrastructure \| Brijesh Yadav | Project Case Study: Growth Quantix, an algorithmic trading and real-time market data platform featuring multi-broker APIs, Redis Pub/Sub feed ingestion, and paper trading parity. |
| `projects/upstox-auth-pro.html` | Upstox Auth Pro (Python SDK) \| Brijesh Yadav | Project Case Study: Published open-source Python SDK (upstox-auth-pro v1.1.3) automating Upstox OAuth2 login, Playwright TOTP 2FA, token storage, and diagnostic retries. |
