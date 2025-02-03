from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import math
import logging
logging.basicConfig(level=logging.INFO)
from functools import lru_cache

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

@lru_cache(maxsize=1000)  # Cache up to 1000 fun facts
def get_fun_fact(number: int) -> str:
    """Fetch a fun fact about a number with error handling and retry logic."""
    url = f"http://numbersapi.com/{number}"
    try:
        response = httpx.get(url, timeout=2.0)  # Slightly increased timeout
        logging.info(f"API response: {response.status_code}")
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"API error: {response.status_code}")
            return f"Could not fetch fun fact (HTTP {response.status_code})."
    except httpx.TimeoutException:
        logging.error("API timeout")
        return "Could not fetch fun fact (timeout)."
    except httpx.RequestError as e:
        logging.error(f"API error: {str(e)}")
        return f"Could not fetch fun fact (error: {str(e)})."

def classify_number(n: int):
    """Classify the number and return its properties."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 != 0:
        properties.append("odd")

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(n))
    }

@app.get("/api/classify-number")
async def classify(number: int = Query(..., description="Number to classify")):
    """Classify a number as prime, perfect, odd, or none of the above."""
    try:
        classification = classify_number(number)
        classification["fun_fact"] = get_fun_fact(number)  # Fetch fun fact immediately
        return JSONResponse(content=classification, status_code=200)
    except ValueError:
        return JSONResponse(content={"number": str(number), "error": True}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions gracefully."""
    return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)
