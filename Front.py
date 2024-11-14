import streamlit as st
from main import *
from PIL import Image
import time

# Configuración de la página
st.set_page_config(page_title="Universidad de Buenos Aires - Úbatron", page_icon="uba-LOGO.png", layout="centered")

# Estilos CSS de alto impacto
st.markdown("""
    <style>
        /* Fondo animado en 3D */
        .stApp {
            background: radial-gradient(circle, #d8eefe, #bbdefb, #9fc7e4);
            background-size: 400% 400%;
            animation: gradientShift 10s ease infinite;
            font-family: 'Montserrat', sans-serif;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Encabezado con efecto neón y destellos animados */
        h1 {
            color: #00539C;
            font-weight: 900;
            font-size: 3.5em;
            text-shadow: 0px 0px 10px rgba(0, 83, 156, 0.5), 0px 0px 25px rgba(0, 83, 156, 0.6), 0px 0px 40px rgba(0, 83, 156, 0.3);
            animation: pulseGlow 2s infinite alternate, neonShine 0.8s infinite alternate;
        }

        h2 {
            color: #007bb5;
            font-weight: 600;
            font-size: 1.7em;
            text-shadow: 0px 0px 8px rgba(0, 123, 181, 0.5);
            animation: subtitleGlow 3s infinite alternate, pulseGlow 1.5s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { text-shadow: 0px 0px 12px rgba(0, 83, 156, 0.7); }
            100% { text-shadow: 0px 0px 18px rgba(0, 83, 156, 1); }
        }

        @keyframes neonShine {
            0% { text-shadow: 0px 0px 20px rgba(0, 83, 156, 1), 0px 0px 40px rgba(0, 83, 156, 0.6), 0px 0px 60px rgba(0, 83, 156, 0.3); }
            100% { text-shadow: 0px 0px 8px rgba(0, 83, 156, 0.5), 0px 0px 20px rgba(0, 83, 156, 0.4); }
        }

        @keyframes subtitleGlow {
            0% { text-shadow: 0px 0px 10px rgba(0, 123, 181, 0.3); }
            100% { text-shadow: 0px 0px 25px rgba(0, 123, 181, 0.6); }
        }

        /* Efecto de expansión en el contenedor */
        .title-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 20px;
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.85);
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(15px);
            transform: scale(1);
            transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.4s ease;
        }

        /* Efecto hover para el contenedor */
        .title-container:hover {
            transform: scale(1.05);
            box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.3);
            background-color: rgba(255, 255, 255, 0.95);
        }

        /* Botón con color sobrio y sin animación */
        .stButton > button {
            background-color: #4A90E2; /* Color azul sobrio */
            color: white;
            font-weight: bold;
            font-size: 1.1em;
            border: none;
            border-radius: 50px;
            padding: 12px 28px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #357ABD; /* Color más oscuro en hover */
        }

        /* Estilo de chat con animación lenta */
        .stChatMessage {
            font-size: 1.3em;
            line-height: 1.6;
            padding: 20px;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0px 5px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 25px;
            transform: translateY(80px);
            animation: floatIn 2.5s ease-out forwards, chatFadeIn 2s ease-out forwards, bounceIn 2s ease-in-out forwards, scaleUp 1.5s ease-out forwards;
            opacity: 0;
        }

        @keyframes floatIn {
            from { transform: translateY(80px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes chatFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes bounceIn {
            0% { transform: translateY(80px); }
            30% { transform: translateY(0); }
            50% { transform: translateY(-30px); }
            70% { transform: translateY(10px); }
            100% { transform: translateY(0); }
        }

        @keyframes scaleUp {
            0% { transform: scale(0.6); }
            100% { transform: scale(1); }
        }

        @keyframes userBubble {
            0% { transform: scale(0.8); opacity: 0.4; }
            100% { transform: scale(1); opacity: 1; }
        }

        @keyframes botBubble {
            0% { transform: scale(0.8); opacity: 0.4; }
            100% { transform: scale(1); opacity: 1; }
        }

        @keyframes userBubbleScale {
            0% { transform: scale(0.9); }
            100% { transform: scale(1); }
        }

        @keyframes botBubbleScale {
            0% { transform: scale(0.9); }
            100% { transform: scale(1); }
        }

        @keyframes userBubbleBounce {
            0% { transform: translateY(10px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }

        @keyframes botBubbleBounce {
            0% { transform: translateY(10px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }

    </style>
""", unsafe_allow_html=True)

# Cargar y mostrar el logo de la UBA
img = Image.open("uba-LOGO.png")

# Crear layout del encabezado con animación de hover
st.markdown("<div class='title-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 2])

with col1:
    st.title("Universidad de Buenos Aires")
    st.subheader("Descubrí tu futuro académico con **Úbatron** 🤖")

with col2:
    st.image(img, width=350)

st.markdown("</div>", unsafe_allow_html=True)

# Botón para borrar historial con feedback visual mejorado (botón estático y sobrio)
if st.button(" Borrar historial 🧹 "):
    st.session_state.messages = []
    chat_history = []
    memory.clear()
    st.success("Historial borrado con éxito.", icon="✅")

# Definir avatares
usuario = "🎓"
bot = "🤖"


# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes de chat anteriores
for message in st.session_state.messages:
    avatar = usuario if message["role"] == "user" else bot
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Campo de entrada para el usuario
if prompt := st.chat_input("¡Animate a escribirme!"):
    # Agregar mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensaje del usuario
    with st.chat_message("user", avatar=usuario):
        st.markdown(prompt)

    # Concatenar historial de mensajes del usuario
    chat_history = "\n\n".join(
        [f"**Usuario:** {message['content']}" for message in st.session_state.messages if message["role"] == "user"]
    )

    # Generar y mostrar respuesta del bot
    with st.chat_message("assistant", avatar=bot):
        contenedor_respuesta = st.empty()
        full_response = ""
        
        # Obtener respuesta del bot
        respuesta = chatbot(prompt, chat_history)

        # Mostrar respuesta progresivamente, simulando escritura
        for char in respuesta:  # Mostrar caracter por caracter
            full_response += char
            time.sleep(0.02)  # Ajusta la velocidad de "escritura"
            contenedor_respuesta.markdown(full_response)

    # Agregar respuesta completa al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": full_response})
