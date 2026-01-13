from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, DirectoryTree, Button


class PathScreen(Screen):

    BINDINGS = [
        ("b","path_back_to_hello","back")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Test")
        yield Footer()

    def action_path_back_to_hello(self) -> None:
        self.app.pop_screen()

class HelloScreen(Screen):

    BINDINGS = [
        ("s","selectPath","Select A Deck")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Hello Screen")
        yield Footer()

    def action_selectPath(self) -> None:
        self.app.push_screen(PathScreen()) # push and pop screens only from the app


class MemoApp(App):

    CSS_PATH = "memomd.tcss"
    BINDINGS = []

    def on_mount(self): 
        self.push_screen(HelloScreen())



    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Tmam")
        yield Footer()

    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     if(event.button.id == "sel"):
    #         self.push_screen(PathScreen())


if __name__ == "__main__":
    app = MemoApp()
    app.run()