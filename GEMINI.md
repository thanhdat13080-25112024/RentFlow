# GEMINI.md

This file provides foundational mandates and technical guidance for Gemini CLI in this repository.

## Commands

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the application
python main.py

# Run tests
pytest

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

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

## Architecture Overview

RentFlow is a lightweight property management system.
- **Backend**: FastAPI with SQLAlchemy 2.0.
- **Frontend**: Jinja2 templates + Alpine.js + Tailwind CSS.
- **Database**: SQLite (default) or PostgreSQL.
- **Authentication**: JWT stored in HTTP-only cookies.

### Key Directories
- `app/api/v1/endpoints/`: REST API implementation.
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic models for data validation.
- `app/services/`: Business logic (billing, seeding).
- `app/templates/`: Jinja2 UI components.
- `app/static/`: CSS tokens and Alpine.js logic.
