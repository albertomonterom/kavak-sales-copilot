import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Importar el prompt desde data/prompts.py
from data.prompts import LISTENER_PROMPT

# Carga variables del entorno
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", LISTENER_PROMPT)
])

def detect_events_from_segment(segment: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
        Envía un segmento transcrito al LLM (Listener) y devuelve una lista de eventos detectados.
    """
    text = segment.get("text", "").strip()
    if not text:
        return []

    # Construir entrada
    input_text = (
        f"Texto: \"{text}\"\n"
        f"Speaker: {segment.get('speaker', 'Desconocido')}\n"
        f"Timestamp: {segment.get('start', 0.0)}"
    )

    chain = prompt | llm | parser
    raw_response = chain.invoke({"input_text": input_text})
    print("\n--- RAW RESPONSE ---")
    print(raw_response)
    print("--------------------\n")


    try:
        events = json.loads(raw_response)
        if isinstance(events, dict):
            events = [events]
        return events
    except Exception as e:
        print(f"Error al parsear JSON para segmento: {text[:50]}... -> {e}")
        return []