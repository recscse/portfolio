# Full Site Inventory & Audit Report

**Engineer:** Brijesh Yadav  
**Date:** July 2026  
**Scope:** Complete inspection of all 28 HTML pages, CSS files, JavaScript scripts, static JSON data, Markdown audits, and media assets.  

---

## 1. Public Page Inventory & Verification Matrix

| Page Path | Purpose | Title | Meta Description | Status | Inbound/Outbound Routing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `index.html` | Homepage Executive Summary | `Brijesh Yadav — Backend Software Engineer \| Java • Python • Distributed Systems` | `Portfolio of Brijesh Yadav, Backend Software Engineer specializing in Java, Spring Boot, Python, Distributed Systems, Real-Time Market Infrastructure, and AI Architecture.` | **VERIFIED** | Links to `projects.html`, `blog/index.html`, `skills.html`, `projects/*.html`, `blog/*.html` |
| `projects.html` | Project Index (4 Categories) | `Engineering Projects & AI Systems \| Brijesh Yadav` | `Software engineering projects, distributed trading infrastructure, open-source SDKs, and cognitive AI architectures built by Brijesh Yadav.` | **VERIFIED** | Links to dedicated case studies in `projects/*.html`, PyPI, GitHub |
| `blog/index.html` | Engineering Writing Index | `Engineering Writing & System Architecture \| Brijesh Yadav` | `Deep-dive engineering case studies on distributed systems, real-time market pipelines, cognitive AI architectures, and low-latency inference.` | **VERIFIED** | Links to all 7 flagship `.html` articles |
| `skills.html` | Core Technical Stack | `Technical Skills & Stack \| Brijesh Yadav` | `Technical stack inventory across Java, Spring Boot, Python, FastAPI, PostgreSQL, Redis, Kafka, Z3, and ONNX Runtime.` | **VERIFIED** | Links back to `index.html` and `projects.html` |
| `404.html` | 404 Fallback Page | `404 — Page Not Found \| Brijesh Yadav` | `Page not found.` | **VERIFIED** | Links to `index.html`, `projects.html`, `blog/index.html` |

---

## 2. Dedicated Project Pages Inventory (`projects/`)

| Page Path | Title | Category | Architecture Diagram | Primary Links |
| :--- | :--- | :--- | :--- | :--- |
| `projects/growth-quantix.html` | `Growth Quantix — Algorithmic Trading Infrastructure \| Brijesh Yadav` | Active System | Mermaid Topology | Blog Case Study |
| `projects/hsci.html` | `HSCI — Hyper-Symbolic Cognitive Invention \| Brijesh Yadav` | Research / Experimental (v0.1.0-alpha) | Mermaid Component Flow | GitHub Repo & Blog Case Study |
| `projects/aitos.html` | `AITOS — AI-Assisted Trading Architecture \| Brijesh Yadav` | Experimental / WIP | Mermaid Execution Pipeline | Blog Case Study |
| `projects/upstox-auth-pro.html` | `Upstox Auth Pro (Python SDK) \| Brijesh Yadav` | Open Source (PyPI v1.1.3) | Mermaid OAuth2 Sequence | PyPI, GitHub, Docs, Blog |
| `projects/prindox.html` | `Prindox — Document Processing Platform \| Brijesh Yadav` | Live Platform | Mermaid Ingestion Topology | GitHub Repository |

---

## 3. Engineering Blog Articles Inventory (`blog/`)

| Article Path | Headline | Primary Focus | Mermaid Diagram | Structured Data |
| :--- | :--- | :--- | :--- | :--- |
| `blog/building-self-verifying-cognitive-architecture-hsci.html` | Building a Self-Verifying Cognitive Architecture: Inside HSCI | Cognitive Architecture & SMT | 3 Mermaid Flowcharts | `BlogPosting` + `BreadcrumbList` |
| `blog/designing-an-ai-trading-system-without-model-control.html` | Designing an AI Trading System Without Letting the Model Control Everything | Risk Filter Boundaries | 1 Mermaid Flowchart | `BlogPosting` + `BreadcrumbList` |
| `blog/from-pytorch-to-onnx-low-latency-inference-pipeline.html` | From PyTorch to ONNX: Building a Low-Latency Inference Pipeline | Model Inference | 1 Mermaid Flowchart | `BlogPosting` + `BreadcrumbList` |
| `blog/building-production-ready-oauth2-automation-sdk-upstox.html` | Building a Production-Ready OAuth2 Automation SDK for Upstox | OAuth2 & Playwright 2FA | 1 Mermaid Sequence | `BlogPosting` + `BreadcrumbList` |
| `blog/designing-real-time-market-data-pipeline-algorithmic-trading.html` | Designing a Real-Time Market Data Pipeline for an Algorithmic Trading Platform | Redis Pub/Sub Feed | 2 Mermaid Diagrams | `BlogPosting` + `BreadcrumbList` |
| `blog/why-an-ai-system-is-more-than-a-model.html` | Why an AI System is More Than a Model | Software Systems vs Models | 1 Mermaid Flowchart | `BlogPosting` + `BreadcrumbList` |
| `blog/designing-safe-ai-assisted-trading-system.html` | Designing a Safe AI-Assisted Trading System | Safety Gates & Slippage | 1 Mermaid Flowchart | `BlogPosting` + `BreadcrumbList` |

---

## 4. Audit Summary & Conclusion

- **Total HTML Pages Audited:** 28
- **Broken Internal Links:** 0 (Validated via `scripts/check-links.js`)
- **Visual Design Standard:** Glassmorphism UI tokens, theme-aware light/dark mode, 780px readable prose container.
- **Routing Status:** 100% verified. Every homepage CTA opens its exact target page or dedicated project case study.
