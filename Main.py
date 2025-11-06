import telebot
from transformers import pipeline
import os
import json
import time
from groq import Groq
import base64
from PIL import Image
import re
from typing import Optional
from dotenv import load_dotenv

from analizador_audio import AnalizadorAudio

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("Cargando el modelo de analisis de sentimiento...")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

cliente_groq = Groq(api_key=GROQ_API_KEY)

GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

DATASET_PATH = 'dataset.json'

analizador_de_sentimiento = pipeline("sentiment-analysis",
                                     model = "pysentimiento/robertuito-sentiment-analysis")
print ("Modelo cargado con exito.....")

#instanciar el objeto === crear el bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

analizar_audio = AnalizadorAudio.__init__(cliente_groq, bot, DATASET_PATH)

# Función para cargar el dataset desde el archivo JSON
def cargar_dataset():
	try:
		# Abre el archivo dataset.json en modo lectura y codificación utf-8
		with open(DATASET_PATH, 'r', encoding='utf-8') as f:
			# Carga y retorna el contenido como una lista de diccionarios
			return json.load(f)
	except Exception:
		# Si hay error (por ejemplo, el archivo no existe), retorna una lista vacía
		return []
      
dataset = cargar_dataset()

def sacar_signos (pregunta):
    pregunta_sin_signo = pregunta.replace("?", "").replace("¿", "")
    return pregunta_sin_signo

def sumar(pregunta):
    numeros = [int(n) for n in re.findall(r'\d+', pregunta)]
    for n in numeros :
         total += n

    print(total)
    return f"el resultado es {total}"

def imagen_a_base64(ruta_o_bytes_imagen):
    """Convierte una imagen a base64 para enviarla a Groq"""
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')
    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None
    
# Manejador para imágenes
@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa las imágenes enviadas por el usuario"""
    try:
        bot.reply_to(mensaje, "📸 He recibido tu imagen. Analizándola... ⏳")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        imagen_base64 = imagen_a_base64(archivo_descargado)

        if not imagen_base64:
            bot.reply_to(mensaje, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return

        descripcion = describir_imagen_con_groq(imagen_base64)

        if descripcion:
            respuesta = f"🤖 *Descripción de la imagen:*\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

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

# Función para describir imagen con Groq
def describir_imagen_con_groq(imagen_base64):
    """Envía la imagen a Groq y obtiene la descripción"""
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, describe esta imagen de manera detallada y clara en español. Incluye todos los elementos importantes que veas, colores, objetos, personas, acciones, emociones, y cualquier detalle relevante que puedas observar."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagen_base64}"
                            }
                        }
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=1000
        )
        return completado_chat.choices[0].message.content
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None

def analizador_sentimiento(frase):
    try:
        resultados = analizador_de_sentimiento(frase)
        if not resultados or not isinstance(resultados, list):
            return "⚠️ No se pudo analizar el sentimiento."

        sentimiento = resultados[0]["label"]

        if sentimiento == "POS":
            respuesta = buscar_en_dataset(frase, dataset) or "😊 Me alegra escuchar eso."
        elif sentimiento == "NEG":
            respuesta = "😟 ¿Estás bien? Si querés puedo ayudarte con algo."
        elif sentimiento == "NEU":
            respuesta = buscar_en_dataset(frase, dataset) or "Ok, lo entiendo."
        else:
            respuesta = "❓ No pude determinar el sentimiento."

        return respuesta

    except Exception as e:
        print(f"Error en analizador_sentimiento: {e}")
        return "⚠️ Ocurrió un error al analizar el sentimiento."

def buscar_en_dataset(pregunta, dataset):
    # Normaliza la pregunta (quita espacios y pasa a minúsculas)
    pregunta = pregunta.strip().lower()
    pregunta_sin_signo = sacar_signos(pregunta)
    if "cuanto es" in pregunta and "mas" in pregunta: 
         if "+" in pregunta : 
              return sumar(pregunta)

    # Recorre cada elemento del dataset
    for item in dataset:
        # Compara la pregunta del usuario con la del dataset (normalizada)
        if sacar_signos(item['pregunta'].strip().lower()) == pregunta_sin_signo:
            # Si hay coincidencia exacta, retorna la respuesta
            return item['respuesta']

    # Si no encuentra coincidencia, retorna None
    return None

@bot.message_handler(commands=["start","help","pepito"])
def cmd_welcome(message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    bot.reply_to(message,"Bienvenido, en que puedo ayudarte? Tengo mucha informacion sobre temas de escolar.")

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
    # response = get_groq_response(transcription)
    response = analizar_audio.get_groq_response(transcription)

    if response:
        bot.reply_to(message, response)
    else:
        error_message = """❌ Lo siento, hubo un error al procesar tu consulta.
Por favor, intenta nuevamente o contáctanos:
📧 info@codificardev.com.ar"""
        bot.reply_to(message, error_message)

@bot.message_handler(func=lambda message: True)
def responder(message):
    pregunta = message.text
    resultado = analizador_sentimiento(pregunta)
    bot.reply_to(message, resultado)
if __name__=="__main__":
    print("Bot ejecutado!")
    bot.infinity_polling()

