import os
import json
from typing import List, Any


class TemplateFile:
    def __init__(self, name: str, content: str = "", vars: List[Any] = None, id: int = 0):
        self.name: str = name
        self.content: str = content
        self.vars: List[Any] = vars if vars is not None else []
        self.id: int = id

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "vars": self.vars,
            "id": self.id,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TemplateFile":
        return cls(
            name=data.get("name", ""),
            content=data.get("content", ""),
            vars=data.get("vars", []),
            id=data.get("id", 0),
        )


class FileTerm:
    def __init__(self, name: str, id: int):
        self.format = "json"
        self.name_file = f"{name}.{id}.{self.format}"
        self.name_dir = ".exterm"
        self.path_dir = os.path.expanduser(f"~/{self.name_dir}")
        self.pathFile = os.path.join(self.path_dir, self.name_file)

        self.content = TemplateFile(name=name, id=id)

    def create(self) -> None:
        """Crea el archivo y directorio si no existen."""
        os.makedirs(self.path_dir, exist_ok=True)
        if not os.path.exists(self.pathFile):
            with open(self.pathFile, "w") as file:
                json.dump(self.content.to_dict(), file, indent=2)

    def read(self) -> str:
        """Lee el contenido del archivo."""
        if os.path.exists(self.pathFile):
            try:
                with open(self.pathFile, "r", encoding="utf-8") as file:
                    data = json.load(file)  # Intentamos cargar el JSON
                    self.content = TemplateFile.from_dict(data)  # Convertir a objeto
                    return self.content.content
            except json.JSONDecodeError as e:
                print(f"Error al cargar el archivo JSON: {e}")
                print(f"Contenido del archivo: {open(self.pathFile, 'r').read()}")
                return ""
        return ""


    def write(self, data: str) -> None:
        """Agrega datos al contenido del archivo."""
        self.content.content += f"{data}\n"
        self._save()

    def delete(self) -> None:
        """Elimina el archivo si existe."""
        if os.path.exists(self.pathFile):
            os.remove(self.pathFile)

    def clear(self) -> None:
        """Limpia el contenido del archivo."""
        self.content.content = ""
        self._save()

    def addVars(self, var: Any) -> None:
        """Agrega una variable al archivo."""
        self.content.vars.append(var)
        self._save()

    def _save(self) -> None:
        """Guarda el estado actual de `self.content` en el archivo."""
        os.makedirs(self.path_dir, exist_ok=True)
        with open(self.pathFile, "w") as file:
            json.dump(self.content.to_dict(), file, indent=2)
