import json
from dataclasses import dataclass

ESTAT_PENDENT = "pendent"


@dataclass
class Task:
    id: int
    títol: str
    assignatura: str
    estat: str = ESTAT_PENDENT

    @property
    def title(self):
        return self.títol

    @property
    def subject(self):
        return self.assignatura

    @property
    def status(self):
        return self.estat

    def to_dict(self):
        return {
            "id": self.id,
            "títol": self.títol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    @classmethod
    def from_dict(cls, dades):
        return cls(
            id=dades["id"],
            títol=dades.get("títol", dades.get("title")),
            assignatura=dades.get("assignatura", dades.get("subject")),
            estat=dades.get("estat", dades.get("status", ESTAT_PENDENT)),
        )

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, cadena):
        return cls.from_dict(json.loads(cadena))
