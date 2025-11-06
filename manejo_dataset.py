import json
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
        
    def sacar_signos (self, pregunta):
        texto_limpio = re.sub(r'([aeiouáéíóúrsy])\1{2,}', r'\1', pregunta, flags=re.I)
        pregunta_sin_signo = texto_limpio.replace("?", "").replace("¿", "")
        return pregunta_sin_signo

    def sumar(self, pregunta):
        numeros = [int(n) for n in re.findall(r'\d+', pregunta)]
        for n in numeros :
            total += n

        print(total)
        return f"el resultado es {total}"
        
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