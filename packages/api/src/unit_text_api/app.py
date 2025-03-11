"""FastAPI application for the unit-text API."""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from unit_text_core import IdeaModel, TestResult, run_tests

app = FastAPI()


class TestRequest(BaseModel):
    """Request model for the test endpoint."""

    draft: str
    idea: IdeaModel


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the unit-text API!"}


@app.post("/test")
async def test(request: TestRequest) -> TestResult:
    """Run tests on the input draft against the idea configuration."""
    print("Running tests...")

    try:
        return run_tests(request.draft, request.idea)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


def run():
    """Start the FastAPI server with uvicorn."""
    uvicorn.run(app, host="127.0.0.1", port=8000)


def dev():
    """Start the FastAPI server with uvicorn."""
    uvicorn.run(
        "unit_text_api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["packages/api/src/unit_text_api"],
    )
