import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# 1. Preparar las credenciales
load_dotenv()
# Asegúrate de que en tu .env la variable se llame GOOGLE_API_KEY
api_key = os.getenv("GOOGLE_API_KEY")

def resumidor_pirata():
    # 2. Inicializar el LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # 3. Definir la "Personalidad" y la "Tarea" (Prompt Engineering)
    system_msg = ("Eres un experto en desarrollo de IT. "
                  "Tu misión es explicar conceptos de desarrollo a diferentes públicos")

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "Explica este error {error_tecnico} a {nivel_del_publico}")
    ])

    # 4. Crear la cadena simple (Chain)
    chain = prompt | llm

    # 5. El texto de prueba
    error_tecnico = "NullPointerException"

    nivel_del_publico = "niño"

    # 6. Ejecutar
    print("--- Procesando botín de información con Gemini... ---\n")
    respuesta = chain.invoke({"error_tecnico": error_tecnico, "nivel_del_publico": nivel_del_publico})

    print(respuesta.content)

if __name__ == "__main__":
    resumidor_pirata()