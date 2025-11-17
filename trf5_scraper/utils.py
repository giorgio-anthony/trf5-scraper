import re


def extract_regex(pattern, text):
    """
    Executa uma expressão regular e retorna o match encontrado.

    :param pattern: Padrão regex a ser aplicado.
    :param text: Texto onde a busca será realizada.
    :return: String correspondente ao match ou string vazia.
    """
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def clean_text(value):
    """
    Remove caracteres desnecessários e espaços em excesso do texto.

    :param value: Texto de entrada.
    :return: Texto limpo sem ":" e espaços extras.
    """
    return value.replace(":", "").strip()


def xpath_text(response, xpath):
    """
    Extrai um único texto usando uma expressão XPath.

    :param response: Objeto Response HTML do Scrapy.
    :param xpath: Expressão XPath a ser usada.
    :return: Texto extraído ou string vazia caso não exista.
    """
    return response.xpath(xpath).get(default="").strip()


def xpath_texts_join(response, xpath):
    """
    Extrai múltiplos textos de um XPath e concatena tudo em uma única string.

    :param response: Objeto Response HTML do Scrapy.
    :param xpath: Expressão XPath para capturar vários textos.
    :return: String única com todos os textos concatenados e limpos.
    """
    texts = response.xpath(xpath).getall()
    return " ".join(t.strip() for t in texts if t.strip())
