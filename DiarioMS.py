import requests
import datetime

class DiarioMS:
    def __init__(self, texto_busca):
        self.url = 'https://www.spdo.ms.gov.br/DiarioDOE/Index/Index/1'
        self.texto_busca = texto_busca
        # usando o datetime para pegar data inicial como sendo 60 dias atrás
        self.data_inicial = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime('%d/%m/%Y')

        self.post_data = {
            "Filter.Numero": "",
            "Filter.DataInicial": self.data_inicial,
            "Filter.DataFinal": "",
            "Filter.Texto": self.texto_busca,
            "Filter.TipoBuscaEnum": "1",
        }

    def location_text(self):
        return f"Iremos buscar no Diário Oficial do Estado de Mato Grosso do Sul os diários publicados a partir de {self.data_inicial} que contenham o texto '{self.texto_busca}'"

    def get_diarios(self):
        try:
            response = requests.post(self.url, data=self.post_data)
            response.raise_for_status()

            data = response.json()
            if not data["dataElastic"]:
                return "Nenhum resultado encontrado"

            message_return = ""

            for item in data["dataElastic"]:
                link_diario = f"https://www.spdo.ms.gov.br/diariodoe/Index/Download/{item['Source']['NomeArquivo'].replace('.pdf', '')}"
                message_return += f"Diário n. {item['Source']['Numero']} - {item['Source']['Descricao']}"
                message_return += f"\nLink Download: {link_diario}"
                message_return += f"\n"

            return message_return

        except Exception as e:
            return f"Erro ao buscar diários: {e}"