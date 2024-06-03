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

# TODO: user_input dibuat dictionary aja nanti & Subject email bs jadi acuan atau exact
def send_to_openai(user_input):
    promptText = f'Buatkan email tentang {user_input}' 
    # promptText = f"""
    # Buatkan konten email dengan subject dan isi email yang sesuai dengan tujuan berikut:

    # #### Tujuan Email
    # {user_input}

    # #### Audiens
    # Pelanggan setia dan prospektif

    # #### Gaya dan Tone
    # Semi-formal dan informatif

    # #### Poin-Poin Utama
    # 1. Pengumuman acara webinar eksklusif
    # 2. Topik utama yang akan dibahas dalam webinar
    # 3. Pembicara utama dan kredibilitas mereka
    # 4. Tanggal, waktu, dan cara mendaftar untuk webinar
    # 5. Manfaat mengikuti webinar bagi pelanggan
    # 6. Informasi kontak untuk pertanyaan lebih lanjut

    # #### Subject Email
    # Jangan Lewatkan Webinar Eksklusif Kami tentang Strategi Pemasaran Digital!
    # """
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
                response = send_to_openai(user_input)

                def generate():

                    for chunk in response:
                        for choice in chunk.choices:
                            content = choice.delta.content
                            yield content
                        # if 'choices' in chunk:
                        #     print("CHOICES IN CHUNK")
                        #     text = chunk['choices'][0]['delta'].get('content', '')
                        #     yield text
                        # else:
                        #     chunk.choices[0].delta.content

                return StreamingHttpResponse(generate(), content_type='text/plain')

        except Exception as e:
            logger.error("Error processing request: %s", e)
            return JsonResponse({'response': 'Error processing request'}, status=500)
    return JsonResponse({'response': 'Invalid request'}, status=400)