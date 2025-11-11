from transformers import pipeline

from manejo_dataset import manejoDataset 

class AnalizadorSentimientos: 

    def __init__(self, DATASET_PATH):
        self.manejoDataset = manejoDataset(DATASET_PATH) 
        self.datasetListo = self.manejoDataset.cargar_dataset()
        self.analizador_de_sentimiento = pipeline("sentiment-analysis",
                                     model = "pysentimiento/robertuito-sentiment-analysis")
        print ("Modelo cargado con exito.....")

    def analizar_sentimiento(self, frase):
        try:
            resultados = self.analizador_de_sentimiento(frase)

            if not resultados or not isinstance(resultados, list):
                return "⚠️ No se pudo analizar el sentimiento."

            sentimiento = resultados[0]["label"]

            if sentimiento == "POS":
                respuesta = self.manejoDataset.buscar_en_dataset(frase, self.datasetListo) or "😊 Me alegra escuchar eso."
            elif sentimiento == "NEG":
                respuesta = "😟 ¿Estás bien? Si necesitas ayuda te recomiendo hablar con un adulto o maestro."
            elif sentimiento == "NEU":
                respuesta = self.manejoDataset.buscar_en_dataset(frase, self.datasetListo) or "¿Podrias repetir la pregunta? 🌭"
            else:
                respuesta = "❓ No pude entender el mensaje."

            return respuesta

        except Exception as e:
            print(f"Error en analizador_sentimiento: {e}")
            return "⚠️ Ocurrió un error al analizar el sentimiento."
