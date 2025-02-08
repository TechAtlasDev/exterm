from exterm.core.term import Terminal
import time
from exterm.core.visual.ui import UI
import requests

terminal = Terminal("debug")

def main():
  ip = "1.1.1.1"
  URL = "http://ip-api.com/json/{}".format(ip)
  terminal.add_var(ip)

  terminal.log(f"Sistema hará consulta a: {URL}")

  try:
    response = requests.get(URL)
    data = response.json()
#    terminal.json(data)
  except Exception as error:
    terminal.error(error)

  time.sleep(10)
  terminal.clear()

# Crear y ejecutar la aplicación
def testing():
  viewer = UI(terminal)
  viewer.show()