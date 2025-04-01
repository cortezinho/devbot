from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionFornecerSuporte(Action):
    def name(self) -> Text:
        return "action_fornecer_suporte"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "problema_acesso":
            resposta = """Para problemas de acesso:
Verifique seu email, senha e telefone..."""
        
        elif intent == "problema_plano":
            resposta = """Para alterar seu plano:
Para alterar seu plano vá em configurações e em seus planos e mude pra outro.
"""
        
        elif intent == "problema_tecnico":
            resposta = """Para problemas técnicos:
Busque verificar seu aplicativo, caso não funcione entre em contato"""
        
        elif intent == "problema_pagamento":
            resposta = """Para problemas com pagamento:
Verifique seus dados, numero do cartao e cvv."""
        
        else:
            resposta = "Não entendi completamente seu problema. Poderia reformular?"

        dispatcher.utter_message(text=resposta)
        
        return []