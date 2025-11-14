import json
import re
import unicodedata
import re

class manejoDataset: 
    def __init__(self, dataset):
        self.dataset = dataset

    def cargar_dataset(self):
        try:
            # Abre el archivo dataset.json en modo lectura y codificación utf-8
            with open(self.dataset, 'r', encoding='utf-8') as f:
                # Carga y retorna el contenido como una lista de diccionarios
                return json.load(f)
        except Exception:
            # Si hay error (por ejemplo, el archivo no existe), retorna una lista vacía
            return []

    def sacar_signos(self, pregunta):
        # Normaliza el texto para eliminar acentos
        texto_normalizado = unicodedata.normalize('NFD', pregunta)
        texto_sin_acentos = texto_normalizado.encode('ascii', 'ignore').decode('utf-8')
        
        # Elimina signos de interrogación
        texto_sin_signo = texto_sin_acentos.replace("?", "").replace("¿", "")
        
        # Reduce letras repetidas (ej: holaaa -> hola)
        texto_limpio = re.sub(r'([aeiouyrs])\1{2,}', r'\1', texto_sin_signo, flags=re.I)
        
        return texto_limpio

    def extraer_pregunta(self, texto):
        texto_lower = texto.lower()
        
        palabras_interrogativas = r"(qué|como|cómo|cuándo|cuando|dónde|donde|por qué|porque|quién|cual|cuáles)"
        
        match = re.search(rf"({palabras_interrogativas}[^?.!]*)", texto_lower)
        if match:
            return match.group(1).strip()

        match = re.search(r"(que [^?.!]*)", texto_lower)
        if match:
            return match.group(1).strip()
        
        return None
        
    def buscar_en_dataset(self, pregunta, dataset):
        # Normaliza la pregunta (quita espacios y pasa a minúsculas)
        pregunta = pregunta.strip().lower()
        pregunta_sin_signo = self.sacar_signos(pregunta)
        if "cuanto es" in pregunta and "mas" in pregunta: 
            if "+" in pregunta : 
                return self.sumar(pregunta)

        # Recorre cada elemento del dataset
        for item in dataset:
            # Compara la pregunta del usuario con la del dataset (normalizada)
            if self.sacar_signos(item['pregunta'].strip().lower()) == pregunta_sin_signo:
                # Si hay coincidencia exacta, retorna la respuesta
                return item['respuesta']

        # Si no encuentra coincidencia, retorna None
        return None
    