import requests
import json
import uuid
import time
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def chat_with_agent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Session ID for memory isolation
            session_id = request.session.get('chat_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chat_session_id'] = session_id

            n8n_url = "https://vishnu040.app.n8n.cloud/webhook/9fdcbad6-f4f9-47c8-9acb-bb4b4c7b1711"

            time.sleep(1)

            response = requests.post(
                n8n_url,
                json={
                    "chatInput": user_message,
                    "sessionId": session_id
                },
                timeout=45
            )

            try:
                result = response.json()
                reply = (
                    result.get('output')
                    or result.get('response')
                    or result.get('message')
                    or "I was unable to complete that. Please try again."
                )
            except ValueError:
                reply = f"Agent error: {response.text[:200]}"

            return JsonResponse({'reply': reply})

        except requests.exceptions.Timeout:
            return JsonResponse({'reply': 'Request timed out. Please try again.'})
        except Exception as e:
            return JsonResponse({'reply': f'Error: {str(e)}'})

    return JsonResponse({'error': 'POST only'}, status=405)