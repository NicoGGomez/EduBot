import json

class cargarDataset: 
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
