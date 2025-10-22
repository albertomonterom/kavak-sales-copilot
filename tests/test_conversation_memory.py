"""
    Cuando creamos un agente necesitamos que este tenga memoria de la conversación
    para que pueda responder de manera contextualizada. Estaremos usando la clase
    ConversationBufferMemory sobre RunnableWithMessageHistory, la razón de esto es que
    ConversationBufferMemory es compatible con la interfaz de LangChain y nos permite
    almacenar el historial de la conversación de manera sencilla.
"""

# Primero definiremos nuestro LLM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Definiremos nuestras tools
from langchain_core.tools import tool
@tool
def add(x: float, y: float) -> float:
    """Suma dos números."""
    return x + y

@tool
def subtract(x: float, y: float) -> float:
    """Resta dos números."""
    return x - y

@tool
def multiply(x: float, y: float) -> float:
    """Multiplica dos números."""
    return x * y

@tool
def exponentiate(x: float, y: float) -> float:
    """Eleva x a la potencia y."""
    return x ** y

# Ahora definiremos nuestro prompt
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Eres un asistente útil que ayuda con operaciones matemáticas."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Ahora definiremos nuestra memoria
from langchain.memory import ConversationBufferMemory

# Definimos la memoria de la conversación
memory = ConversationBufferMemory(
    memory_key="chat_history", # clave para acceder al historial
    return_messages=True # retornar mensajes en lugar de texto plano
)

"""
    Ahora inicializaremos nuestro agente. Para esto usaremos:
    - llm: el modelo de lenguaje que usaremos
    - memory: la memoria que acabamos de crear
    - prompt: el prompt que usaremos para guiar al agente
    - memory: la memoria que usaremos para almacenar el historial    
"""

from langchain.agents import create_tool_calling_agent, AgentExecutor

# Definimos las tools que usaremos
tools = [add, subtract, multiply, exponentiate]

# Creamos el agente
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Finalmente creamos el ejecutor del agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
)

"""
    Finalmente probaremos nuestro agente con una conversación de ejemplo
    que involucra múltiples pasos y el uso de memoria.
"""
response = agent.invoke({
    "input": "¿Cuánto es 10.7 multiplicado por 7.68?",
    "chat_history": memory.chat_memory.messages,
    "intermediate_steps": []
})

print("Respuesta del agente:", response)