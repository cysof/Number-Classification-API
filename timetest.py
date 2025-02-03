import requests
import time

url = "https://number-classification-api-zf81.onrender.com/api/classify-number?number=371"

start_time = time.time()  # Record start time
response = requests.get(url)
end_time = time.time()  # Record end time

elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

print(f"Response Time: {elapsed_time:.2f} ms")
print("Status Code:", response.status_code)
print("Response:", response.json())
