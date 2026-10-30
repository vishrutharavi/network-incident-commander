from fastapi import FastAPI

app = FastAPI(title="Inventory Service")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reserve")
def reserve():
    return {
        "reservation_id": "INV-001",
        "status": "reserved"
    }