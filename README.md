# Kavak Sales Copilot

Sistema **Kavak Sales Copilot**, una arquitectura multi-agente que asiste a los agentes humanos de Kavak durante llamadas en tiempo real.  
El sistema escucha la conversación, detecta intención y sentimiento, ejecuta acciones automáticas (cotización, reserva, financiamiento) y se auto-mejora con cada llamada.

---

## Objetivo

Construir un **copiloto de ventas auto-mejorable** que:
- Transcriba llamadas en vivo (Speech-to-Text)
- Analice intención, emoción y objeciones del cliente
- Ejecute acciones automáticas (API Kavak simuladas)
- Cierre la llamada con la acción óptima
- Evalúe su desempeño y mejore sus prompts de manera autónoma

---

## Instalación y configuración

```bash
# Clonar el repositorio
git clone https://github.com/albertomonterom/kavak-sales-copilot.git
cd kavak-sales-copilot

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Instalar dependencias
pip install -r requirements.txt