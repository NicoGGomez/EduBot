# 🧠 EduBot (Asistente Escolar IA)

## 📘 Descripción del Proyecto
**EduBot** es un proyecto desarrollado en **Python** como parte del curso de *Inteligencia Artificial de Samsung Innovation Campus*.  
Este bot está diseñado para ayudar a **estudiantes de nivel primario** en materias básicas como **Matemática, Lengua, Ciencias y más**, brindando explicaciones simples, ejercicios interactivos y acompañamiento educativo mediante **técnicas de Procesamiento de Lenguaje Natural (NLP)**.

El bot utiliza el framework **TeleBot** para la interacción en Telegram y modelos de inteligencia artificial de **Groq** y **Hugging Face** para analizar texto, imágenes y audios.

---

## 🧩 Arquitectura del Proyecto

El proyecto implementa **Programación Orientada a Objetos (POO)** y se organiza en cuatro clases principales:

- **🔹 manejoDataset** → Encargada de cargar, limpiar y buscar información dentro del dataset principal (`dataset.json`).
- **🔹 AnalizadorImagen** → Analiza y describe imágenes utilizando modelos de visión de Groq.
- **🔹 AnalizadorAudio** → Transcribe audios y genera respuestas educativas usando reconocimiento de voz.
- **🔹 AnalizadorSentimientos** → Analiza el tono emocional del mensaje del usuario y responde de manera empática o contextual.

---

## ⚙️ Método de Uso

### 1️⃣ Configuración inicial
Para utilizar el bot, es necesario crear un archivo **`.env`** en la raíz del proyecto con las siguientes variables:

**`
TELEGRAM_TOKEN="tu_token_de_telegram"
GROQ_API_KEY="tu_api_key_de_groq"
`**

### 2️⃣ Ejecución del bot

Ejecutá el archivo principal desde la terminal con:

### python main.py

El bot se conectará automáticamente a Telegram y comenzará a procesar mensajes, imágenes y audios.

### 💬 Comandos disponibles

/Comenzar → Inicia la interacción con el bot.

/Ayuda → Explica cómo comenzar a usar EduBot.

### 🧠 Ejemplos de preguntas

Pregunta	Respuesta esperada
¿Qué colores forman el violeta?	El azul y el rojo.
¿Qué necesitan las plantas para vivir?	Las plantas necesitan sol, agua, aire y tierra para crecer.
¿Cuántos lados tiene un triángulo?	Un triángulo tiene tres lados.
¿Qué es EduBot?	EduBot es un asistente educativo creado para ayudar a niños de primaria a aprender de forma divertida e interactiva, haciendo preguntas, dando pistas y enseñando curiosidades.

### 🧠 Tecnologías utilizadas

Python 3.10+
TeleBot (pyTelegramBotAPI)
Groq API
Hugging Face Transformers
dotenv
JSON

### 🚀 Objetivo Educativo

El propósito de EduBot es acercar la inteligencia artificial al aprendizaje infantil, promoviendo el pensamiento lógico y la curiosidad de los niños, con un lenguaje claro y adaptado a su nivel escolar.

### 👨‍💻 Autores 

Desarrollado por: 

### Nicolás Gómez - anelecarg@gmail.com
### Agustina Fennema - agusfennema@gmail.com
### Iñaki Boixados - ilboixa2@gmail.com
