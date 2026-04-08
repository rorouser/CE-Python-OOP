import os
import sys
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import create_retriever_tool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

@tool
def consultar_calendario_examenes(consulta: str) -> str:
    """Consulta fechas de exámenes y entregas del ciclo formativo DAW."""
    calendario = {
        "Proyecto de Desarrollo de Aplicaciones Web": "Entrega final: 15 de junio de 2026",
        "Desarrollo Web en Entorno Cliente": "Examen: 2 de junio de 2026",
        "Desarrollo Web en Entorno Servidor": "Examen: 4 de junio de 2026",
        "Despliegue de Aplicaciones Web": "Examen: 28 de mayo de 2026",
        "Diseño de Interfaces Web": "Examen: 30 de mayo de 2026",
        "Empresa e Iniciativa Emprendedora": "Examen: 26 de mayo de 2026",
    }

    resultados = []
    consulta_lower = consulta.lower()
    for modulo, fecha in calendario.items():
        if any(palabra in consulta_lower for palabra in modulo.lower().split()):
            resultados.append(f"- {modulo}: {fecha}")

    if resultados:
        return "Fechas encontradas:\n" + "\n".join(resultados)

    todas = [f"- {m}: {f}" for m, f in calendario.items()]
    return ("No encontré un módulo específico. Aquí tienes el calendario completo:\n"
            + "\n".join(todas))


def configurar_asistente():

    if not os.path.exists("normativa"):
        os.makedirs("normativa")
        print("Se ha creado la carpeta 'normativa/'. Coloca tus PDFs dentro y ejecuta de nuevo.")
        return None

    pdf_files = [f for f in os.listdir("normativa") if f.endswith(".pdf")]
    if not pdf_files:
        print("La carpeta 'normativa/' está vacía. Añade PDFs y ejecuta de nuevo.")
        return None

    sys.stdout.write("--- Indexando normativa... ")
    sys.stdout.flush()

    loader = PyPDFDirectoryLoader("normativa/")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(chunks, embeddings)
    sys.stdout.write("Listo!\n")

    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    tool_normativa = create_retriever_tool(
        retriever=retriever,
        name="buscador_normativa",
        description=(
            "Busca información oficial sobre el ciclo formativo: módulos, horas, "
            "competencias, contenidos y normativa educativa. "
            "NO usar para fechas de exámenes."
        ),
    )

    tools = [tool_normativa, consultar_calendario_examenes]

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_output_tokens=600,
        max_retries=2,
    )

    system_msg = (
        "Eres un asistente educativo del Ciclo Formativo DAW. Tienes DOS herramientas:\n"
        "1) 'buscador_normativa': para consultar información sobre módulos, horas, "
        "competencias y contenidos del ciclo (basada en PDFs oficiales).\n"
        "2) 'consultar_calendario_examenes': para consultar fechas de exámenes y entregas.\n\n"
        "REGLAS:\n"
        "- Si te preguntan sobre contenido, horas o normativa -> usa 'buscador_normativa'.\n"
        "- Si te preguntan sobre fechas, exámenes o entregas -> usa 'consultar_calendario_examenes'.\n"
        "- Si te preguntan sobre un módulo y luego dicen '¿cuándo es el examen?', "
        "usa el contexto de la conversación para saber de qué módulo hablan.\n"
        "- Para preguntas generales que no requieran herramientas, responde directamente.\n"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    history = ChatMessageHistory()

    return RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )


def limpiar_respuesta(salida_raw):
    if isinstance(salida_raw, list):
        texto = ""
        for item in salida_raw:
            if isinstance(item, dict) and "text" in item:
                texto += item["text"]
            elif isinstance(item, str):
                texto += item
        return texto
    return str(salida_raw)


def chat_asistente():
    asistente = configurar_asistente()
    if not asistente:
        return

    print("\n" + "=" * 50)
    print("  ASISTENTE EDUCATIVO DAW v3.0")
    print("  Con doble herramienta: Normativa + Calendario")
    print("  Escribe 'salir' para finalizar")
    print("=" * 50)
    print()
    print("Prueba estas consultas para validar la memoria:")
    print("  1) '¿Cuántas horas tiene el módulo de Proyecto?'")
    print("  2) '¿Y cuándo es el examen?'  (debe recordar el módulo)")
    print()

    config = {"configurable": {"session_id": "sesion_docente"}}

    while True:
        usuario = input("Tu: ")
        if usuario.lower() in ["salir", "exit"]:
            print("Hasta luego!")
            break

        try:
            response = asistente.invoke({"input": usuario}, config=config)
            respuesta_final = limpiar_respuesta(response["output"])
            print(f"Asistente: {respuesta_final}\n")
        except Exception as e:
            print(f"Error en la comunicación: {e}\n")


if __name__ == "__main__":
    chat_asistente()
