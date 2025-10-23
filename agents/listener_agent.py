import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from typing import List
from core.transcriber import transcribe_wav_verbose
from core.listener_event_detector import detect_events_from_segment

load_dotenv()

def run_listener_on_file(audio_path: str, out_dir: str = "data/logs") -> str:
    """
        Ejecuta el listener sobre un archivo de audio WAV
        y guarda los eventos en formato JSONL.

        Parámetros:
            - audio_path: Ruta al archivo de audio WAV.
            - out_dir: Directorio donde se guardarán los resultados.

        Retorna:
            - Ruta completa del archivo JSONL con los eventos generados.
    """
    # Construcción de rutas absolutas
    base_dir = os.path.dirname(os.path.dirname(__file__))
    audio_full = os.path.join(base_dir, audio_path)
    logs_full = os.path.join(base_dir, out_dir)
    os.makedirs(logs_full, exist_ok=True)

    if not os.path.exists(audio_full):
        raise FileNotFoundError(f"No se encontró el archivo de audio: {audio_full}")

    # Transcribir
    print("Transcribiendo audio...")
    segments = transcribe_wav_verbose(audio_path)

    # Generar eventos
    print("Detectando eventos...")
    all_events = []
    for seg in segments:
        events = detect_events_from_segment(seg)
        if events:
            all_events.extend(events)
    
    # Guardar resultados
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(logs_full, f"listener_events_{timestamp}.jsonl")

    with open(out_path, "w", encoding="utf-8") as f:
        for ev in all_events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    print(f"Eventos guardados en: {out_path}")
    return out_path


if __name__ == "__main__":
    run_listener_on_file("data/audio/demo.wav")