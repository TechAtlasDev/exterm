from random import randint
from .files import FileTerm

class Terminal:
  def __init__(self, name:str, id:int=0):
    self.id = id if self.__generateRandomID() != 0 else 0
    self.name = name

    self.file = FileTerm(name=self.name, id=self.id)
    self.file.create()

  def print(self, data):
    self.file.write(data)

  def error(self, error:Exception):
    # Obteniendo todos los datos del error
    error_type = type(error).__name__
    error_message = str(error)
    error_traceback = error.__traceback__
    error_line = error_traceback.tb_lineno
    error_file = error_traceback.tb_frame.f_code.co_filename

    self.file.write(f"[ ERROR ] {error_type}: {error_message} in {error_file} at line {error_line}")

  def log(self, data):
    self.file.write(f"[ LOG ] {data}")

  def warning(self, data):
    self.file.write(f"[ WARNING ] {data}")
  
  def success(self, data):
    self.file.write(f"[ SUCCESS ] {data}")
  
#  def json(self, data:dict):
#    self.file.write(json.dumps(data, indent=2))

  def clear(self):
    self.file.clear()

  def add_var(self, var):
    self.file.addVars(var)

  def __generateRandomID(self) -> int:
    return randint(0, 1000000)