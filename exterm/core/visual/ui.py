from prompt_toolkit.document import Document
import threading
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Frame, TextArea

from exterm.core.term import Terminal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class UI:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.name = terminal.name
        self.id = terminal.id

        layout = self.__create_layout()
        shortcuts = self.__create_shortcuts()

        self.app = Application(
            layout=layout,
            key_bindings=shortcuts,
            full_screen=True,
        )

        # Iniciar el hilo para observar el archivo de la terminal
        self._start_file_watcher()

    def __create_layout(self):
        header = Window(
            content=FormattedTextControl(f"[🟢] Terminal: on  |  [📝] NAME: {self.name}  |  [🪪] ID: {self.id}"),
            height=1,
            style="bg:#333 #ffffff bold",
        )
        footer = Window(
            content=FormattedTextControl("Press Ctrl+c to exit | Tab for change of window."),
            height=1,
            style="bg:#a100b4 #e7e7e7 bold",
        )

        content = self.__create_content()
        layout = Layout(container=HSplit([header, content, footer]))

        return layout

    def __create_content(self):
        left_area = TextArea(self.get_terminal_content(), multiline=True, read_only=True, wrap_lines=True, scrollbar=True)
        right_area = TextArea("Contenido del panel derecho", multiline=True, read_only=True, wrap_lines=True)

        left_panel = Frame(left_area, title="Lines")
        right_panel = Frame(right_area, title="Vars")

        content = VSplit([left_panel, right_panel])

        self.left_area = left_area  # Guardar referencia para actualizar más tarde

        return content

    def get_terminal_content(self):
        return self.terminal.file.read()
    
    def update_terminal_content(self):
        new_content = self.get_terminal_content()

        self.left_area.text = new_content

        doc = self.left_area.document
        doc = Document(new_content, cursor_position=len(new_content))
        self.left_area.document = doc

        self.app.invalidate()

    def __create_shortcuts(self):
        keyboard = KeyBindings()

        # Control + C -> Salir de la interfaz
        keyboard.add("c-c")(lambda event: event.app.exit())

        # Control + R -> Reiniciar la interfaz
        keyboard.add("c-r")(lambda event: event.app.exit())

        # Tab -> Cambiar entre paneles
        keyboard.add("tab")(lambda event: event.app.layout.focus_next())

        # Control + U -> Actualizar contenido de la terminal (como ejemplo)
        keyboard.add("c-u")(lambda event: self.update_terminal_content())

        return keyboard

    def _start_file_watcher(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self._on_file_modified

        observer = Observer()
        observer.schedule(event_handler, path=self.terminal.file.pathFile, recursive=False)
        observer.start()

        threading.Thread(target=self._watch_file, args=(observer,), daemon=True).start()

    def _on_file_modified(self, event):
        if event.src_path == self.terminal.file.pathFile:
            self.update_terminal_content()

    def _watch_file(self, observer):
        try:
            observer.join()
        except KeyboardInterrupt:
            observer.stop()

    def show(self):
        self.app.run()
