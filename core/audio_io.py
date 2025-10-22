from pydub import AudioSegment
import os

def ensure_wav_16k_mono(src_path: str, dst_path: str) -> str:
    """
        Carga cualquier archivo de audio y lo guarda como WAV mono 16k PCM s16le.
        Si dst_path existe, lo sobrescribe.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__)) # Sube un nivel para llegar a la raíz del proyecto
    src_full = os.path.join(base_dir, src_path)
    dst_full = os.path.join(base_dir, dst_path)

    if not os.path.exists(src_full):
        raise FileNotFoundError(f"Archivo no encontrado: {src_full}")

    audio = AudioSegment.from_file(src_full)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(dst_full, format="wav")
    return dst_full

# ensure_wav_16k_mono("data/audio/demo.mp4", "data/audio/demo.wav")