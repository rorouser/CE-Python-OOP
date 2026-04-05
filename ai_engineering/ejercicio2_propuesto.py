
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def filtro_candidatos():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    perfiles = [
        "Desarrollador backend senior con 5 años de experiencia en Python, Django y APIs REST. "
        "Experto en arquitectura de microservicios, lógica de servidor y bases de datos PostgreSQL.",

        "Diseñadora gráfica especializada en interfaces móviles y experiencia de usuario (UX). "
        "Domina Figma, Adobe XD y prototipado interactivo.",

        "Ingeniero DevOps con experiencia en Docker, Kubernetes y pipelines CI/CD. "
        "Gestión de infraestructura cloud en AWS y despliegue de aplicaciones.",

        "Data Scientist con dominio de Machine Learning, TensorFlow y análisis estadístico. "
        "Experiencia en modelos predictivos y visualización de datos con Python.",

        "Desarrolladora fullstack junior con conocimientos de Node.js, Express y MongoDB. "
        "Experiencia creando APIs y lógica de negocio para aplicaciones web.",

        "Camarero profesional con 8 años de experiencia sirviendo mesas en restaurantes "
        "de alta cocina. Experto en atención al cliente y servicio de banquetes.",
    ]

    vector_db = FAISS.from_texts(perfiles, embeddings)

    query_vacante = "Buscamos un programador para crear servidores y lógica de negocio"

    resultados = vector_db.similarity_search_with_score(query_vacante, k=6)

    print("=" * 60)
    print("SISTEMA DE FILTRADO DE CANDIDATOS (HR-Tech)")
    print("=" * 60)
    print(f"\nVacante: \"{query_vacante}\"\n")
    print(f"{'Pos':<5} {'Score':<12} {'Perfil':<60}")
    print("-" * 77)

    for i, (doc, score) in enumerate(resultados, 1):
        perfil_corto = doc.page_content[:75] + "..."
        marcador = " <-- TRAMPA" if "Camarero" in doc.page_content else ""
        print(f"{i:<5} {score:<12.4f} {perfil_corto}{marcador}")

    print("\n" + "=" * 60)
    print("TOP 3 CANDIDATOS RECOMENDADOS")
    print("=" * 60)

    for i, (doc, score) in enumerate(resultados[:3], 1):
        print(f"\n--- Candidato #{i} (Distancia: {score:.4f}) ---")
        print(doc.page_content)

    print("\n" + "=" * 60)
    print("ANÁLISIS DEL CANDIDATO TRAMPA")
    print("=" * 60)

    for i, (doc, score) in enumerate(resultados, 1):
        if "Camarero" in doc.page_content:
            print(f"\nPosición en el ranking: {i} de {len(resultados)}")
            print(f"Distancia semántica: {score:.4f}")
            if i > 3:
                print("La IA ha detectado correctamente que 'servir mesas' NO es lo mismo "
                      "que 'crear servidores', a pesar de la coincidencia de palabras.")
            else:
                print("Sorpresa: la IA no ha filtrado bien al candidato trampa. "
                      "Esto puede pasar con modelos ligeros.")
            break


if __name__ == "__main__":
    filtro_candidatos()
