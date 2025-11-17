import scrapy
from scrapy.http import FormRequest

from scraper.items import ProcessoItem

from ..utils import clean_text, extract_regex, xpath_text, xpath_texts_join


class TRF5Spider(scrapy.Spider):
    """
    Spider para coletar informações de processos no TRF5 utilizando Scrapy.
    Permite passar o número do processo via linha de comando:

        scrapy crawl trf5 -a numero_processo=0015648-78.1999.4.05.0000
    """

    name = "trf5"
    numero_processo = None

    FORM_URL = "https://cp.trf5.jus.br/cp/cp.do"

    FORMDATA_TEMPLATE = {
        "navigation": "Netscape",
        "filtroCpfRequest": "",
        "tipo": "xmlproc",
        "filtro": "",
        "filtroCPF2": "",
        "tipoproc": "T",
        "filtroRPV_Precatorios": "",
        "uf_rpv": "PE",
        "numOriginario": "",
        "numRequisitorio": "",
        "numProcessExec": "",
        "uf_rpv_OAB": "PE",
        "filtro_processo_OAB": "",
        "filtro_CPFCNPJ": "",
        "campo_data_de": "",
        "campo_data_ate": "",
        "vinculados": "true",
        "ordenacao": "D",
        "ordenacao cpf": "D",
    }

    def __init__(self, numero_processo=None, *args, **kwargs):
        """
        Inicializa a spider garantindo que o número do processo foi informado.

        :param numero_processo: Número do processo.
        """
        super().__init__(*args, **kwargs)

        if not numero_processo:
            raise ValueError(
                "Informe o número do processo.\n"
                "Exemplo:\n"
                "scrapy crawl trf5 -a numero_processo=0015648-78.1999.4.05.0000"
            )

        self.numero_processo = numero_processo

    def start_requests(self):
        """
        Envia a requisição inicial POST com o formulário do TRF5 preenchido.
        """
        formdata = self.FORMDATA_TEMPLATE.copy()
        formdata["filtro"] = self.numero_processo

        yield FormRequest(
            self.FORM_URL,
            formdata=formdata,
            callback=self.parse,
            method="POST",
        )

    def parse(self, response):
        """
        Valida a resposta e monta o objeto ProcessoItem com os dados extraídos.

        :param response: HTML contendo os dados do processo.
        """
        if "PROCESSO" not in response.text:
            self.logger.error("❌ TRF5 não retornou dados.")
            return

        item = ProcessoItem()

        item["numero_processo"] = self.extract_numero_processo(response)
        item["numero_legado"] = self.extract_numero_legado(response)
        item["data_autuacao"] = self.extract_data_autuacao(response)
        item["relator"] = self.extract_relator(response)
        item["envolvidos"] = self.extract_envolvidos(response)
        item["movimentacoes"] = self.extract_movimentacoes(response)

        yield item

    # ------------------------------
    #   Extrações dos dados
    # ------------------------------
    def extract_numero_processo(self, response):
        """
        Extrai o número do processo.

        :param response: HTML contendo os dados do processo.
        :return: Número do processo.
        """
        text = xpath_texts_join(
            response,
            "//p[contains(translate(., 'processo', 'PROCESSO'), 'PROCESSO')]/text()",
        )
        return extract_regex(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", text)

    def extract_numero_legado(self, response):
        """
        Extrai o número de processo legado.

        :param response: HTML contendo os dados do processo.
        :return: Número legado.
        """
        text = xpath_text(
            response, "//p[contains(., 'PROCESSO')]/following-sibling::p[1]/text()"
        )
        legado = extract_regex(r"\(?\d{2}\.\d{2}\.\d{4,}-\d\)?", text)
        return legado.strip("()")

    def extract_data_autuacao(self, response):
        """
        Extrai a data de autuação do processo.

        :param response: HTML contendo os dados do processo.
        :return: Data no formato dd/mm/yyyy.
        """
        text = xpath_text(
            response,
            "//div[contains(translate(text(),'autuado','AUTUADO'), 'AUTUADO')]",
        )
        return extract_regex(r"\d{2}/\d{2}/\d{4}", text)

    def extract_relator(self, response):
        """
        Extrai o nome do relator do processo.

        :param response: HTML contendo os dados do processo.
        :return: Nome do relator.
        """
        relator = xpath_text(
            response,
            "//td[contains(translate(text(),'relator','RELATOR'),'RELATOR')]/following-sibling::td[1]/b/text()",
        )
        return clean_text(relator)

    def extract_envolvidos(self, response):
        """
        Extrai todos os envolvidos do processo.

        :param response: HTML contendo os dados do processo.
        :return: Lista de dicionários com 'papel' e 'nome' dos envolvidos.
        """
        envolvidos = []

        # Seleciona a terceira tabela da página
        table = response.xpath("(//table)[3]")

        if not table:
            return envolvidos  # Tabela não encontrada

        # Pega todas as linhas da tabela
        rows = table.xpath(".//tr")

        for tr in rows:
            # Extrai o papel (primeira coluna)
            papel = tr.xpath("normalize-space(./td[1]//text())").get(default="")

            # Extrai o nome (segunda coluna)
            nome = tr.xpath("normalize-space(./td[2]//b/text())").get(default="")

            # Ignorar RELATOR
            if "RELATOR" in papel.upper():
                continue

            if papel and nome:
                papel = clean_text(papel)
                nome = clean_text(nome)

                envolvidos.append({"papel": papel, "nome": nome})

        return envolvidos

    def extract_movimentacoes(self, response):
        """
        Extrai a lista de movimentações processuais (data + descrição).

        :param response: HTML contendo os dados do processo.
        :return: Lista de movimentações.
        """
        movimentos = []
        tables = response.xpath("//table[contains(., 'Em ')]")

        for tbl in tables:
            data_mov = tbl.xpath("normalize-space(.//a/text())").get(default="")
            data_mov = data_mov.replace("Em ", "").strip()

            descricao = xpath_texts_join(tbl, ".//tr[2]/td[2]//text()")

            if data_mov and descricao:
                movimentos.append({"data": data_mov, "texto": descricao})

        return movimentos
