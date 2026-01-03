import os
from fastapi import FastAPI, Request, HTTPException
from services.api import payments, marketplace, auctions

app = FastAPI(title="Hype Commerce Engine")

# Include the modular routes from our roadmap phases
app.include_router(payments.router, prefix="/payments", tags=["Phase 1"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Phase 2"])
app.include_router(auctions.router, prefix="/auctions", tags=["Phase 3"])

@app.get("/")
async def root():
    return {"status": "online", "projects": ["localSq", "Shop Oahu", "Phoenix Valley"]}
  
