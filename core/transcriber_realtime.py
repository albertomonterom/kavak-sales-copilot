import os
import pyaudio
import webrtcvad
import numpy as np
from faster_whisper import WhisperModel
import json
from datetime import datetime, timezone
from core.listener_event_detector import detect_events_from_segment

SESSION_LOG_PATH = None

RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
FRAME_DURATION = 20  # menor duración → menor latencia
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
VAD_SENSITIVITY = 2  # sensibilidad media
SILENCE_LIMIT = 10  # número de frames (~0.6 s) de silencio para cortar

model = WhisperModel(
    "tiny",
    device="cuda" if os.getenv("USE_CUDA") == "1" else "cpu",
    compute_type="int8"
)

def frame_generator(stream):
    while True:
        data = stream.read(FRAME_SIZE, exception_on_overflow=False)
        if len(data) < FRAME_SIZE * 2:
            continue
        yield data

def transcribe_frames(frames):
    audio = np.frombuffer(b"".join(frames), np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(audio, beam_size=3, language="es")
    return " ".join(seg.text.strip() for seg in segments).strip()

def get_session_log_path(out_dir="data/logs"):
    """Devuelve la ruta del archivo único de esta sesión."""
    global SESSION_LOG_PATH
    if SESSION_LOG_PATH is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        logs_full = os.path.join(base_dir, out_dir)
        os.makedirs(logs_full, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        SESSION_LOG_PATH = os.path.join(logs_full, f"live_listener_{timestamp}.jsonl")
    return SESSION_LOG_PATH


def save_event(event):
    """Guarda eventos en el mismo archivo durante toda la sesión."""
    out_path = get_session_log_path()
    with open(out_path, "a", encoding="utf-8") as f:
        if isinstance(event, list):
            for ev in event:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        else:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

def stream_with_vad():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=1024)
    vad = webrtcvad.Vad(VAD_SENSITIVITY)

    print("Escuchando (Ctrl+C para detener)...")
    voiced_frames, silence_frames, speaking = [], 0, False

    try:
        for frame in frame_generator(stream):
            is_speech = vad.is_speech(frame, RATE)
            print("voz" if is_speech else "silencio", end="\r")

            if is_speech:
                voiced_frames.append(frame)
                silence_frames = 0
                speaking = True
            elif speaking:
                silence_frames += 1
                if silence_frames > SILENCE_LIMIT:
                    speaking = False
                    if voiced_frames:
                        extra_padding = int(0.2 * RATE / (FRAME_SIZE / 2))
                        voiced_frames.extend([b"\x00" * FRAME_SIZE] * extra_padding)

                        print("\nTranscribiendo...")
                        text = transcribe_frames(voiced_frames)
                        voiced_frames = []
                        silence_frames = 0
                        print(f"Texto detectado: {text}")

                        if text:
                            event = detect_events_from_segment({
                                "text": text
                            })
                            print(f"Evento detectado: {event}")
                            if event:
                                save_event(event)
            else:
                pass

    except KeyboardInterrupt:
        print("\nGrabación detenida.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    stream_with_vad()