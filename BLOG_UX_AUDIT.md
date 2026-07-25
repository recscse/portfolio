# Blog UX & Architecture Visualization Audit Report

**Engineer:** Brijesh Yadav  
**Date:** July 2026  
**Scope:** Mermaid.js Integration, Architecture Diagrams, CSS Callout Components, Design Decision Tables, Reading Width Audit.  

---

## 1. Articles Reviewed & Visual Upgrades

| Article File | Mermaid Diagrams Added | Diagram Types | Technical Callouts & Tables Added |
| :--- | :--- | :--- | :--- |
| `building-self-verifying-cognitive-architecture-hsci.html` | 3 Diagrams | Flowchart (Subsystems), Flowchart (NGSS Search), State Diagram (Z3 Verification & Savepoint Rollback) | Status Callout, Limitation Callout, Design Tradeoffs Table, Status Matrix |
| `designing-an-ai-trading-system-without-model-control.html` | 1 Diagram | Flowchart (AI Signal Scoring vs Deterministic Risk & Execution Boundary) | Limitation Disclaimer, Design Tradeoffs Table, Cross Links |
| `from-pytorch-to-onnx-low-latency-inference-pipeline.html` | 1 Diagram | Flowchart (Offline Training Path vs Online ONNX Serving Path) | Decision Callout, Design Tradeoffs Table, Cross Links |
| `building-production-ready-oauth2-automation-sdk-upstox.html` | 1 Diagram | Sequence Diagram (App → SDK → Browser Playwright → Upstox Auth → TOTP 2FA → Token Store) | Status Callout, Design Tradeoffs Table, Cross Links |
| `designing-real-time-market-data-pipeline-algorithmic-trading.html` | 2 Diagrams | Flowchart (Market Data Ingestion Bus), State Diagram (WebSocket Reconnection State Machine) | Tradeoff Callout, Design Tradeoffs Table, Cross Links |
| `why-an-ai-system-is-more-than-a-model.html` | 1 Diagram | Flowchart (Layered Production AI System) | Decision Callout, Design Tradeoffs Table, Cross Links |
| `designing-safe-ai-assisted-trading-system.html` | 1 Diagram | Flowchart (Stock Selection → Risk Gate → Paper Execution) | Research Callout, Design Tradeoffs Table, Cross Links |

---

## 2. Infrastructure & CSS Enhancements

- **Mermaid.js Integration**: Loaded via CDN (`v10`) with dark theme configuration, responsive SVG wrapping, and automatic theme switching support.
- **Reading Width Optimization**: Set `.prose` max-width to `780px` (70–85 characters per line) for optimal long-form reading comfort.
- **Technical Callout Components**:
  - `callout-experimental` (`[STATUS: RESEARCH / EXPERIMENTAL]`)
  - `callout-decision` (`[DECISION NOTE]`)
  - `callout-limitation` (`[LIMITATION NOTE]`)
  - `callout-security` (`[SECURITY NOTE]`)
  - `callout-tradeoff` (`[TRADEOFF NOTE]`)
- **ASCII Diagrams Retained**: Simple `.diagram-content` boxes preserved for concise terminal snippets.
- **Heading Hygiene**: Removed emoji-heavy headings (`🧩`, `🔍`) in favor of clean, professional engineering section titles.
- **Cross-Linking**: Added 2–3 contextually relevant internal engineering article links at the bottom of each flagship post.

---

## 3. Verification & Compliance

- [x] No layout shifts or text overflow on mobile/tablet viewports.
- [x] Light/Dark mode transitions verified for Mermaid containers and text readability.
- [x] No unverified quantitative claims present in any article.
- [x] Assistive text provided around all diagrams for accessibility.
