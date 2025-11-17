# TRF5 Web Scraper

Este projeto é um scraper em **Python + Scrapy** para buscar informações de processos no sistema do **TRF5** (Tribunal Regional Federal da 5ª Região).

O scraper realiza requisições ao endpoint oficial do TRF5 e extrai:

* Número do processo
* Número legado
* Data de autuação
* Relator
* Envolvidos (exceto relator)
* Movimentações processuais

---

## 🧩 Estrutura do Projeto

```
trf5_scraper/
│
├── trf5_scraper/
│   ├── spiders/
│   │   └── trf5_spider.py
│   ├── items.py
│   ├── utils.py
│   ├── pipelines.py
│   ├── middlewares.py
│   └── settings.py
│
├── results.jl
├── requirements.txt
└── README.md
```

---

## 🚀 Como executar o scraper

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute o Scrapy passando o número do processo:

```bash
scrapy crawl trf5 -a numero_processo=0015648-78.1999.4.05.0000
```

O resultado será salvo no arquivo **results.jl** (JSON Lines).

Se quiser sobrescrever:

```bash
scrapy crawl trf5 -a numero_processo=0015648-78.1999.4.05.0000 -O saida.json
```

---

## 🧰 Utilização do arquivo utils.py

Funções utilitárias usadas em todo o scraper:

* `extract_regex()` — extrai dados via regex
* `clean_text()` — normaliza e limpa textos
* `xpath_text()` — extrai texto de um único XPath
* `xpath_texts_join()` — extrai múltiplos textos e concatena

Isso melhora a legibilidade (**Clean Code**) e evita duplicações (**DRY**).

---

## 📝 Estrutura do item retornado

O spider retorna um objeto JSON no seguinte formato:

```json
{
  "numero_processo": "0015648-78.1999.4.05.0000",
  "numero_legado": "99.05.15648-8",
  "data_autuacao": "15/04/1999",
  "relator": "DESEMBARGADOR FEDERAL ...",
  "envolvidos": [
    {"papel": "APTE", "nome": "FULANO"},
    {"papel": "APDO", "nome": "BELTRANO"}
  ],
  "movimentacoes": [
    {"data": "01/01/2000", "texto": "Movimentação X"}
  ]
}
```

---

## 🧪 Testes

Você pode criar testes com **pytest** usando mocks para HTML ou responses locais.
Se quiser, posso gerar uma suíte de testes completa.

---

## 🔧 Princípios aplicados

* **SOLID**: Funções com responsabilidade única (Single Responsibility).
* **DRY**: Utilização do `utils.py` para funções repetitivas.
* **KISS**: XPath simples e claros.
* **Clean Code**: Nomes descritivos, docstrings e modularização.

---

## 📌 Melhorias futuras

* Suporte a múltiplos processos em lote
* Retry com backoff exponencial
* Exportação para banco de dados
* Criação de API Flask para consultar processos

---

## 📄 Licença

Este projeto é livre para uso pessoal e estudos.

---

Se quiser, posso adicionar um **badge**, melhorar a documentação ou criar um **Makefile** para facilitar a execução.
