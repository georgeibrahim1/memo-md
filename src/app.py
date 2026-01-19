import os
from zandev_textual_widgets import FileSelector

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, DirectoryTree, Button, MarkdownViewer

from helpers.parser import MdParser


# class PathScreen(Screen):

#     BINDINGS = [
#         ("b","path_back_to_hello","back")
#     ]

#     def compose(self) -> ComposeResult:
#         yield Header()
#         yield Label("Test")
#         yield Footer()

#     def action_path_back_to_hello(self) -> None:
#         self.app.pop_screen()



class HelloScreen(Screen):

    BINDINGS = [
        ("s","path","Select A Deck")
    ]

    def compose(self) -> ComposeResult:

        self.b = MdParser("format.md") # compose runs before on_mount 

        yield Header()
        yield Label("Hello Screen")
        md_text = self.b.cards_to_markdown()
        yield MarkdownViewer(md_text , show_table_of_contents=False)
        yield Footer()

    async def action_path(self):
        def selectedPath(value):
            print(f"{value}")

        self.app.push_screen(FileSelector(directory=os.getcwd()), callback=selectedPath)


class MemoApp(App):

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


# here will be a function that takes the cards as parameter
# there will be a parameter here to save the wrong ones
# for each card
    # a function to get the type of display (it will be different from the type of question function)
    # function to take user input :
        # photo or normal -> enter -> true or false screen
        # multiple choice -> keys up and down -> enter
        # fill in gaps -> keyboard and display what is written -> enter
        # order -> up and down keys -> enter
        # --------> enter
        # a function from session class to grade or determine which is true , it will be used for specific 
    # a function to make two or one file to test again for the wrong ones 


if __name__ == "__main__":
    app = MemoApp()
    app.run()