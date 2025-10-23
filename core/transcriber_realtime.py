import numpy as np
from faster_whisper import WhisperModel
from pydub import AudioSegment

# Inicializa el modelo
# Usa el modelo base 'small' para buena velocidad y calidad
model = WhisperModel("small", device="cpu", compute_type="int8")

def stream_transcribe_wav(path_wav: str, chunk_ms: int = 5000):
    """
    Simula transcripción en tiempo real dividiendo el audio en fragmentos.
    Devuelve un generador que produce segmentos (texto, start, end) a medida que los obtiene.
    """
    audio = AudioSegment.from_wav(path_wav)
    duration_ms = len(audio)
    start_ms = 0

    while start_ms < duration_ms:
        end_ms = min(start_ms + chunk_ms, duration_ms)
        chunk = audio[start_ms:end_ms]

        # Convertimos a numpy float32 mono
        samples = np.array(chunk.get_array_of_samples()).astype(np.float32) / 32768.0

        # Transcripción del fragmento
        segments, _ = model.transcribe(samples, language="es", beam_size=1)

        for seg in segments:
            yield {
                "start": seg.start + start_ms / 1000.0,
                "end": seg.end + start_ms / 1000.0,
                "text": seg.text.strip()
            }

        start_ms = end_ms