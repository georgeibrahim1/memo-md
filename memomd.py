from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, DirectoryTree, Button


class PathScreen(Screen):

    BINDINGS = [
        ("q","request_qut","qut")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Test")
        yield Footer()

    def action_request_qut(self) -> None:
        self.app.pop_screen()

class MemoApp(App):

    CSS_PATH = "memomd.tcss"
    BINDINGS = [
        ("s","selectPath","Select A Deck")
    ]

    # def on_mount(self): 
    #     self.screen.styles.background = "darkblue"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Tmam")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if(event.button.id == "sel"):
            self.push_screen(PathScreen())

    def action_selectPath(self) -> None:
        self.push_screen(PathScreen())


if __name__ == "__main__":
    app = MemoApp()
    app.run()