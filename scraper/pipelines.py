import json
import os


class JsonLinesPipeline:
    """
    Persistência simples em JSON Lines.
    """

    def open_spider(self, spider):
        # não commitar este arquivo no repositório
        out = os.environ.get("OUTPUT_FILE", "results.jl")
        self.file = open(out, "a", encoding="utf-8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # Converte datetimes para isoformat se houver
        obj = dict(item)
        for k in ["data_autuacao"]:
            v = obj.get(k)
            if hasattr(v, "isoformat"):
                obj[k] = v.isoformat()
        # movimentacoes já armazenam isoformat no spider
        line = json.dumps(obj, ensure_ascii=False)
        self.file.write(line + "\n")
        return item
