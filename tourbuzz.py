import uvicorn
from api import app
from jobs import run_jobs


if __name__ == "__main__":
    """
    The main entry point for the API, runs a uvicorn server on port 8000.
    """
    run_jobs()
    uvicorn.run(app, host="0.0.0.0", port=8000)
