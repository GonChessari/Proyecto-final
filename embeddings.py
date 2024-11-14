import os
import re
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

#CARGO LAS VARIABLES DE ENTORNO CON UN MENSAJE POR SI TIRA ERROR
if not load_dotenv():
    raise EnvironmentError("No se pudieron cargar las variables de entorno.")

#DEFINO LOS PDF QUE VOY A UTILIZAR Y EL DIRECTORIO
pdf_file_paths = ["./docs/carreras UBA.pdf", "./docs/sedes_UBA_CBC.pdf"]
persist_directory = "docs/Chroma"

#ESTO PARA VER SI ESTAN BIEN CARGADOS LOS PDF
for pdf_file_path in pdf_file_paths:
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"El archivo {pdf_file_path} no existe.")

#CONFIGURO LOS EMBEDDINGS
embeddings_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

#CARGO Y PROCESO LOS PDF
documents = []
for pdf_file_path in pdf_file_paths:
    loader = PyPDFLoader(pdf_file_path)
    text = "\n".join([page.page_content for page in loader.load()])

    #USO ESTA EXPRESION PARA CHUKEAR EL TEXTO ME BASO EN EL SIMBOLO "●" PARA QUE IDENTIFIQUE TITULOS
    pattern = r"(● [^\n]+)"  #CAPTURO LAS LINEAS QUE EMPIEZAN CON "● " COMO TITULOS
    chunks = re.split(pattern, text)

    # ESTRUCTURACION DE FRAGMENTOS (TITULO Y CONTENIDOS)
    for i in range(1, len(chunks), 2):
        title = chunks[i].strip()  #"EL TITULO ES EL TEXTO DESPUES DE ""●"""
        content = chunks[i + 1].strip() if (i + 1) < len(chunks) else ""  #EL CONTENIDO QUE SIGUE EL TITULO
        documents.append({"text": f"{title}\n{content}"})  #COMBINA EL TITULO Y EL CONTENIDO

#CREA EL DIRECTORIO DE PERSISTENCIA SI NO EXISTE
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

#CREO LA BASE DE DATOS CON LOS FRAGMENTOS ESTRUCTURADOS
db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings_function,
    persist_directory=persist_directory
)
