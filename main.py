from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import math
from functools import lru_cache
import logging
import re

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper Functions
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):  # Skip even numbers
        if n % i == 0:
            return False
    return True

@lru_cache(maxsize=1000)  # Cache results for performance
def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@lru_cache(maxsize=1000)  # Cache results for performance
def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

@lru_cache(maxsize=1000)  # Cache results for performance
def get_fun_fact(number: int) -> str:
    """Fetch a fun fact about a number from the Numbers API."""
    url = f"http://numbersapi.com/{number}"
    try:
        response = httpx.get(url, timeout=2.0)  # Set a timeout for the request
        if response.status_code == 200:
            return response.text
        else:
            return f"Could not fetch fun fact (HTTP {response.status_code})."
    except httpx.TimeoutException:
        return "Could not fetch fun fact (timeout)."
    except httpx.RequestError as e:
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
        "digit_sum": sum(int(digit) for digit in str(n)),
    }

# Input Validation
def validate_number(input: str) -> int:
    """Validate the input to ensure it is a positive integer."""
    if not re.match(r"^\d+$", input):  # Check if the input is a valid integer
        raise ValueError("Input must be a valid positive integer.")
    number = int(input)
    if number <= 0:
        raise ValueError("Input must be a positive integer.")
    return number

# API Endpoint
@app.get("/api/classify-number")
async def classify(number: str = Query(..., description="Number to classify")):
    """Classify a number as prime, perfect, odd, or none of the above."""
    try:
        # Validate the input
        number_int = validate_number(number)

        # Classify the number and fetch its properties
        classification = classify_number(number_int)
        classification["fun_fact"] = get_fun_fact(number_int)  # Fetch fun fact
        return JSONResponse(content=classification, status_code=200)
    except ValueError:
        # Handle invalid input (e.g., negative numbers, decimals, or non-numeric input)
        return JSONResponse(
            content={"number": number, "error": True},
            status_code=400,
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions gracefully."""
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        content={"error": True, "message": exc.detail}, status_code=exc.status_code
    )