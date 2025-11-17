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
├── scraper/
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


## 📝 Estrutura do item retornado

O spider retorna um objeto JSON no seguinte formato:

```json
{
  "numero_processo": "1234567-89.2024.4.05.9999",
  "numero_legado": "24.99.123456-7",
  "data_autuacao": "10/02/2024",
  "relator": "DESEMBARGADOR FEDERAL JOÃO SILVA",
  "envolvidos": [
    { "papel": "APTE", "nome": "CARLOS ALMEIDA" },
    { "papel": "APDO", "nome": "MARIA FERNANDA" },
    { "papel": "Advogado", "nome": "DR. RICARDO MENDES" }
  ],
  "movimentacoes": [
    { "data": "20/02/2024", "texto": "Distribuição automática realizada." },
    { "data": "25/02/2024", "texto": "Concluso para despacho." },
    { "data": "01/03/2024", "texto": "Despacho proferido pelo relator." }
  ]
}

```

 ⚠️ IMPORTANTE: Estes dados são totalmente fictícios e servem apenas como exemplo técnico.


---
