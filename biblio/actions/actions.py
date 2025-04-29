import requests
# Importa a biblioteca 'requests' para fazer requisições HTTP
from typing import Any, Text, Dict, List
# Importa tipos usados para anotações de tipo
from rasa_sdk import Action, Tracker
# Importa a classe base Action e o rastreador de diálogo Tracker do Rasa SDK
from rasa_sdk.executor import CollectingDispatcher
# Importa o despachante que envia mensagens de volta ao usuário

# Classe que define a ação personalizada para buscar livro por título
class ActionBuscarPorTitulo(Action):
    
    def name(self) -> Text:
        return "action_buscar_por_titulo"  # Nome da ação personalizada, usado no domain.yml

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        # Obtém o valor mais recente da entidade "titulo" fornecida pelo usuário
        titulo = next(tracker.get_latest_entity_values("titulo"), None)
        
        if not titulo:
            # Se o título não foi identificado, solicita ao usuário que informe
            dispatcher.utter_message(text="Qual é o título do livro que você procura?")
            return []

        # Monta a URL da API do OpenLibrary para buscar livros por título
        url = f"https://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url)  # Faz a requisição GET para a API
        data = response.json()  # Converte a resposta para formato JSON

        if data["numFound"] > 0:
            # Se encontrou livros, pega os 3 primeiros resultados
            livros = data["docs"][:3]
            # Cria uma lista de mensagens com título e autores dos livros
            mensagens = [f"- {livro.get('title')} por {', '.join(livro.get('author_name', []))}" for livro in livros]
            # Envia os resultados ao usuário
            dispatcher.utter_message(text="Aqui estão alguns resultados:\n" + "\n".join(mensagens))
        else:
            # Se nenhum livro foi encontrado, envia uma mensagem de erro (definida nas respostas)
            dispatcher.utter_message(response="utter_erro_busca")
        
        return []  # Retorna uma lista vazia (nenhum evento de diálogo a ser aplicado)

# Classe que define a ação personalizada para buscar livros por autor
class ActionBuscarPorAutor(Action):
    
    def name(self) -> Text:
        return "action_buscar_por_autor"  # Nome da ação personalizada

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        # Obtém o valor mais recente da entidade "autor" fornecida pelo usuário
        autor = next(tracker.get_latest_entity_values("autor"), None)
        
        if not autor:
            # Se o autor não foi informado, solicita ao usuário
            dispatcher.utter_message(text="Qual autor você quer buscar?")
            return []

        # Monta a URL da API do OpenLibrary para buscar livros por autor
        url = f"https://openlibrary.org/search.json?author={autor}"
        response = requests.get(url)  # Faz a requisição HTTP
        data = response.json()  # Converte a resposta para JSON

        if data["numFound"] > 0:
            # Se encontrou livros, pega os 3 primeiros resultados
            livros = data["docs"][:3]
            # Cria mensagens com título e ano da primeira publicação
            mensagens = [f"- {livro.get('title')} ({livro.get('first_publish_year', 'Ano desconhecido')})" for livro in livros]
            # Envia os resultados ao usuário
            dispatcher.utter_message(text="Aqui estão alguns livros do autor:\n" + "\n".join(mensagens))
        else:
            # Se nenhum livro foi encontrado, envia uma mensagem de erro
            dispatcher.utter_message(response="utter_erro_busca")
        
        return []  # Retorna lista vazia (nenhuma modificação no diálogo)
    
# Classe que define a ação personalizada para buscar livros por assunto
class ActionBuscarPorAssunto(Action):

    def name(self) -> Text:
        return "action_buscar_por_assunto"  # Nome da ação para o domain.yml

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        # Obtém o valor mais recente da entidade "assunto" fornecida pelo usuário
        assunto = next(tracker.get_latest_entity_values("assunto"), None)
        
        if not assunto:
            dispatcher.utter_message(text="Qual assunto você deseja buscar?")
            return []

        # Formata o assunto para a URL (substitui espaços por '+')
        assunto_formatado = assunto.replace(" ", "+")
        url = f"https://openlibrary.org/search.json?subject={assunto_formatado}"

        response = requests.get(url)
        data = response.json()

        if data["numFound"] > 0:
            livros = data["docs"][:3]
            mensagens = [f"- {livro.get('title')} por {', '.join(livro.get('author_name', ['Autor desconhecido']))}" for livro in livros]
            dispatcher.utter_message(text="Aqui estão alguns livros relacionados ao assunto:\n" + "\n".join(mensagens))
        else:
            dispatcher.utter_message(response="utter_erro_busca")

        return []

