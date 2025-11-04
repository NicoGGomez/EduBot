def get_groq_response(user_message: str) -> Optional[str]:
    try: 
        system_prompt = f"""Eres el asistente virtual de Edubot. Tu tarea es responder preguntas basándote en la siguiente información de la empresa.

Datos de la empresa:
{json.dumps(dataset)}
 
lista completa que aparece en el dataset para ver ejemplos de páginas."""
        chat_completion = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model = "llama-3.3-70b-versatile",
            temperature = 0.3,
            max_tokens = 500
        )
        
        return chat_completion.choices[0].message.content.strip()


    except Exception as e:
        print(f"Error al obtener la respuesta: {str(e)}")
        return None

def transcribe_voice_with_groq(message: telebot.types.Message) -> Optional[str]:
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        #guardar el archivo de forma temporal
        with open(temp_file, "wb") as f:
            f.write(downloaded_file)
        with open(temp_file, "rb") as file:
            transcription = cliente_groq.audio.transcriptions.create(
                file = (temp_file, file.read()),
                model = "whisper-large-v3-turbo",
                prompt = "Especificar contexto o pronunciacion",
                response_format = "json",
                language = "es",
                temperature = 1
            )
        os.remove(temp_file)

        
        return transcription.text

    except Exception as e:
        print(f"Error al transcribir; {str(e)}")
        return None

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: telebot.types.Message):
    if not dataset:
        bot.reply_to(message, "Error al cargar los datos de la empresa. Por favor, intente más tarde.")
        return
    
    # Enviar mensaje de "escribiendo..."
    bot.send_chat_action(message.chat.id, 'typing')

    # Transcribir el mensaje de voz usando Groq
    transcription = transcribe_voice_with_groq(message)

    if not transcription:
        bot.reply_to(message, "❌ Lo siento, no pude transcribir el audio. Por favor, intenta de nuevo.")
        return
    
    # Obtener respuesta de Groq usando la transcripción como input
    response = get_groq_response(transcription)

    if response:
        bot.reply_to(message, response)
    else:
        error_message = """❌ Lo siento, hubo un error al procesar tu consulta.
Por favor, intenta nuevamente o contáctanos:
📧 info@codificardev.com.ar"""
        bot.reply_to(message, error_message)