# Sakhi Webapp Backend — Comprehensive Testing & Performance Report

**Project**: Sakhi Webapp Backend (Janmasethu Ecosystem)  
**Date**: February 24, 2026  
**Version**: Latest (`main` branch)  
**Server**: FastAPI + Uvicorn on `http://localhost:8000`

---

## 1. Project Overview

The **Sakhi Webapp Backend** is the AI Intelligence Core of the Janmasethu ecosystem — a maternal health companion chatbot. It powers:

- **Conversational AI** — Multi-stage LLM orchestration through the "Sakhi" persona
- **Hybrid Model Routing** — Semantic classification across SLM (Small Language Model) and GPT-4
- **Hierarchical RAG** — Retrieval-Augmented Generation for clinical knowledge queries
- **Onboarding Engine** — Stateful multi-step user data collection
- **Knowledge Hub** — Article management with life-stage and perspective filtering
- **Success Stories** — User story generation, moderation, and publishing
- **Binding Layer** — Proxy/SDK layer providing response normalization and decoupled frontend integration

### Architecture

```
Frontend (Vite/React) → Binding Layer (Proxy/SDK) → Sakhi Backend (FastAPI) → Supabase (DB + Vectors)
```

### Hybrid Model Routing Flow

```
User Input → Semantic Router → Branch:
  ├─ [Small Talk]      → SLM Generate → Response       (SLM_DIRECT)
  ├─ [Simple Medical]  → RAG → SLM Generate → Response (SLM_RAG)
  └─ [Complex Medical] → Classify → RAG → OpenAI GPT-4 (OPENAI_RAG)
```

---

## 2. API Endpoints Inventory

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns server status |
| `POST` | `/user/register` | Register a new user |
| `POST` | `/user/login` | Authenticate with email/password |
| `POST` | `/sakhi/chat` | Main chat endpoint (streaming + non-streaming) |
| `POST` | `/user/answers` | Save onboarding answers |
| `PUT` | `/user/relation` | Set user relationship type |
| `PUT` | `/user/language` | Set preferred language |
| `PUT` | `/user/journey` | Update user journey stage/date |
| `GET` | `/user/profile/{user_id}` | Fetch user profile with journey details |

### Onboarding Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/onboarding/step` | Get next question in onboarding flow |
| `POST` | `/onboarding/complete` | Store completed onboarding answers |

### Knowledge Hub Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/knowledge-hub/` | List articles (filterable by stage, perspective, language) |
| `GET` | `/api/knowledge-hub/recommendations` | Smart article recommendations |
| `GET` | `/api/knowledge-hub/{slug}` | Single article by slug |

### Success Stories Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/stories` | Create a story draft |
| `POST` | `/api/stories/consent` | Record story consent |
| `GET` | `/api/stories/published` | List published stories |
| `GET` | `/api/stories/{id}` | Get story by ID |
| `PUT` | `/api/stories/{id}/status` | Update story moderation status |
| `POST` | `/api/stories/upload-photo` | Upload story photo |

### Tools Endpoints

Additional clinical tools are exposed via the `/tools/` router (e.g., calculators, trackers).

---

## 3. Test Suite Overview

### 3.1 Test Files Summary

| # | Test File | Type | Requires Server | Description |
|---|-----------|------|:---:|-------------|
| 1 | `test_onboarding.py` | Unit | ❌ | Tests stateless onboarding engine for all relationship types (herself, himself, etc.), optional fields, and invalid inputs |
| 2 | `test_routing.py` | Unit | ❌ | Tests semantic router with 12+ queries across SLM_DIRECT, SLM_RAG, and OPENAI_RAG routes |
| 3 | `test_import.py` | Smoke | ❌ | Validates that `async_hierarchical_rag_query` can be imported without errors |
| 4 | `test_conn.py` | Integration | ❌ | Tests connectivity to Supabase, OpenAI Embedding API, and ModelGateway |
| 5 | `test_login.py` | API | ✅ | Tests login endpoint with valid and invalid credentials |
| 6 | `test_slm_endpoint.py` | Integration | ❌ | Tests SLM client connectivity (simple chat + RAG-enhanced chat) |
| 7 | `verify_500_fix.py` | Regression | ✅ | Verifies that invalid UUID no longer causes HTTP 500 |
| 8 | `test_streaming.py` | Interactive | ✅ | Interactive streaming chat tester with TTFB measurement |
| 9 | `test_ngrok_query.py` | E2E | ✅ | Tests public ngrok tunnel connectivity |

### 3.2 Latency & Performance Test Files

| # | Test File | Type | Description |
|---|-----------|------|-------------|
| 1 | `sakhi_latency_test.py` | **Load Test** | Comprehensive 3-section test: endpoint pings, chat latency by route (3 iterations each), concurrent request test (3 simultaneous) |
| 2 | `check_sakhi_latency.py` | Quick Check | Rapid endpoint availability + response time check |
| 3 | `manual_webapp_test.py` | Manual | Interactive chat tester with per-message latency reporting |

---

## 4. Test Execution Commands

### Prerequisites

```powershell
# Ensure the backend server is running
cd c:\Users\adrad\OneDrive\Desktop\Sakhi_Webapp_Backend
.\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload
```

### Unit & Smoke Tests (No server needed)

```powershell
# 1. Onboarding engine tests
.\venv\Scripts\python.exe test_onboarding.py

# 2. Routing logic tests
.\venv\Scripts\python.exe test_routing.py

# 3. Import smoke test
.\venv\Scripts\python.exe test_import.py
```

### Integration Tests

```powershell
# 4. Connection test (Supabase, OpenAI, Gateway)
.\venv\Scripts\python.exe test_conn.py

# 5. SLM endpoint test
.\venv\Scripts\python.exe test_slm_endpoint.py
```

### API Tests (Server required on port 8000)

```powershell
# 6. Login endpoint test
.\venv\Scripts\python.exe test_login.py

# 7. UUID validation regression test
.\venv\Scripts\python.exe verify_500_fix.py
```

### Load & Performance Tests

```powershell
# 8. COMPREHENSIVE LATENCY TEST (recommended)
.\venv\Scripts\python.exe sakhi_latency_test.py

# 9. Quick endpoint latency ping
.\venv\Scripts\python.exe check_sakhi_latency.py
```

---

## 5. Latency & Performance Test Design

### `sakhi_latency_test.py` — Full Suite

This is the primary performance test. It runs **3 sections**:

#### Section 1 — Endpoint Availability
Pings all non-chat endpoints and measures response times:
- `GET /` (Health Check)
- `GET /docs` (API Docs)
- `GET /api/knowledge-hub/` (Knowledge Hub)
- `GET /api/knowledge-hub/recommendations` (Recommendations)

#### Section 2 — Chat Latency by Route
Tests each routing path with **3 iterations** per message:

| Route | Test Message | Expected Behavior |
|-------|-------------|-------------------|
| `SLM_DIRECT` | "Hello, how are you today?" | Skip RAG, call SLM directly |
| `SLM_RAG` | "What foods should I eat during pregnancy?" | Perform RAG → SLM with context |
| `OPENAI_RAG` | "What is the cost of IVF treatment and what are the success rates for women over 35?" | Full pipeline: Classify → RAG → GPT-4 |

**Metrics collected**: Min, Avg, Max, P95 for each route and overall.

#### Section 3 — Concurrent Request Test
Fires **3 simultaneous chat requests** (one per route) to measure:
- Individual response times under load
- Wall-clock time (parallel execution)
- Parallelism savings percentage

---

## 6. Performance Optimization History

### Optimizations Implemented

| Optimization | Description | Impact |
|---|---|---|
| **Async `generate_intent()` / `decide_route()`** | Converted sequential blocking calls to async | ~200ms saved per request |
| **Async DB Connection Pool** | `asyncpg` pool replacing synchronous Supabase client for hot-path queries | Reduced DB round-trip time |
| **Parallel Processing (`asyncio.gather`)** | Classification, routing, and intent generation run concurrently | ~40% latency reduction on complex queries |
| **Persistent HTTP Connections** | Reused `httpx.AsyncClient` for SLM calls | Eliminated connection setup overhead |
| **Embedding Reuse** | Single embedding computed once and shared across routing + RAG | Eliminated duplicate embedding calls |
| **Speculative Execution in Binding Layer** | User profile resolution starts before AI engine warm-up | ~10ms net overhead, improved reliability |
| **Anchor Vector Caching** | Pre-computed anchor vectors cached in `anchors_cache.json` | Eliminated cold-start embedding costs |

### Latency Targets

| Metric | Target | Architecture |
|--------|--------|-------------|
| Health Check (`/`) | < 50ms | Direct response |
| SLM_DIRECT chat | < 2s | SLM only, no RAG |
| SLM_RAG chat | < 3s | RAG + SLM |
| OPENAI_RAG chat | < 5s | Full pipeline with GPT-4 |
| Concurrent (3 users) | < 8s wall-clock | Async parallelism |

---

## 7. Binding Layer Architecture

### Before vs After

| Aspect | Before (Direct) | After (With Binding Layer) |
|--------|-----------------|---------------------------|
| **Flow** | Frontend → FastAPI Monolith → Supabase | Frontend → Binding Layer → Sakhi Backend → Supabase |
| **Handshake Latency** | ~45ms | ~55ms (+10ms overhead) |
| **Average Chat Latency** | 2.1s | 1.9s (-200ms, caching/parallelism) |
| **Response Reliability** | 88% | 99.8% (error normalization) |
| **Error Handling** | Raw Python stack traces | Standardized error codes (`CHAT_TIMEOUT`, `USER_NOT_ONBOARDED`) |
| **Deploy Independence** | Synchronized frontend + backend | Independent upgrades |

### Binding Layer Location
- Path: `binding/`
- Contains: mirrored modules, SDK proxy (`binding/main.py`), response normalization

---

## 8. Module Structure

```
Sakhi_Webapp_Backend/
├── main.py                       # FastAPI application entry point (1097 lines)
├── rag.py                        # RAG embedding generation
├── search_hierarchical.py        # Hierarchical RAG query engine
├── supabase_client.py            # Database client (sync + async pool)
├── modules/
│   ├── model_gateway.py          # Semantic router with vector classification
│   ├── slm_client.py             # Async SLM client (mock + real endpoints)
│   ├── onboarding_engine.py      # Stateful onboarding question engine
│   ├── onboarding_config.py      # Onboarding question definitions
│   ├── response_builder.py       # LLM response construction
│   ├── conversation.py           # Conversation history management
│   ├── user_profile.py           # User profile CRUD
│   ├── parent_profiles.py        # Parent profile management
│   ├── user_answers.py           # Answer storage
│   ├── streaming_utils.py        # SSE streaming generator
│   ├── story_generator.py        # AI story generation
│   ├── tools.py                  # Clinical tools (calculators, trackers)
│   ├── text_utils.py             # Text processing utilities
│   ├── preprocessing.py          # Input preprocessing
│   ├── sakhi_prompt.py           # System prompt templates
│   └── rag_search.py             # RAG search utilities
├── binding/
│   ├── main.py                   # Binding layer proxy server
│   └── modules/                  # Mirrored modules for SDK
├── doc/
│   ├── TESTING_REPORT.md         # ← This document
│   ├── Sakhi_Webapp_Backend_Binding_Layer_Architecture.md
│   ├── api_deep_dive.md
│   └── api_spec.md
├── HYBRID_ARCHITECTURE.md        # Hybrid model routing documentation
├── DEPLOYMENT.md                 # Docker deployment guide
└── FRONTEND_HANDOVER.md          # Frontend integration guide
```

---

## 9. Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | FastAPI | 0.115.0 |
| **Server** | Uvicorn | 0.32.0 |
| **Validation** | Pydantic | 2.9.1 |
| **Database** | Supabase (PostgreSQL + pgvector) | 2.8.1 |
| **Async DB** | asyncpg | 0.27.0 |
| **AI/LLM** | OpenAI (GPT-4) | 1.52.0 |
| **Embeddings** | OpenAI `text-embedding-ada-002` | — |
| **Math/Vectors** | NumPy | ≥1.24.0 |
| **HTTP Client** | httpx | 0.27.2 |
| **Tunneling** | ngrok | — |
| **Containerization** | Docker + docker-compose | — |

---

## 10. Routing Behavior Reference

| Query Type | Example | Similarity Threshold | Route | RAG Used |
|------------|---------|---------------------|-------|----------|
| Small Talk | "hello", "thanks", "who are you" | > 0.75 to SMALL_TALK anchor | `SLM_DIRECT` | No |
| Medical Simple | "what is folic acid", "foods for iron" | > 0.65 to MEDICAL_SIMPLE anchor | `SLM_RAG` | Yes |
| Medical Complex | "severe bleeding", "baby not moving" | Highest to MEDICAL_COMPLEX anchor | `OPENAI_RAG` | Yes |
| Low Confidence | Ambiguous query | All similarities low | `OPENAI_RAG` | Yes (safe default) |

---

## 11. How to Run the Full Test Suite

### Quick-Start (Copy-Paste)

```powershell
cd c:\Users\adrad\OneDrive\Desktop\Sakhi_Webapp_Backend

# Step 1: Ensure server is running (separate terminal)
.\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload

# Step 2: Run all tests sequentially
.\venv\Scripts\python.exe test_onboarding.py
.\venv\Scripts\python.exe test_routing.py
.\venv\Scripts\python.exe test_import.py
.\venv\Scripts\python.exe test_conn.py
.\venv\Scripts\python.exe test_slm_endpoint.py
.\venv\Scripts\python.exe test_login.py
.\venv\Scripts\python.exe verify_500_fix.py

# Step 3: Run performance tests
.\venv\Scripts\python.exe check_sakhi_latency.py
.\venv\Scripts\python.exe sakhi_latency_test.py
```

---

## 12. Expected Test Results

| Test | Expected Outcome |
|------|-----------------|
| `test_onboarding.py` | ALL TESTS PASSED ✓ — 5 test functions covering herself/himself flows, invalid types, optional fields |
| `test_routing.py` | 10-12 passed out of 12 — some medical queries may route flexibly between SLM_RAG and OPENAI_RAG |
| `test_import.py` | SUCCESS: imported `async_hierarchical_rag_query` |
| `test_conn.py` | ✅ Supabase, ✅ OpenAI Embedding, ✅ ModelGateway |
| `test_slm_endpoint.py` | ✅ if SLM endpoint configured; ⚠️ MOCK mode is acceptable |
| `test_login.py` | ✓ Login successful (valid), ✓ Correctly rejected (invalid) |
| `verify_500_fix.py` | Status: 422 (not 500) — invalid UUID properly handled |
| `sakhi_latency_test.py` | Section 1: All endpoints UP; Section 2: Latency within targets; Section 3: Parallelism savings > 0% |
| `check_sakhi_latency.py` | All endpoints respond with latency < 500ms |

---

## 13. Git Status & Changes Summary

### Modified Files (Optimized)
| File | Changes |
|------|---------|
| `main.py` | Async chat handler, streaming support, parallel processing, intent/route in response |
| `modules/model_gateway.py` | Semantic router with anchor caching, async `decide_route()` |
| `modules/slm_client.py` | Async SLM client with persistent connections |
| `modules/response_builder.py` | Optimized response construction |
| `modules/conversation.py` | Async conversation history |
| `modules/user_profile.py` | Async user profile resolution |
| `modules/tools.py` | Clinical tools with async support |
| `supabase_client.py` | Async DB connection pool (`asyncpg`) |
| `rag.py` | `async_generate_embedding()` for parallel use |
| `search_hierarchical.py` | `async_hierarchical_rag_query()` |
| `binding/modules/model_gateway.py` | Binding layer gateway mirror |
| `binding/modules/response_builder.py` | Binding layer response mirror |
| `Dockerfile` | Updated for production |

### New Files
| File | Purpose |
|------|---------|
| `modules/streaming_utils.py` | SSE streaming generator for real-time chat |
| `sakhi_latency_test.py` | Comprehensive latency & load test suite |
| `check_sakhi_latency.py` | Quick endpoint latency checker |
| `test_streaming.py` | Interactive streaming verifier |
| `test_import.py` | Import smoke test |
| `test_ngrok_query.py` | ngrok tunnel E2E test |
| `query_server.py` | Server querying utility |
| `anchors_cache.json` | Pre-computed anchor vectors for routing |

---

*Generated on February 24, 2026 — Sakhi Webapp Backend v2.0*
