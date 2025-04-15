from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionBuscarLivroTitulo(Action):
    def name(self) -> Text:
        return "action_buscar_livro_titulo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        titulo = next(tracker.get_latest_entity_values("titulo_livro"), None)
        if not titulo:
            dispatcher.utter_message(text="Desculpe, não entendi o título do livro.")
            return []

        url = f"http://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url).json()

        if response["docs"]:
            livro = response["docs"][0]
            resultado = f"Encontrei: {livro.get('title', 'Título não encontrado')} - Autor: {livro.get('author_name', ['Desconhecido'])[0]}"
        else:
            resultado = "Não encontrei nenhum livro com esse título."

        dispatcher.utter_message(text=resultado)
        return []

class ActionBuscarLivroAutor(Action):
    def name(self) -> Text:
        return "action_buscar_livro_autor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        autor = next(tracker.get_latest_entity_values("nome_autor"), None)
        if not autor:
            dispatcher.utter_message(text="Desculpe, não entendi o nome do autor.")
            return []

        url = f"http://openlibrary.org/search.json?author={autor}"
        response = requests.get(url).json()

        if response["docs"]:
            livros = [doc["title"] for doc in response["docs"][:3]]
            resultado = f"Alguns livros de {autor}: {', '.join(livros)}"
        else:
            resultado = "Não encontrei livros desse autor."

        dispatcher.utter_message(text=resultado)
        return []

class ActionBuscarLivroAssunto(Action):
    def name(self) -> Text:
        return "action_buscar_livro_assunto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        assunto = next(tracker.get_latest_entity_values("assunto_livro"), None)
        if not assunto:
            dispatcher.utter_message(text="Desculpe, não entendi o assunto.")
            return []

        url = f"http://openlibrary.org/search.json?subject={assunto}"
        response = requests.get(url).json()

        if response["docs"]:
            livros = [doc["title"] for doc in response["docs"][:3]]
            resultado = f"Alguns livros sobre {assunto}: {', '.join(livros)}"
        else:
            resultado = "Não encontrei livros sobre esse assunto."

        dispatcher.utter_message(text=resultado)
        return []
