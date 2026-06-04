# GEMINI.md

This file provides foundational mandates for Gemini CLI in this repository.

## Development Workflow

1.  **Branching**: ALWAYS create a new feature branch from `main` before making any code changes.
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  **Implementation**: Make changes, test, and validate.
3.  **Documentation**: Create or update a Markdown file (e.g., `PROGRESS.md`) to document the progress, technical decisions, and specific changes made.
4.  **Merging**: Once the task is complete and verified, merge the branch back into `main`.
    ```bash
    git checkout main
    git merge feature/your-feature-name
    git branch -d feature/your-feature-name
    ```
