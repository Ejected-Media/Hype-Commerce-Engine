import redis
from fastapi import APIRouter

router = APIRouter()
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

@router.post("/bid")
async def place_bid(auction_id: str, user_id: str, amount: float):
    # Phase 3: Lua Script for atomic "Hype" extension
    lua_bid = """
    local current = tonumber(redis.call('HGET', KEYS[1], 'price') or 0)
    if tonumber(ARGV[1]) > current then
        redis.call('HSET', KEYS[1], 'price', ARGV[1], 'winner', ARGV[2])
        redis.call('HINCRBY', KEYS[1], 'end_time', 10)
        return 1
    end
    return 0
    """
    success = r.eval(lua_bid, 1, f"auction:{auction_id}", amount, user_id)
    return {"success": bool(success)}
  
