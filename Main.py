from dotenv import load_dotenv
from groq import Groq
import telebot
import time
import json
import os

from analizador_audio import AnalizadorAudio
from analizador_imagenes import AnalizadorImagen
from analizador_sentimientos import AnalizadorSentimientos
from manejo_dataset import manejoDataset

# -------------------------------
# Carga de variables de entorno
# -------------------------------

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("Cargando el modelo de analisis de sentimiento...")

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# -------------------------------
# Inicialización de clientes y paths
# -------------------------------

cliente_groq = Groq(api_key=GROQ_API_KEY)

GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

DATASET_PATH = 'dataset.json'
DATASET_PATH_CONCRETAS = 'dataset_concreto.json'

# -------------------------------
# Inicialización del bot y analizadores
# -------------------------------

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

analizar_audio = AnalizadorAudio(cliente_groq, bot, DATASET_PATH)
analizar_img = AnalizadorImagen(cliente_groq, bot, DATASET_PATH)
analizador_sentimiento = AnalizadorSentimientos(DATASET_PATH)

# -------------------------------
# Comandos del bot
# -------------------------------

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

# -------------------------------
# Manejo de imágenes
# -------------------------------

@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa las imágenes enviadas por el usuario"""
    try:
        descripcion = analizar_img.procesarFoto(mensaje)

        if descripcion:
            respuesta = f"🤖 *Descripción de la imagen:*\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")

# -------------------------------
# Manejo de mensajes de voz
# -------------------------------

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: telebot.types.Message):
    bot.send_chat_action(message.chat.id, 'typing')

    transcription = analizar_audio.transcribe_voice_with_groq(message)

    if not transcription:
        bot.reply_to(message, "❌ Lo siento, no pude transcribir el audio. Por favor, intenta de nuevo.")
        return
    
    response = analizar_audio.get_groq_response(transcription)

    if response:
        bot.reply_to(message, response)
    else:
        error_message = """❌ Lo siento, hubo un error al procesar tu consulta.
Por favor, intenta nuevamente o contáctanos:
📧 info@codificardev.com.ar"""
        bot.reply_to(message, error_message)

# -------------------------------
# Manejo de mensajes de texto
# -------------------------------

preguntaAnterior = ''

@bot.message_handler(func=lambda message: True)
def responder(message):
    global preguntaAnterior
    pregunta = message.text
    if pregunta == preguntaAnterior:
        manDataset = manejoDataset(DATASET_PATH_CONCRETAS)
        dataset = manDataset.cargar_dataset()
        resultado = manDataset.buscar_en_dataset(pregunta, dataset)
    else:
        preguntaAnterior = pregunta
        resultado = analizador_sentimiento.analizar_sentimiento(pregunta)
    bot.reply_to(message, resultado)
if __name__=="__main__":
    print("Bot ejecutado!")
    bot.infinity_polling()


