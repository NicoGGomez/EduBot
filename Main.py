import telebot
import os
import time
from groq import Groq
from dotenv import load_dotenv
import json

# datatime

from analizador_audio import AnalizadorAudio
from analizador_imagenes import AnalizadorImagen
from analizador_sentimientos import AnalizadorSentimientos

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("Cargando el modelo de analisis de sentimiento...")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

cliente_groq = Groq(api_key=GROQ_API_KEY)

GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

DATASET_PATH = 'dataset.json'

#instanciar el objeto === crear el bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

analizar_audio = AnalizadorAudio(cliente_groq, bot, DATASET_PATH)
analizar_img = AnalizadorImagen(cliente_groq, bot, DATASET_PATH)
analizador_sentimiento = AnalizadorSentimientos(DATASET_PATH)
    
# Manejador para imágenes
@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa las imágenes enviadas por el usuario"""
    try:
        bot.reply_to(mensaje, "📸 He recibido tu imagen. Analizándola... ⏳")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        imagen_base64 = analizar_img.imagen_a_base64(archivo_descargado)

        if not imagen_base64:
            bot.reply_to(mensaje, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return

        descripcion = analizar_img.describir_imagen_con_groq(imagen_base64)

        if descripcion:
            respuesta = f"🤖 *Descripción de la imagen:*\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

@bot.message_handler(commands=["Comenzar"])
def cmd_welcome(message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    bot.reply_to(message,"Bienvenido, en que puedo ayudarte? Tengo mucha informacion sobre temas de escuela primaria.")

@bot.message_handler(commands=["Ayuda"])
def cmd_help(message):
    bot.send_chat_action(message.chat.id,"typing")
    time.sleep(1)
    bot.reply_to(message,"Para comenzar a usar el bot, debes usar el comand: '/Comenzar'.")

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: telebot.types.Message):
    # Enviar mensaje de "escribiendo..."
    bot.send_chat_action(message.chat.id, 'typing')

    # Transcribir el mensaje de voz usando Groq
    transcription = analizar_audio.transcribe_voice_with_groq(message)

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
    resultado = analizador_sentimiento.analizar_sentimiento(pregunta)
    bot.reply_to(message, resultado)
if __name__=="__main__":
    print("Bot ejecutado!")
    bot.infinity_polling()


