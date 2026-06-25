import subprocess
import sys


def run_migrations():
    """Run Alembic migrations before starting the application."""
    try:
        print("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Migrations completed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    run_migrations()

    print("Starting FastAPI application...")
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from app.main import app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
