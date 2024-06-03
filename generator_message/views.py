import openai
import json
from decouple import config
import logging
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

logger = logging.getLogger(__name__)

# Set OpenAI API key and initialize OpenAI client
client = openai.OpenAI(api_key=config('OPENAI_API_KEY'))


@staff_member_required(login_url='/auth/login/')
def generator_view(request):
    return render(request, "generator.html")

def sendMessage(prompt):
    promptText = f"""
    Buatkan sebuah materi untuk konten Instagram yang singkat tentang {prompt}
    dalam format list HTML.
    Setiap sub-judul dan list ditebalkan menggunakan bold, serta diberikan baris baru menggunakan <br> jadi lebih rapih. Berikan juga caption di akhir dengan 20 hashtags
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": promptText}
        ],
        stream=True
    )
    return response


def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message')
            if user_input:
                response = sendMessage(user_input)

                def generate():
                    for chunk in response:
                        if 'choices' in chunk:
                            text = chunk['choices'][0]['delta'].get('content', '')
                            yield text

                return StreamingHttpResponse(generate(), content_type='text/plain')

        except Exception as e:
            logger.error("Error processing request: %s", e)
            return JsonResponse({'response': 'Error processing request'}, status=500)
    return JsonResponse({'response': 'Invalid request'}, status=400)