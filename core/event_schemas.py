from typing import Optional
from pydantic import BaseModel, Field

class Event(BaseModel):
    """
    Representa un evento semántico detectado por el Listener.
    """
    type: str = Field(..., description="Tipo de evento: interest_detected, objection_detected, etc.")
    speaker: str = Field(..., description="Quién habla: Cliente | Agente | Desconocido")
    text: str = Field(..., description="Texto exacto o resumido del fragmento.")
    timestamp: float = Field(..., description="Tiempo aproximado en segundos donde ocurre el evento.")
    confidence: Optional[float] = Field(None, description="Nivel estimado de confianza (0-1).")


# Ejemplo: crear un evento de prueba
# evento = Event(
#     speaker="Cliente",
#     start=12.5,
#     end=15.0,
#     text="Hola, estoy interesado en el Mazda 3 2020.",
#     turn_id=1,
# )
# print(evento.model_dump())