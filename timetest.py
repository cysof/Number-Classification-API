import requests
import time

url = "http://127.0.0.1:8000/api/classify-number?number=371"

start_time = time.time()  # Record start time
response = requests.get(url)
end_time = time.time()  # Record end time

elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

print(f"Response Time: {elapsed_time:.2f} ms")
print("Status Code:", response.status_code)
print("Response:", response.json())
