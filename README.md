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

Creacion de variables

Para crear el token de telgram dirigirse al enlace: https://web.telegram.org, crear un chat con botFather y enviar el comando /newBot, una vez creado tendras tu token

Para crear la key de groq, es necesario ir a https://console.groq.com/keys

### 2️⃣ Instalacion de dependecias para el correcto uso del bot

para que funcione el bot, debe crearse un nuevo entorno y mover e instalar las dependecias listadas en el requiriments.txt

### 3️⃣ Ejecución del bot

Ejecutá el archivo principal desde la terminal con:

### python Main.py o python3 Main.py

El bot se conectará automáticamente a Telegram y comenzará a procesar mensajes, imágenes y audios.

### 💬 Comandos disponibles

/Comenzar → Inicia la interacción con el bot.

/Ayuda → Explica cómo comenzar a usar EduBot.

### 🧠 Ejemplos de preguntas

- Analizis de imagen
Subir imagen cualquiera, puede ser una del siguiente drive: https://drive.google.com/drive/u/0/folders/1LUgEQFJMOe1SA4jpnc98yawUEHW2Yk-c .
El bot deberia describir la imagen.

imagen subida: "Alien.png"
ejemplo de respuesta: "La imagen muestra un alienígena de color verde. El alienígena tiene la cabeza grande y redonda, con ojos grandes y redondos que parecen tener una forma..."

- Analizis de audio
Preguntas de ejemlo:
¿Qué colores forman el violeta?	El azul y el rojo.
¿Qué necesitan las plantas para vivir?	Las plantas necesitan sol, agua, aire y tierra para crecer.
¿Qué es EduBot?	EduBot es un asistente educativo creado para ayudar a niños de primaria a aprender de forma divertida e interactiva, haciendo preguntas, dando pistas y enseñando curiosidades.

En caso de no encontrar la respuesta en el dataset, el bot le pedira a groq informacion. 

- Analizis de Mensaje
Preguntas de ejemplo:
¿Cuántos lados tiene un triángulo?	Un triángulo tiene tres lados.
¿Qué colores tiene la bandera argentina? La bandera argentina tiene los colores celeste y blanco, con un sol en el centro.
¿Cuántas vocales tiene el abecedario? Tiene cinco vocales: A, E, I, O y U.

El bot formatea el mensaje entrante quitandole signos de pregunta, acentos, dejando el texto en minsuculas para que corresponda correctamente con la informacion del dataset.

- Analizis de sentimientos
El bot analiza tus sentimientos dependiendo el tono del mensaje q mandes.
Ejemplo:
no me saleeee. **😟 ¿Estás bien? Si querés puedo ayudarte con algo.**

Estoy mal. 

### 🧠 Tecnologías utilizadas

- Python 3.10+
- TeleBot (pyTelegramBotAPI)
- Groq API
- Transformers
- dotenv
- JSON

### 🚀 Objetivo Educativo

El propósito de EduBot es acercar la inteligencia artificial al aprendizaje infantil, promoviendo el pensamiento lógico y la curiosidad de los niños, con un lenguaje claro y adaptado a su nivel escolar.

### 👨‍💻 Autores 

Desarrollado por: 

**Nicolás Gómez - anelecarg@gmail.com**
**Agustina Fennema - agusfennema@gmail.com**
**Iñaki Boixados - ilboixa2@gmail.com**
