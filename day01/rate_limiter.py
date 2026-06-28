import asyncio
import time
from fastapi import FastAPI, HTTPException, Depends

class TokenRateLimiter():
    def __init__(self, max_tokens : int, refill_rate : float):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self._lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False    
    
    def _refill(self):
        curr_time = time.monotonic()
        els_time = curr_time - self.last_refill
        added = els_time * self.refill_rate
        self.tokens = min(self.max_tokens, self.tokens + added)
        self.last_refill = curr_time

limiter =  TokenRateLimiter(5, 1.0)  
#limiter = TokenRateLimiter(max_token = 10, refill_rate = 1.0)


async def rate_limit_dep():
    allowed = await limiter.acquire()

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeds")



app = FastAPI()

@app.get('/valuation', dependencies=[Depends(rate_limit_dep)])
def get_valuation():
    return {"status": "success", "message": "Valuation data retrieved successfully."}



