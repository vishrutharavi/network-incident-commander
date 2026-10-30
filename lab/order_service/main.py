import os
import logging
import httpx

from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("order-service")

app = FastAPI(title="Order Service")

PAYMENT_URL = os.getenv(
    "PAYMENT_URL",
    "http://payment-service:8003"
)

INVENTORY_URL = os.getenv(
    "INVENTORY_URL",
    "http://inventory-service:8002"
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/orders")
async def create_order():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            payment = await client.post(
                f"{PAYMENT_URL}/pay"
            )
            payment.raise_for_status()

            inventory = await client.post(
                f"{INVENTORY_URL}/reserve"
            )
            inventory.raise_for_status()

        return {
            "order_id": "ORD-001",
            "status": "completed",
            "payment": payment.json(),
            "inventory": inventory.json()
        }

    except httpx.HTTPError as error:
        logger.error(
            "Downstream service failure: %s",
            error
        )

        raise HTTPException(
            status_code=503,
            detail="Downstream service unavailable"
        )