from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import math

app = FastAPI()

# Ensure CORS is enabled
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
    digits = [int(d) for d in str(abs(n))]  # Use absolute value for calculation
    return sum(d ** len(digits) for d in digits) == abs(n)

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def classify_number(n: int):
    """Classify the number and return properties."""
    properties = []
    
    if n < 0:
        properties.append("negative")  # Explicitly mark negative numbers

    if is_armstrong(abs(n)):  # Check Armstrong property with absolute value
        properties.append("armstrong")

    if n % 2 != 0:
        properties.append("odd")
    
    return {
        "number": n,
        "is_prime": is_prime(abs(n)),  # Use absolute value for prime check
        "is_perfect": is_perfect(abs(n)),  # Use absolute value for perfect number check
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(n)))  # Ensure digit sum is valid
    }

@app.get("/api/classify-number")
async def classify(number: int = Query(..., description="Number to classify")):
    """Classify a number as prime, perfect, odd, or none of the above."""
    try:
        classification = classify_number(number)
        fun_fact = "No fun fact available."

        async with httpx.AsyncClient(timeout=1.0) as client:
            response = await client.get(f"http://numbersapi.com/{number}")
            if response.status_code == 200:
                fun_fact = response.text

        classification["fun_fact"] = fun_fact
        return JSONResponse(content=classification, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions gracefully."""
    return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)
