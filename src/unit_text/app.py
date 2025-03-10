import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile

from .core import run_tests
from .models import IdeaModel, TestResult

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the unit-text API!"}


@app.post("/test")
async def test(
    file: UploadFile,
    config: UploadFile,
) -> TestResult:
    """Run tests on the input file against the config."""
    print("Running tests...")

    try:
        file_content = await file.read()
        config_content = await config.read()

        file_text = file_content.decode("utf-8")
        idea = IdeaModel.model_validate_json(config_content.decode("utf-8"))

        return run_tests(file_text, idea)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


def run():
    """Start the FastAPI server with uvicorn"""
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run()
