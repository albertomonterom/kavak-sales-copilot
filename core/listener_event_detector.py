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

def detect_events_from_segment(segment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Envía un fragmento transcrito al modelo y devuelve solo un dict con 'type' y 'text'.
    """
    text = segment.get("text", "").strip()
    if not text:
        return {"type": "other", "text": ""}

    input_text = f'Texto: "{text}"'
    chain = prompt | llm | parser

    try:
        raw = chain.invoke({"input_text": input_text}).strip()
        event = json.loads(raw)
        return event
    except Exception as e:
        print(f"[WARN] Error parseando para '{text[:40]}...': {e}")
        return {"type": "other", "text": text}