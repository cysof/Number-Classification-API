# Number Classification API

## Overview
The Number Classification API classifies numbers based on their mathematical properties and provides a fun fact about them.

## Features
- Determines if a number is prime, perfect, or an Armstrong number.
- Identifies number properties (odd, even, Armstrong, etc.).
- Computes the sum of digits.
- Fetches a fun fact from the Numbers API.
- Supports CORS for public access.
- Returns structured JSON responses with appropriate HTTP status codes.

## Technologies Used
- **FastAPI** – High-performance API framework
- **Uvicorn** – ASGI server for running FastAPI
- **httpx** – For making asynchronous HTTP requests
- **Python** – The programming language used

## Installation & Setup

### Prerequisites
- Python 3.8+
- Pip

### Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/cysof/Number-Classification-API.git
   cd number-classification-api
   ```
2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```
5. **Access the API**
   - Open `http://127.0.0.1:8000/docs` for interactive API documentation.
   - Open `http://127.0.0.1:8000/api/classify-number?number=371` for a sample response.
   - Open `https://number-classification-api-zf81.onrender.com/api/classify-number`

## API Endpoints

### **GET /api/classify-number**
#### **Query Parameters:**
- `number` (integer) - The number to classify.

#### **Response Format (200 OK)**
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```
#### **Response Format (400 Bad Request)**
```json
{
    "number": "invalid",
    "error": true
}
```

## Deployment


### **Deploy on Render**
1. Create a **new web service** on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Use the following **build and start command**:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
4. Deploy and get your public API URL.

## Testing
- Use **Postman** or `curl` to send requests and verify responses.
- Run `pytest` for automated tests (if test cases are included).

## License
MIT License

## Author
Developed by **Ogbu Cyprian**

# Number-Classification-API
