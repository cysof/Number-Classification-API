from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import math

app = FastAPI()

# making sure CORS IS ENABLE

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    
)

def is_prime(n: int) -> bool:

    """
    Return True if n is a prime number, False otherwise.

    A prime number is a positive integer that is divisible only by itself and 1.
    """
    
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    """
    Return True if n is an Armstrong number, False otherwise.
    An Armstrong number is one for which the sum of the k-th powers of its digits is equal to the number itself.
    """
    
    _digits = [int(d) for d in str(n)]
    return sum(d ** len(_digits) for d in _digits) == n

def is_perfect(n: int) -> bool:
    """
    Return True if n is a perfect number, False otherwise.
    A perfect number is an integer that is equal to the sum of its proper divisors, excluding itself.
    """
    
    return sum(i for i in range(1, n) if n % i == 0) == n


def classify_number(n: int):
    """
    Classify a number into a set of properties and return a dict with the number,
    whether it is prime, whether it is perfect, a list of properties (odd,
    armstrong, etc.), and the sum of its digits.
    """
    
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

@app.get("https://number-classification-api-zf81.onrender.com/api/classify-number?number=371")
async def classify(number: int = Query(..., description = "Number to classify")):
    """
    Classify a number as prime, perfect, odd, or none of the above.
    
    Args:
        number (int): The number to classify.
    
    Returns:
        dict: A dictionary with the following keys:
            - `number`: The number that was classified.
            - `is_prime`: A boolean indicating if the number is prime.
            - `is_perfect`: A boolean indicating if the number is perfect.
            - `properties`: A list of strings with the properties of the number.
            - `digit_sum`: The sum of the digits of the number.
            - `fun_fact`: A fun fact about the number, or a string indicating that the fact could not be fetched.
    """
    classification = classify_number(number)
    fun_fact = ""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://numbersapi.com/{number}')
            if response.status_code == 200:
                fun_fact = response.text
    except Exception as e:
        fun_fact = "Could not fetch fun fact."
    
    classification["fun_fact"] = fun_fact
    return {
        "number": classification["number"],
        "is_prime": classification["is_prime"],
        "is_perfect": classification["is_perfect"],
        "properties": classification["properties"],
        "digit_sum": classification["digit_sum"],
        "fun_fact": classification["fun_fact"]
    }

@app.exception_handler(ValueError)
async def value_error_handle(request, exc):
    """
    Handles ValueErrors that are raised when the user inputs a number that
    is not a positive integer.

    Args:
        request: The request that caused the error.
        exc: The exception that was raised.

    Returns:
        dict: A dictionary with the following keys:
            - `number`: The number that caused the error.
            - `error`: A boolean indicating that an error occurred.
    """
    return {"number": str(exc), "error":True}