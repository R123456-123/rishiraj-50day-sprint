import asyncio
import functools

def retry_with_backoff(max_retries: int = 3, delay_rate: float =1.0):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attemps in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attemps == max_retries:
                        print(f"Failed after {max_retries} attemps: {e}")
                        raise
                    delay = delay_rate * (2 **(attemps - 1))
                    print(f"Attempt {attemps} failed: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator            
           
# test — simulates an API call that fails twice then succeeds
call_count = 0

@retry_with_backoff(max_retries=3, delay_rate=1.0)
async def fake_api_call():
    global call_count
    call_count += 1
    if call_count < 3:
        raise Exception(f"API timeout (call {call_count})")
    return {"status": "ok", "data": "valuation result"}


async def main():
    print("=== Testing retry_with_backoff ===")
    result = await fake_api_call()
    print(f"Final result: {result}")

asyncio.run(main())