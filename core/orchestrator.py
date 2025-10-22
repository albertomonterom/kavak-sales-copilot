# core/orchestrator.py
from agents.listener_agent import ListenerAgent
from agents.coach_agent import CoachAgent
from agents.actioner_agent import ActionerAgent
from agents.closer_agent import CloserAgent
from agents.critic_agent import CriticAgent

class Orchestrator:
    def __init__(self):
        self.listener = ListenerAgent()
        self.coach = CoachAgent()
        self.actioner = ActionerAgent()
        self.closer = CloserAgent()
        self.critic = CriticAgent()

    def handle_audio_stream(self, audio_chunk):
        text = self.listener.transcribe(audio_chunk)
        suggestion = self.coach.analyze(text)
        result = self.actioner.execute(suggestion)
        return result
