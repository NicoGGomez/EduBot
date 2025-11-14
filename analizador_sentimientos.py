from transformers import pipeline

from manejo_dataset import manejoDataset 

class AnalizadorSentimientos: 

    def __init__(self, DATASET_PATH):
        self.manejoDataset = manejoDataset(DATASET_PATH) 
        self.datasetListo = self.manejoDataset.cargar_dataset()
        self.analizador_de_sentimiento = pipeline(
            "sentiment-analysis",
            model = "pysentimiento/robertuito-sentiment-analysis")
        print ("Modelo cargado con exito.....")

    def analizar_sentimiento(self, frase):
        try:
            resultados = self.analizador_de_sentimiento(frase)

            if not resultados or not isinstance(resultados, list):
                return "⚠️ No se pudo analizar el sentimiento."

            sentimiento = resultados[0]["label"]

            if sentimiento == "POS":
                pregunta = self.manejoDataset.extraer_pregunta(frase)
                respuestaTemp = self.manejoDataset.buscar_en_dataset(pregunta, self.datasetListo)
                if respuestaTemp is None:
                    respuesta = "😊 Me alegra escuchar eso."
                else :
                    respuesta = respuestaTemp 
            elif sentimiento == "NEG":
                pregunta = self.manejoDataset.extraer_pregunta(frase)
                if pregunta is None:
                    respuestaTemp = self.manejoDataset.buscar_en_dataset(frase, self.datasetListo)
                else:
                    respuestaTemp = self.manejoDataset.buscar_en_dataset(pregunta, self.datasetListo)
        
                if respuestaTemp is None:
                    respuesta = "😟 Si necesitas ayuda te recomiendo hablar con un adulto o maestro."
                else :
                    respuesta = "tranqui yo te ayudo, la respuesta es: " + respuestaTemp 
            elif sentimiento == "NEU":
                pregunta = self.manejoDataset.extraer_pregunta(frase)
                if pregunta is None:
                    respuestaTemp = self.manejoDataset.buscar_en_dataset(frase, self.datasetListo)
                else:
                    respuestaTemp = self.manejoDataset.buscar_en_dataset(pregunta, self.datasetListo)
                    
                if respuestaTemp is None:
                    respuesta = "No tengo informacion sobre eso 😞🌭"
                else :
                    respuesta = respuestaTemp or "No tengo información sobre eso 😞🌭"
            else:
                respuesta = "❓ No pude entender el mensaje."

            return respuesta

        except Exception as e:
            print(f"Error en analizador_sentimiento: {e}")
            return "⚠️ Ocurrió un error al analizar el sentimiento."
