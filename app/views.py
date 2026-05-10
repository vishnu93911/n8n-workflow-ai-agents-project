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
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Session Management
            session_id = request.session.get('chat_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chat_session_id'] = session_id

            n8n_url = "https://vishnu040.app.n8n.cloud/webhook/9fdcbad6-f4f9-47c8-9acb-bb4b4c7b1711"

            # Call n8n with a longer timeout (AI can be slow)
            response = requests.post(
                n8n_url,
                json={
                    "chatInput": user_message,
                    "sessionId": session_id
                },
                timeout=60 
            )

            if response.status_code == 200:
                result = response.json()
                # n8n agents usually return 'output'
                reply = result.get('output') or result.get('response') or result.get('message') or "Task completed, but no text response received."
                return JsonResponse({'reply': reply})
            else:
                return JsonResponse({'reply': f"Agent is busy (Error {response.status_code}). Please try again shortly."})

        except requests.exceptions.Timeout:
            return JsonResponse({'reply': "The AI Agent took too long to respond. Please try again."})
        except Exception as e:
            # This will show the actual error message in your UI instead of a 500 error
            return JsonResponse({'reply': f"System Error: {str(e)}"})

    return JsonResponse({'error': 'POST only'}, status=405)