import stripe, httpx, os
from fastapi import APIRouter

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/checkout")
async def create_session(drop_id: str, seller_stripe_id: str, amount: float):
    # Phase 1: Directing funds with a 10% platform fee
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': drop_id}, 'unit_amount': int(amount * 100)}, 'quantity': 1}],
        mode='payment',
        payment_intent_data={'transfer_data': {'destination': seller_stripe_id}, 'application_fee_amount': int(amount * 10)},
        success_url="https://localsq.com/success",
        cancel_url="https://localsq.com/cancel"
    )
    return {"url": session.url}

@router.get("/twitch/verify")
async def verify_stream(twitch_id: str):
    # Phase 1: Check if seller is live to release funds
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.twitch.tv/helix/streams?user_id={twitch_id}", 
                               headers={"Client-Id": os.getenv("TWITCH_ID"), "Authorization": f"Bearer {os.getenv('TWITCH_TOKEN')}"})
        return {"is_live": len(res.json().get('data', [])) > 0}
      
