import requests
from django.shortcuts import render
from django.http import JsonResponse
import json
import time

# Create your views here.

def index(request):
    return render(request, 'index.html')

# dashboard/views.py

def chat_with_agent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            time.sleep(2)  # small delay to avoid rate limit

            # Ensure this is the PRODUCTION URL (no "-test" in the link)
            n8n_url = "https://vishnu040.app.n8n.cloud/webhook/9fdcbad6-f4f9-47c8-9acb-bb4b4c7b1711"

            response = requests.post(n8n_url, json={"chatInput": user_message})

            # Check if n8n actually sent JSON
            try:
                result = response.json()
                reply = reply = (
                    result.get('output')
                    or result.get('response')
                    or result.get('message')
                    or "No valid response"
                )
            except ValueError:
                # This happens if n8n sends a 404 or a text error
                reply = f"The Agent sent a non-JSON response: {response.text[:100]}"

            return JsonResponse({'reply': reply})

        except Exception as e:
            return JsonResponse({'reply': f"Django Error: {str(e)}"})