from typing import Optional
from groq import Groq
import telebot
import base64
import json

from analizadores.manejo_dataset import manejoDataset 

class AnalizadorImagen:
     
    def __init__(self, cliente_groq, bot, DATASET_PATH):
        self.cliente_groq = cliente_groq
        self.bot = bot
        self.procesarDataset = manejoDataset(DATASET_PATH) 
        self.datasetListo = self.procesarDataset.cargar_dataset()

    def imagen_a_base64(self, ruta_o_bytes_imagen):
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

    def describir_imagen_con_groq(self, imagen_base64):
        """Envía la imagen a Groq y obtiene la descripción"""
        try:
            completado_chat = self.cliente_groq.chat.completions.create(
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
        