from fastapi import FastAPI

app = FastAPI(title="Payment Service")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/pay")
def pay():
    return {
        "payment_id": "PAY-001",
        "status": "success"
    }