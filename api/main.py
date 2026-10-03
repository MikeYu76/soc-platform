from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SOC Platform",
        "version": "0.1.0"
    }