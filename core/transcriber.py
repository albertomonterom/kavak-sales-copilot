import os
from dotenv import load_dotenv
from typing import List, Dict
from openai import OpenAI

load_dotenv()  # Carga las variables de entorno desde el archivo .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_wav_verbose(path_wav: str) -> List[Dict]:
    """
        Devuelve una lista de segmentos [{'start': float, 'end': float, 'text': str}]
        usando Whisper (OpenAI API) con formato verbose_json.
    """
    
    # Obtener la ruta absoluta del archivo
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Sube un nivel para llegar a la raíz del proyecto
    full_path = os.path.join(base_dir, path_wav)
    
    # Validar existencia del archivo
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo: {full_path}")

    with open(full_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            temperature=0
        )

    # Construir la lista de segmentos
    segments = []
    for seg in response.segments:
        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })
    return segments

# transcribe_wav_verbose("data/audio/demo.wav")
segments = transcribe_wav_verbose("data/audio/demo.wav")  # --- IGNORE ---
print("Transcripción detallada:")  # --- IGNORE ---
for segment in segments:  # --- IGNORE ---
    print(segment)  # --- IGNORE ---