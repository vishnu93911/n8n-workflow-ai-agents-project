import requests
import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def chat_with_agent(request):
    if request.method == "POST":
        try:
            # 1. Parse Input
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # 2. Get/Create Session for AI Memory
            session_id = request.session.get('chat_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chat_session_id'] = session_id

            # 3. Call n8n Webhook
            n8n_url = "https://vishnu040.app.n8n.cloud/webhook/9fdcbad6-f4f9-47c8-9acb-bb4b4c7b1711"
            
            response = requests.post(
                n8n_url,
                json={
                    "chatInput": user_message,
                    "sessionId": session_id
                },
                timeout=55  # Increased timeout for AI processing
            )

            # 4. Handle Response
            if response.status_code == 200:
                result = response.json()
                # Check for various common n8n return keys
                reply = result.get('output') or result.get('response') or result.get('message') or "Action completed."
                return JsonResponse({'reply': reply})
            
            elif response.status_code == 429:
                return JsonResponse({'reply': "Error: Google Gemini is busy (Rate Limit). Please wait 1 minute and try again."})
            
            else:
                return JsonResponse({'reply': f"Agent service error (Status {response.status_code})."})

        except requests.exceptions.Timeout:
            return JsonResponse({'reply': 'The agent took too long to respond. Please try a simpler request.'})
        except Exception as e:
            # This prints the error in your terminal so you can see it
            print(f"Server Error: {str(e)}")
            return JsonResponse({'reply': f"Internal Server Error: {str(e)}"})

    return JsonResponse({'error': 'POST only'}, status=405)