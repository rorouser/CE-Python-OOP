import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

ARCHIVO_PDF = "AI Engineering con Python .pdf"

PREGUNTA = "¿Qué es un embedding y para qué sirve?"


def ejecutar_prueba(nombre_prueba: str, chunk_size: int, chunk_overlap: int):

    print(f"\n{'=' * 60}")
    print(f"  {nombre_prueba}")
    print(f"  chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    print(f"{'=' * 60}")

    # 1. Inicializar componentes
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if not os.path.exists(ARCHIVO_PDF):
        print(f"Error: No se encuentra '{ARCHIVO_PDF}'")
        print("Coloca el PDF en el mismo directorio que este script.")
        return
    loader = PyPDFLoader(ARCHIVO_PDF)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(docs)
    print(f"\nTotal de chunks generados: {chunks.__len__()}")

    vector_store = FAISS.from_documents(chunks, embeddings)

    prompt = ChatPromptTemplate.from_template("""
        Utiliza el siguiente contexto para responder a la pregunta del usuario.
        Si la respuesta no está literal, intenta deducirla basándote en la información disponible.
        Si el contexto no tiene absolutamente nada que ver, indica qué temas se tratan en el texto.
        
        IMPORTANTE: Al final de tu respuesta, indica SIEMPRE en qué página(s) del PDF
        encontraste la información, usando el formato "Fuente: página X".
        
        Contexto: {context}
        Pregunta: {input}
        """)

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(
        vector_store.as_retriever(),
        combine_docs_chain
    )

    print(f"Pregunta: \"{PREGUNTA}\"")
    inicio = time.time()
    response = rag_chain.invoke({"input": PREGUNTA})
    tiempo = time.time() - inicio

    print(f"\n--- CONTEXTO RECUPERADO ({len(response['context'])} fragmentos) ---")
    for i, doc in enumerate(response["context"]):
        pagina = doc.metadata.get("page", "N/A")
        contenido_preview = doc.page_content[:120].replace("\n", " ") + "..."
        print(f"  Fragmento {i + 1} (Pág. {pagina}): {contenido_preview}")

    print(f"\n--- RESPUESTA DE LA IA ---")
    print(response["answer"])

    print(f"\n--- MÉTRICAS ---")
    print(f"Tiempo de respuesta: {tiempo:.2f} segundos")
    print(f"Total chunks en la base: {len(chunks)}")
    print(f"Chunks recuperados: {len(response['context'])}")

    return {
        "nombre": nombre_prueba,
        "chunks_totales": len(chunks),
        "tiempo": tiempo,
        "respuesta": response["answer"]
    }


def detective_de_chunks():

    print("=" * 60)
    print("  EL DETECTIVE DE CHUNKS")
    print("  Analizando el impacto del tamaño de fragmentos en RAG")
    print("=" * 60)

    resultado_a = ejecutar_prueba(
        nombre_prueba="PRUEBA A: Trozos MINÚSCULOS",
        chunk_size=100,
        chunk_overlap=0
    )

    resultado_b = ejecutar_prueba(
        nombre_prueba="PRUEBA B: Trozos ENORMES",
        chunk_size=5000,
        chunk_overlap=500
    )

    if resultado_a and resultado_b:
        print("\n" + "=" * 60)
        print("  COMPARATIVA FINAL")
        print("=" * 60)
        print(f"\n{'Métrica':<25} {'Prueba A (100/0)':<25} {'Prueba B (5000/500)':<25}")
        print("-" * 75)
        print(f"{'Chunks totales':<25} {resultado_a['chunks_totales']:<25} {resultado_b['chunks_totales']:<25}")
        print(f"{'Tiempo (seg)':<25} {resultado_a['tiempo']:<25.2f} {resultado_b['tiempo']:<25.2f}")

        print("\n--- ANÁLISIS ---")
        print("Prueba A (chunks pequeños): Los fragmentos de 100 caracteres son tan cortos")
        print("que la información queda 'rota' entre múltiples trozos. La IA puede dar")
        print("respuestas incoherentes porque no tiene suficiente contexto en cada fragmento.")
        print()
        print("Prueba B (chunks grandes): Los fragmentos de 5000 caracteres capturan más")
        print("contexto, pero incluyen 'paja' (información irrelevante). Además, puede")
        print("tardar más y consumir más tokens de la ventana de contexto del LLM.")
        print()
        print("CONCLUSIÓN: El equilibrio óptimo suele estar entre 500-1500 caracteres")
        print("con un overlap del 10-20% del chunk_size.")


if __name__ == "__main__":
    detective_de_chunks()
