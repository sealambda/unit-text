import uvicorn

from .app import app


# This is just a convenience function to run the server from the command line
def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
