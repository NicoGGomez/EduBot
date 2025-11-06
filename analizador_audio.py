from typing import Optional
from groq import Groq
import telebot
import os
import json

from manejo_dataset import manejoDataset 

class AnalizadorAudio():

    def __init__(self, cliente_groq, bot, DATASET_PATH):
        self.cliente_groq = cliente_groq
        self.bot = bot
        self.procesarDataset = manejoDataset(DATASET_PATH) 
        self.datasetListo = self.procesarDataset.cargar_dataset()

    def get_groq_response(self, user_message: str) -> Optional[str]:
        try: 
            system_prompt = f"""Eres el asistente virtual de Edubot. Tu tarea es responder preguntas basándote en la siguiente información de la empresa.

    Datos de la empresa:
    {json.dumps(self.datasetListo)}
    
    lista completa que aparece en el dataset para ver ejemplos de páginas."""
            chat_completion = self.cliente_groq.chat.completions.create(
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

    def transcribe_voice_with_groq(self, message: telebot.types.Message) -> Optional[str]:
        try:
            file_info = self.bot.get_file(message.voice.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            temp_file = "temp_voice.ogg"

            #guardar el archivo de forma temporal
            with open(temp_file, "wb") as f:
                f.write(downloaded_file)
            with open(temp_file, "rb") as file:
                transcription = self.cliente_groq.audio.transcriptions.create(
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
