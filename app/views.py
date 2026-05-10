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

            # 1. Maintain memory session
            session_id = request.session.get('chat_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chat_session_id'] = session_id

            # 2. Your n8n URL
            n8n_url = "https://vishnu040.app.n8n.cloud/webhook/9fdcbad6-f4f9-47c8-9acb-bb4b4c7b1711"

            # 3. Request with headers and longer timeout
            # Render servers sometimes need a 'User-Agent' to not look like a bot
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.post(
                n8n_url,
                json={
                    "chatInput": user_message,
                    "sessionId": session_id
                },
                headers=headers,
                timeout=75 # Increased to 75 seconds
            )

            if response.status_code == 200:
                result = response.json()
                reply = result.get('output') or result.get('response') or "Task completed, but no text response."
                return JsonResponse({'reply': reply})
            else:
                return JsonResponse({'reply': f"n8n reported an issue: {response.status_code}. Check if your workflow is ACTIVE."})

        except requests.exceptions.Timeout:
            return JsonResponse({'reply': "Connection Timeout: n8n is taking too long. Try a simpler request."})
        except Exception as e:
            return JsonResponse({'reply': f"Backend Error: {str(e)}"})

    return JsonResponse({'error': 'POST only'}, status=405)