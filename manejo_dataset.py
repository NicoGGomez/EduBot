import unicodedata
import json
import re

class manejoDataset: 

    def __init__(self, dataset):
        self.dataset = dataset

    def cargar_dataset(self):
        try:
            with open(self.dataset, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def sacar_signos(self, pregunta):
        texto_normalizado = unicodedata.normalize('NFD', pregunta)
        texto_sin_acentos = texto_normalizado.encode('ascii', 'ignore').decode('utf-8')
        
        texto_sin_signo = texto_sin_acentos.replace("?", "").replace("¿", "")
        
        texto_limpio = re.sub(r'([aeiouyrs])\1{2,}', r'\1', texto_sin_signo, flags=re.I)
        
        return texto_limpio

    def extraer_pregunta(self, texto):
        texto_lower = texto.lower()
        
        palabras_interrogativas = r"(qué|que|cuanto|como|cómo|cuándo|cuando|dónde|donde|por qué|porque|quién|cual|cuáles)"
        
        match = re.search(rf"({palabras_interrogativas}[^?.!]*)", texto_lower)
        if match:
            return match.group(1).strip()

        match = re.search(r"(que [^?.!]*)", texto_lower)
        if match:
            return match.group(1).strip()
        
        return None
        
    def buscar_en_dataset(self, pregunta, dataset):
        pregunta = pregunta.strip().lower()
        pregunta_sin_signo = self.sacar_signos(pregunta)
        if "cuanto es" in pregunta and "mas" in pregunta: 
            if "+" in pregunta : 
                return self.sumar(pregunta)

        for item in dataset:
            if self.sacar_signos(item['pregunta'].strip().lower()) == pregunta_sin_signo:
                return item['respuesta']

        return None
    