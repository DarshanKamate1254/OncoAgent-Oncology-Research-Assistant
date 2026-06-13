# Engineering & Development Best Practices

This document outlines the standard development guidelines, design paradigms, and coding practices for both the Frontend and Backend of the system.

---

## 🎨 Frontend Guidelines (Next.js & React)

### 1. Project Organization
* **App Router Structure**: Always place route pages inside `src/app`. Keep pages lightweight and outsource complex components to `src/components`.
* **CSS Modules**: Use Vanilla CSS Modules (`*.module.css`) for component styling to guarantee encapsulation. Avoid using global styles unless setting core design tokens in `globals.css`.

### 2. State & Data Flow
* **Server Components by Default**: Leave components as Server Components by default. Add `"use client"` only when incorporating client-side interactivity, hooks (`useState`, `useEffect`), or browser APIs.
* **Loading & Error Boundaries**: Always leverage Next.js native `loading.tsx` and `error.tsx` files at the route level to handle async states gracefully.

### 3. Styling & Accessibility (Aesthetics first!)
* **Premium Theme Harmony**: Adhere to the established CSS variables system (dark-themed deep colors, glassmorphism, accent colors like cyber teal and royal violet).
* **Responsive Layouts**: Use CSS Grid and Flexbox for fluid layouts. Verify components render perfectly on viewport widths from `320px` to `1920px`.
* **Alt Tags & ARIA Roles**: Every image must have an `alt` attribute. Interactive elements must have proper semantic HTML tags (e.g., `<button>` instead of `div onClick`).

---

## ⚙️ Backend Guidelines

### 1. Architecture & Design Patterns
* **FastAPI Framework**: Use FastAPI for low-overhead, typed, asynchronous endpoints. Fully leverage Pydantic models for request and response validation.
* **Separation of Concerns**: Divide code into explicit modules:
  * `api/` – Routes and handlers
  * `agents/` – Agent orchestration logic and graphs
  * `tools/` – Search utilities, RAG queries, and external APIs
  * `config/` – Environment variables and system settings

### 2. Modularity & Reusability Constraints (Strict)
* **Max 70 Lines Per File**: No backend source code file should exceed 70 lines of code. This prevents bloated monolithic files and forces clean delegation.
* **High Reusability**: Extract utility functions, helper classes, and agent tools into specialized modules to maximize sharing.
* **Simple Topic-Related Naming**: File and folder names must be lowercase, simple, descriptive, and directly related to their topic (e.g., `trial_search.py`, `patient_parser.py`).

### 3. Agent Orchestration (LangGraph / LangChain)
* **Modular Agent State**: Ensure the state schema passed between agents is well-typed, immutable, and strictly validated.
* **Streaming Streams**: Use Server-Sent Events (SSE) or WebSockets to stream agent execution logs/thoughts to the frontend. Avoid blocking synchronous responses for long-running workflows.

### 4. Reliability & Testing
* **Defensive Design**: Implement retry policies on third-party API calls (e.g., LLMs, search tools) using libraries like `tenacity`.
* **Testing Suites**: Use `pytest` for backend unit and integration tests. Mock LLM responses during tests to ensure predictable CI/CD pipelines.

