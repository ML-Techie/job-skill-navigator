# Job & Skill Navigator — Product Requirements Document

> **Status:** v1 Draft · **Owner:** Tejaswi Pandavula · **Last updated:** 2026-04-30

> **Changelog v1.1:** Replaced PMKVY-centric course strategy with a tiered multi-source catalog (Coursera, Udemy, NPTEL, SWAYAM, YouTube, NCERT, PMKVY). Added Section 9 (Data Sourcing Strategy) and the unified `Course` schema. Updated success metrics, risks, and out-of-scope.

---

## 1. Problem Statement

Career switchers and early-career professionals in India face three compounding pains: (1) they don't know which roles realistically fit their background, (2) they can't identify the *specific* skills missing for a target role, and (3) they waste months on generic courses that don't map to actual hiring requirements. Existing tools (LinkedIn Learning, Naukri, generic chatbots) are either too broad, not India-aware, or fail to connect skill gaps to concrete, recognized learning resources spanning both global platforms (Coursera, Udemy) and Indian options (NPTEL, NCERT, SWAYAM).

**Solution:** An agentic AI career navigator that ingests a user's profile, retrieves real-time Indian job market data and a curated multi-source learning catalog, and produces a personalized career roadmap — with role matches, skill-gap analysis, an India-aware learning path, a tailored resume, and mock interview questions.

---

## 2. Target Users

### Persona 1: "Career-Switcher Meera"
- **Profile:** 26, Mechanical Engineer at a manufacturing firm in Pune, ₹7L/yr
- **Goal:** Switch to Data Analytics within 9 months
- **Frustration:** "I've watched 30 YouTube tutorials and finished 2 Coursera courses. I still don't know if I'm ready to apply, or what's missing."
- **What she needs:** A clear "you are 65% there; here are the 3 missing skills, here are courses ranked by quality + cost, here's how to phrase your manufacturing experience on a Data resume."

### Persona 2: "Fresher Arjun"
- **Profile:** 22, BTech CS final year from a Tier-2 college in Hyderabad
- **Goal:** Land first job — confused between Backend, Data, and ML roles
- **Frustration:** "Everyone says 'do projects.' Which projects? For which role? My placement cell only knows about Infosys and TCS."
- **What he needs:** Role recommendations based on his actual project history + 12-week plan blending NPTEL fundamentals with Coursera/Udemy specializations.

### Persona 3: "Skilling-Up Sunita"
- **Profile:** 32, BCom graduate, 4 years in BPO ops in Indore, wants to upskill on a budget
- **Goal:** Move into a tech-adjacent role (analyst, junior PM, ops automation)
- **Frustration:** "I can't afford ₹50K bootcamps. I need free or low-cost paths that employers actually respect."
- **What she needs:** Free-first learning paths anchored in NPTEL/SWAYAM, with select paid Coursera/Udemy courses only when they significantly boost employability.

> 💡 **Design note:** Three personas spanning *fresher → switcher → upskiller* covers most of India's job-seeker market. Each persona stresses a different dimension of the system: matching, resume tailoring, and cost-aware path generation.

---

## 3. User Journey

1. **Onboarding (30s)** — User uploads resume (PDF) OR fills a 5-field form (education, current role, years of exp, key skills, target goal).
2. **Clarification (15s)** — System asks 1-2 follow-up questions if profile is ambiguous (e.g., "You mentioned Python — is that for data analysis, web dev, or scripting?").
3. **Role Matching (10s)** — System returns top 3 role matches, each with: match score, why it fits, salary range (Indian market), example companies hiring.
4. **Deep Dive (user picks 1 role)** — User clicks one role to expand.
5. **Skill Gap Analysis (10s)** — System shows: skills user has ✅, skills user is missing ❌, prioritized by frequency in real job postings.
6. **Learning Path (15s)** — System recommends a 12-week plan: weeks 1-4 fundamentals, 5-8 specialization, 9-12 portfolio projects. Each week links to specific courses ranked by skill-match, rating, cost, and certification — drawn from Coursera, Udemy, NPTEL, SWAYAM, NCERT, and curated YouTube playlists.
7. **Resume Tailoring (20s)** — System rewrites the user's resume bullets to align with the target role's keywords and ATS expectations.
8. **Interview Prep (10s)** — System generates 10 role-specific mock questions (5 technical + 3 behavioral + 2 India-context like "expected CTC" handling).
9. **Export** — User downloads the full roadmap as a PDF or shareable link.

---

## 4. Core Features (v1)

| # | Feature | Description |
|---|---------|-------------|
| F1 | **Resume Parser** | Upload PDF → extract structured profile (education, skills, experience) using LLM + Pydantic schema |
| F2 | **Role Matcher** | RAG over Indian job postings + NCO 2015 taxonomy → top 3 role recommendations with reasoning and citations |
| F3 | **Skill Gap Analyzer** | Compare user skills vs target role's required skills (mined from real JDs) → prioritized gap list |
| F4 | **Learning Path Generator** | Curate a 12-week plan from a multi-source course catalog; cost-aware (free-first), rating-aware, certification-aware |
| F5 | **Resume Tailor** | Rewrite resume bullets to match target role's keywords and ATS norms |
| F6 | **Mock Interview Generator** | Produce 10 role-specific Qs (5 technical + 3 behavioral + 2 India-context) with model answers |
| F7 | **Roadmap Export** | Single downloadable PDF / shareable link with all of the above |

---

## 5. Out of Scope (v1)

Discipline matters. **We are explicitly NOT building these in v1**:

- ❌ Live job application submission to Naukri/LinkedIn
- ❌ Video / voice mock interviews
- ❌ Recruiter-side dashboard
- ❌ Payment / subscription flows
- ❌ Multi-language UI (English only for v1; Hindi roadmap support deferred to v2)
- ❌ User accounts / login (anonymous sessions only)
- ❌ Mobile app (responsive web only)
- ❌ Live API integrations to course providers (v1 uses snapshot datasets; v2 → live)

---

## 6. Success Metrics

### Quantitative (system quality)
- **Role-match precision @ top-3:** > 75% on a 30-persona golden test set
- **RAGAS faithfulness score:** > 0.85 (claims grounded in retrieved context)
- **RAGAS answer relevance:** > 0.80
- **Course-recommendation precision @ 5:** > 70% (relevant courses in top-5)
- **End-to-end latency (p95):** < 60 seconds for full roadmap
- **Hallucination rate** (claims about non-existent jobs/courses): < 2% on test set

### Qualitative (user experience)
- 8 / 10 test users say "this feels personalized to me, not generic"
- 8 / 10 test users would recommend it to a friend in their cohort
- All test users complete the full journey without abandoning

### Engineering
- Test coverage > 60% on retrieval and agent-orchestration code
- All LLM calls traced in LangSmith
- README has working demo link + architecture diagram + eval results

---

## 7. Architecture

The system is a **multi-agent pipeline orchestrated by LangGraph**, with shared state passed between agents and a hybrid RAG layer underneath.

### Flow
1. User input enters the **Orchestrator** (LangGraph state machine)
2. **Profile Agent** parses the resume into structured Pydantic schema
3. **Job Match Agent** does hybrid retrieval (BM42 + dense) over the indexed corpus, reranks with Cohere, and returns top-K roles
4. **Skill Gap Agent** retrieves the target role's skill requirements and diffs against the user profile
5. **Learning Path Agent** retrieves and ranks courses across all providers (rating × cost × certification weighted)
6. **Resume + Interview Agent** generates final outputs using the consolidated state

### Key design choices
- **Stateful graph (LangGraph) over a linear chain (LangChain):** allows conditional routing (e.g., skip skill-gap if user already has the target role) and human-in-the-loop checkpoints
- **Hybrid retrieval over pure dense:** keyword recall matters for skill names like "PySpark", "AWS Glue" that get watered down in pure embeddings
- **Reranker layer:** cheap quality boost; reduces top-K LLM context size, saving cost
- **Pydantic-typed agent state:** prevents the schema-drift hell that destroys multi-agent projects
- **Provider-agnostic course schema:** all courses (Coursera, Udemy, NPTEL, etc.) flow through one normalized `Course` schema. Retrieval ranks by skill match + rating + cost + certification, *not* by source. This lets us add or remove providers in v2 with zero changes to ranking, agents, or downstream code.

---

## 8. Tech Stack & Rationale

| Layer | Choice | Why |
|-------|--------|-----|
| **LLM (primary)** | Claude Sonnet 4.6 | Best agentic reasoning + tool-use stability |
| **LLM (helper)** | Claude Haiku 4.5 | Cheap, fast for parsing/classification |
| **Agent framework** | LangGraph | Stateful, graph-based, current industry standard |
| **Embeddings** | OpenAI `text-embedding-3-small` | Cheap, multilingual (handles Indian skill terms) |
| **Reranker** | Cohere Rerank v3.5 | Significant retrieval quality lift |
| **Vector DB** | Qdrant Cloud | Production-grade, free tier, hybrid (BM42) support |
| **Observability** | LangSmith | Native LangGraph integration, trace every run |
| **Evaluation** | RAGAS + custom golden set | Industry-standard RAG eval framework |
| **Backend** | FastAPI | Async, type-safe, industry default |
| **Frontend** | Streamlit (v1) | Demoable in hours; v2 → Next.js |
| **Deployment** | Hugging Face Spaces | Free, public URL, Docker-friendly |
| **Tooling protocol** | MCP (Model Context Protocol) | Bleeding-edge standard, strong resume signal |

---

## 9. Data Sourcing Strategy

A tiered approach: build broad coverage first, layer differentiators on top, defer the rest.

### 9.1 Job & Role Data

| Source | Records | Method | Tier |
|---|---|---|---|
| **NCO 2015** (National Classification of Occupations, India) | ~3,600 official roles | PDF parse via `pymupdf` | T1 (foundation) |
| **Naukri.com** (Data/AI vertical slice) | ~500 active JDs | `playwright` headless scrape OR public Kaggle dataset | T1 |
| **NCS portal** (govt jobs) | ~300 | Sitemap scrape | T2 |
| **O*NET skills mapping** (US, for skill enrichment) | ~1,000 | Public CSV download | T1 |

### 9.2 Course Catalog (multi-source)

A unified, provider-agnostic course corpus. All courses flow through the same `Course` Pydantic schema.

| Source | Target records | Method | Why this source |
|---|---|---|---|
| **Coursera** | ~1,500 (top by ratings) | Public Kaggle dataset (e.g., `coursera-courses-dataset-2021` or newer) | Globally recognized; ratings, instructors, providers structured |
| **Udemy** | ~1,000 (top by enrollment) | Public Kaggle dataset (e.g., `udemy-courses`) | Practical, project-heavy, broad price spectrum |
| **NPTEL / SWAYAM** | ~2,000 | Public CSV from their data portal + sitemap | Indian moat — IIT-quality, free, govt-certified |
| **YouTube playlists** (curated channels) | ~500 | YouTube Data API v3 (free 10K-unit/day quota) | Free, vast, where Indian learners actually start |
| **NCERT** | ~200 (foundational only) | Manual curation → CSV | Strong for fresher persona's math/stats foundations |
| **PMKVY** (top schemes) | ~50 | Manual curation → CSV | Differentiator for upskiller persona |
| **Total** | **~5,250 courses** | | |

**Rationale for source mix:**
- **Tier 1 (Coursera, Udemy, NPTEL)** delivers broad, high-quality coverage with minimal ingestion effort via public datasets.
- **Tier 2 (NCERT, PMKVY, YouTube)** adds India-specific differentiation that Western tools ignore.
- **Deferred to v2:** edX, freeCodeCamp, Pluralsight, LinkedIn Learning, live API integrations, regional-language content.

**Legal/ethical posture:** v1 uses publicly available datasets (Kaggle, official govt portals, YouTube Data API). No ToS-violating scrapes of paid platforms. Documented in README.

### 9.3 Salary Benchmarks

| Source | Records | Method |
|---|---|---|
| **AmbitionBox / Glassdoor India** | ~500 role-salary pairs | Manual curation OR Kaggle dataset |
| **Payscale.com/in** | Cross-reference | Public pages |

### 9.4 Unified Document Schema

All ingested data normalizes to this shape (Pydantic):

```python
class Document(BaseModel):
    id: str                    # stable hash-based ID
    type: Literal["job", "role", "course", "scheme", "salary"]
    title: str
    content: str               # text used for embedding
    skills: list[str]          # normalized skill tags
    metadata: dict             # source-specific extras

class Course(Document):
    type: Literal["course"] = "course"
    provider: Literal["coursera", "udemy", "nptel", "swayam",
                      "youtube", "ncert", "pmkvy"]
    duration_hours: float
    cost_inr: float            # 0 = free
    rating: float | None       # 0–5
    is_certified: bool
    url: str
```

**Why this matters:** the retriever and ranker never branch on provider. They operate on `Course` and apply weighted scoring across (skill match, rating, cost, certification, user preference). Adding a new provider in v2 = one ingest script + zero changes anywhere else.

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM hallucinates a job role / course that doesn't exist | High | High | Strict RAG with citation requirement; reject answers without ≥1 retrieved source; eval gate in CI |
| Stale data (old job postings, dead course links) | High | Medium | Quarterly snapshot refresh in v1; metadata `last_updated` field; expire records >180 days old |
| Course quality varies wildly across providers | High | Medium | Min-rating threshold (≥4.0 for paid, ≥3.5 for free); free-first ranking for Indian persona |
| PII leakage (resume sent to third-party LLM logs) | Medium | High | Scrub PII (name, email, phone) before any LLM call; opt-out flag in LangSmith |
| Latency exceeds 60s | Medium | Medium | Parallelize independent agent calls; cache embeddings; stream partial outputs to UI |
| User uploads non-resume PDF | Medium | Low | LLM-based document classification gate before parsing |
| Cost overruns from heavy users | Low (v1) | Medium | Per-session token budget cap; rate limit; switch to Haiku for non-reasoning steps |
| Course dataset has stale URLs | Medium | Low | URL liveness check during ingestion; mark dead links inactive |
| Bias toward English-language courses | High | Low (v1) | Documented v2 plan for Hindi/regional support; v1 explicitly English |

---

## 11. Future (v2+)

Ideas explicitly deferred but worth mentioning to interviewers:

- **Live course-provider APIs** (Coursera Partner API, Udemy Affiliate API, edX) replacing snapshot datasets
- **Live job-application autopilot** via Naukri/LinkedIn integrations (with user approval gate)
- **Voice-based mock interview** with speech-to-speech eval
- **Adaptive learning** — track user's actual progress, re-plan when they fall behind
- **Skill verification** — micro-assessments to validate claimed skills

---

## Appendix A: Golden Test Set Plan

We will hand-craft **30 personas** spanning:
- 10 freshers (across CS, ECE, Mech, BCom, BSc)
- 10 career-switchers (manufacturing→tech, BPO→analyst, etc.)
- 10 upskillers (mid-career adding GenAI, cloud, data)

For each persona, we record:
- Input profile
- Expected top-3 role matches (validated by 2 reviewers)
- Expected critical skill gaps
- Expected reasonable learning path (mix of free + paid, sources spanning ≥2 providers)

This becomes our regression suite + the data RAGAS evaluates against.

---

## Appendix B: Glossary

- **NCO 2015** — National Classification of Occupations (India), official role taxonomy
- **NPTEL** — National Programme on Technology Enhanced Learning, IIT-led MOOC platform
- **SWAYAM** — Govt of India's unified MOOC platform
- **NCERT** — National Council of Educational Research and Training (foundational education content)
- **PMKVY** — Pradhan Mantri Kaushal Vikas Yojana, govt skill development scheme
- **NSDC** — National Skill Development Corporation
- **RAG** — Retrieval-Augmented Generation
- **MCP** — Model Context Protocol (Anthropic)
- **BM42** — Qdrant's hybrid sparse-dense retrieval algorithm
- **ATS** — Applicant Tracking System (resume parsing software used by recruiters)

---

*This PRD is a living document. Every architectural decision, scope cut, source choice, and metric is captured here so future-me (and any interviewer) can trace the "why" behind the "what."*
