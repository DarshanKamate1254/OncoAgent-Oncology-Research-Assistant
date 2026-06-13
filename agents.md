# Agent Coding Instructions & Guidelines

Welcome, AI coding agent! Please read and follow these rules strictly to ensure you do not break the repository structure, styling, or configuration when implementing features.

---

## 📂 Project Structure
- `/frontend`: Next.js (App Router, TypeScript, Vanilla CSS Modules)
- `/backend`: To be implemented (FastAPI, LangGraph/LangChain)

---

## ⚠️ Styling Rules (No Tailwind unless requested)
- **Do NOT introduce Tailwind CSS** to this workspace unless explicitly instructed by the user.
- **Use Vanilla CSS Modules** for styling. Create a `[component].module.css` file next to your component and import it.
- Maintain a **Premium Dark/Neon Aesthetic** using design tokens in `/frontend/src/app/globals.css`.

---

## 🔧 Code Quality & Safety Rules
1. **Preserve Documentation**: Do not remove, replace, or edit existing comments, docstrings, or markdown instructions unless requested to update them.
2. **TypeScript Integrity**: Keep code strictly typed. Do not resort to `any` unless absolutely necessary.
3. **Verify Changes**: After modifying any frontend code, always run the dev server (`npm run dev`) and check the browser console to verify no compilation warnings exist. However, do NOT run automated browser-agent tests or screenshot verifications until the user explicitly confirms that the frontend is ready for testing.
4. **Environment Variables**: Never hardcode secret keys or API keys. Always retrieve them from process environments (`process.env` in frontend, `os.getenv` in backend) and document new keys in `.env.example`.
5. **No Placeholders**: Do not insert dummy placeholders for production features. If an integration is not complete, handle the absence gracefully with loading skeletons, warning banners, or mock fallbacks.
6. **Strict Backend Modularization & Line Limits**: When creating or modifying backend files, ensure that:
   - No code file exceeds 70 lines.
   - Naming conventions are simple and directly related to the file's topic (e.g., `clinical_search.py`, `criteria_validator.py`).
   - Code is written with high reusability in mind, extracting utility functions and components into dedicated sub-modules.
7. **Task Planning Workflow**: Before starting any non-trivial task or feature implementation, you must create a detailed planning file in the `/plans` folder (e.g., `/plans/feature_name.md`). Present the plan to the user, request their feedback, and wait for explicit approval before proceeding with the changes.


