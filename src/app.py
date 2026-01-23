import os
from zandev_textual_widgets import FileSelector

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Label, DirectoryTree, Button, MarkdownViewer

from helpers.parser import MdParser


class MemoApp(App):

    BINDINGS = []

    def on_mount(self): 
        self.push_screen(HelloScreen())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Tmam")
        yield Footer()

    def get_question_screen_type(self,card):
        question_type = MdParser.get_type_of_question(card)

        if(question_type == "Fill_In_Gap"):
            return "FillInGaps"
        elif(question_type == "MultipleChoice_Multiple" or question_type=="MultipleChoice_One"):
            return "MultipleChoices"
        elif(question_type == "Normal" or question_type == "Photo_Answer"):
            return "NormalorPhoto"
        elif(question_type == "Order"):
            return "Order"


class HelloScreen(Screen):

    BINDINGS = [
        ("s","path","Select A Deck")
    ]

    def compose(self) -> ComposeResult:

        # self.b = MdParser("format.md") # compose runs before on_mount 

        yield Header()
        yield Label("Hello Screen")
        # md_text = self.b.cards_to_markdown()
        # yield MarkdownViewer(md_text , show_table_of_contents=False)
        yield Footer()

    async def action_path(self):
        def selectedPath(value):
            parsed = MdParser(value)
            self.push_questions_screens(parsed.cards) # add error validations

        self.app.push_screen(FileSelector(directory=os.getcwd()), callback=selectedPath)


    def push_questions_screens(self,cards):

        n = len(cards)

        for x in range(n-1,-1,-1): # add from behind as it's like a stack
            qt = self.app.get_question_screen_type(cards[x])
            if(qt == "FillInGaps"):
                self.app.push_screen(Question_Display_FillInGaps(cards[x]))
            elif(qt == "MultipleChoices"):
                self.app.push_screen(Question_Display_MultipleChoices(cards[x]))
            elif(qt == "NormalorPhoto"):
                self.app.push_screen(Question_Display_NormalorPhoto(cards[x]))
            elif(qt == "Order"):
                self.app.push_screen(Question_Display_Order(cards[x]))
            else:
                self.app.push_screen(Dummy())



class Dummy(Screen):

    BINDINGS = [
        ("s","skip","Skip")
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        tmam = "udaovhovbrb"
        yield MarkdownViewer(tmam, show_table_of_contents=False)
        yield Footer()

    def action_skip(self):
        self.app.pop_screen()


class Question_Display_NormalorPhoto(Screen):

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("s","skip","Skip")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card
    
    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        yield Horizontal(
            MarkdownViewer(md_text[0], show_table_of_contents=False), 
            Container(
                MarkdownViewer(md_text[1] , show_table_of_contents=False , classes="hidden" , id="answerMarkDown"),
                Button(
                    "Show Answer" , variant="success" , id="answerButton"
                ),
                id="Question_Display_NormalorPhoto_answerContainer"
            )
        )
        yield Footer()
    

    def on_button_pressed(self,event:Button.Pressed):
        if(event.button.id == 'answerButton'):
            self.get_widget_by_id("answerButton").add_class("hidden") # add class here with the widget class not the styles 
            self.get_widget_by_id("answerMarkDown").remove_class("hidden")

    def action_skip(self):
        self.app.pop_screen()

class Question_Display_MultipleChoices(Screen):

    BINDINGS = [
        ("s","skip","Skip")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card

    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        yield MarkdownViewer(md_text[0], show_table_of_contents=False)
        yield Footer()

    def action_skip(self):
        self.app.pop_screen()

class Question_Display_FillInGaps(Screen):

    BINDINGS = [
        ("s","skip","Skip")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card

    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        yield MarkdownViewer(md_text[0], show_table_of_contents=False)
        yield Footer()


    def action_skip(self):
        self.app.pop_screen()

class Question_Display_Order(Screen):

    BINDINGS = [
        ("s","skip","Skip")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card

    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        yield MarkdownViewer(md_text[0], show_table_of_contents=False)
        yield Footer()

    def action_skip(self):
        self.app.pop_screen()


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