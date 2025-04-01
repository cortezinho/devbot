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
1. Clique em 'Esqueci minha senha'
2. Verifique seu e-mail
3. Crie uma nova senha
Mais informações: [Ajuda com acesso](https://somnanuvem.ajuda/acesso)"""
        
        elif intent == "problema_plano":
            resposta = """Para alterar seu plano:
1. Acesse 'Minha Conta'
2. Selecione 'Planos'
3. Escolha seu novo plano

Planos disponíveis:
- Básico: R$19,90/mês
- Premium: R$29,90/mês
- Família: R$39,90/mês (até 6 pessoas)

Mais informações: [Planos disponíveis](https://somnanuvem.ajuda/planos)"""
        
        elif intent == "problema_tecnico":
            resposta = """Para problemas técnicos:
1. Reinicie o aplicativo
2. Verifique sua conexão com a internet
3. Atualize para a versão mais recente

Se o problema persistir, posso encaminhar para um atendente humano."""
        
        elif intent == "problema_pagamento":
            resposta = """Para problemas com pagamento:
1. Verifique os dados do seu cartão
2. Confira o limite disponível
3. Tente outro método de pagamento

Para ajustes de cobrança, precisaremos transferir para um atendente humano."""
        
        else:
            resposta = "Não entendi completamente seu problema. Poderia reformular?"

        dispatcher.utter_message(text=resposta)
        
        return []