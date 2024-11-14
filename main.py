import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory, ConversationBufferWindowMemory
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
import time

# Cargar variables de entorno
load_dotenv()

# Función de embeddings
embeddings_function = OpenAIEmbeddings()

# Instanciar el modelo de lenguaje
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,  # Respuestas más precisas
        model_kwargs={"top_p": 0.5},  # Mejora la coherencia
)

# Cargar la base de datos (Chroma) con la información de ambos documentos
db_carreras = Chroma(
    persist_directory='docs/Chroma',  # Directorio donde están los documentos de carreras
    embedding_function=embeddings_function
)

db_sedes = Chroma(
    persist_directory='docs/Chroma',  # Directorio donde están los documentos de sedes
    embedding_function=embeddings_function
)

# Crear un retriever para cada base de datos
retriever_carreras = db_carreras.as_retriever()
retriever_sedes = db_sedes.as_retriever()

# Crear memoria para el agente
memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True,
    chat_memory=ChatMessageHistory()
)

# Crear la herramienta de búsqueda de carreras
Busqueda_carreras_UBA = create_retriever_tool(
    retriever=retriever_carreras,
    name='Busqueda_carreras_UBA',
    description="Find UBA degree programs that align with the user's interests"
)

# Crear la herramienta de búsqueda de sedes
Busqueda_sedes_UBA = create_retriever_tool(
    retriever=retriever_sedes,
    name='Busqueda_sedes_UBA',
    description="Find UBA campus information for user queries"
)

# Agrupar todas las tools, incluyendo la nueva herramienta de las sedes
tools = [Busqueda_carreras_UBA, Busqueda_sedes_UBA]


# Definir el prompt
prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages[0].prompt.template = (
    "Tu nombre es Úbatron. Sos un bot creado para ayudar a los usuarios a elegir carreras de la Universidad de Buenos Aires (UBA) y, si es necesario, brindarles información sobre las sedes de dicha universidad."
    "Siempre vas a hablar en español de Argentina, utilizando exclusivamente el voseo. Usá 'VOS' en vez de 'TÚ', y 'ACÁ' en vez de 'AQUÍ'. Siempre priorizá un lenguaje informal, cercano y amigable, como si estuvieras hablando con un amigo."
    "La primera frase que digas siempre debe ser: '¡Hola! Soy Úbatron y te voy a ayudar a elegir tu próxima carrera. ¿Podrías contarme un poco sobre vos para poder ayudarte?' Si el usuario no menciona su nombre, decile: '¡No te olvides de decirme tu nombre!' y hacé un salto de línea."
    "Simulá ser un humano. Nadie debe notar que sos un bot, por lo tanto, las respuestas deben sentirse naturales y auténticas."
    "Si no podés encontrar una respuesta exacta sobre las carreras de la UBA, vas a ofrecer recomendaciones breves basadas en el área de interés mencionada por el usuario. Asegurate de ser claro, directo y brindar soluciones útiles, pero siempre de manera breve."
    "Cuando des tus recomendaciones, siempre añadí al final: 'Podés ingresar a https://www.cbc.uba.ar/carreras para obtener más información detallada."
    "Si el usuario lo solicita, podés ofrecerle un listado general de las sedes principales de la UBA para que pueda realizar consultas de manera presencial. Usá el comando Busqueda_sedes_UBA para esto."
    "Tus respuestas deben ser claras y bien estructuradas: empezá con un título destacado, seguido de un subtítulo si es necesario, y después el cuerpo del mensaje. La información debe ser fácil de leer y siempre amigable."
    "El nombre de tu creador es: Gonzalo Chessari. Si te preguntan por él responderás inventando cosas muy agradables sobre él y luego redireccionarás la conversacion para lo que fuiste creado de una menera muy natural."
)


# Crear el agente con las herramientas actualizadas
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Ejecutar el agente con la nueva herramienta
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Función para interactuar con el chatbot
def chatbot(query: str, chat_history):
    response = agent_executor.invoke({'input': query, "chat_history": chat_history })['output']
    return response
