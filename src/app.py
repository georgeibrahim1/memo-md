import os
from pathlib import Path
from zandev_textual_widgets import FileSelector

from textual.app import App, ComposeResult
from textual.screen import Screen , ModalScreen
from textual.containers import Container, Horizontal, Grid
from textual.widgets import Footer, Label, DirectoryTree, Button, MarkdownViewer, SelectionList, Pretty, Static
from textual.widgets.selection_list import Selection

from helpers.parser import MdParser

from rich_pixels import Pixels
from rich.console import Console

from helpers.theme import forest_theme
from helpers.customized_header import Header

class MemoApp(App):

    BINDINGS = []
    CSS_PATH = "app.tcss"

    def __init__(self):
        super().__init__()
        self.path = ""
        self.falsePerSession = []
        self.truePerSession = []

    def on_mount(self): 
        self.register_theme(forest_theme)
        self.theme = "forest"
        self.push_screen(HelloScreen())

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Tmam")
        yield Footer(show_command_palette=False)

    def get_question_screen_type(self,card):
        question_type = MdParser.get_type_of_question(card)

        if(question_type == "MultipleChoice_Multiple"):
            return "MultipleChoices"
        elif(question_type == "Normal" or question_type == "Photo_Answer"):
            return "NormalorPhoto"

class HelloScreen(Screen):

    BINDINGS = [
        ("s","path","Select A Deck")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        # console = Console()
        # pixels = Pixels.from_image_path(os.path.normpath("assets/forest.jpg") , [150,100])
        # yield Static(pixels)
        yield Footer(show_command_palette=False)

    async def action_path(self):

        def check_if_george_wants_to_gen(value: bool):
            if(value):
                md_wrong_file = MdParser.cards_to_markdown_file(self.app.falsePerSession)
                fileName = os.path.basename(self.app.path)
                os.path.join(self.app.path, "_" + fileName)
                with open("_" + fileName, "w") as file:
                    file.write(md_wrong_file)
                self.app.exit()
            else:
                self.app.exit()

        def selectedPath(value : str):

            if((not os.path.isfile(value)) or len(value) == 0 or Path(value).suffix != ".md"):
                self.app.push_screen(ErrorModalScreen())
                return

            self.app.path = value
            self.app.push_screen(SessionClass(value) , check_if_george_wants_to_gen)

        self.app.push_screen(FileSelector(directory=os.getcwd()), callback=selectedPath) # when this opens and I click cancel, it stills returns a value ! , The future me if you read this and you are not busy, pull request to zandev and fix this issue

class ErrorModalScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(
                "Please Choose a markdown file with the required format!", 
                classes="ErrorLabel"
            ),
            Button(
                "Ok", 
                variant="error",
                id="ErrorButton"
            ),
            classes="ErrorModal"
        )
    
    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()

class SessionClass(Screen):
    def __init__(self,md:str):
        super().__init__()
        self.md = md
        try:
            self.cards = MdParser(self.md).cards
        except:
            self.app.push_screen(ErrorModalScreen())
        

        
    def on_mount(self):
        self._push_questions_screens() # add error validations

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(
                "Do you want to generate a markdown file for your mistakes?",
                id="generateModal_QuestionLabel",
                classes="QuestionLabel"
            ),
            Button(
                "Yes",
                variant="success",
                id="generateModal_YesButton"
            ),
            Button(
                "No",
                variant="error",
                id="generateModal_NoButton"
            ),
            id="generateModal",
            classes="SessionModal"
        )

    def on_button_pressed(self, event:Button.Pressed):
        if(event.button.id == "generateModal_YesButton"):
            self.dismiss(True)
        elif(event.button.id == "generateModal_NoButton"):
            self.dismiss(False) 

    def _push_questions_screens(self):

        n = len(self.cards)

        for x in range(n-1,-1,-1): # add from behind as it's like a stack
            qt = self.app.get_question_screen_type(self.cards[x])
            if(qt == "MultipleChoices"):
                self.app.push_screen(Question_Display_MultipleChoices(self.cards[x]))
            elif(qt == "NormalorPhoto"):
                self.app.push_screen(Question_Display_NormalorPhoto(self.cards[x]))
            else:
                self.app.push_screen(Question_Display_Dummy())


class Question_Display_Dummy(Screen):

    BINDINGS = [
        ("s","skip","Skip")
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        tmam = "This a dummy one, there is a problem in the app!"
        yield MarkdownViewer(tmam, show_table_of_contents=False)
        yield Footer(show_command_palette=False)

    def action_skip(self):
        self.app.pop_screen()


class Question_Display_NormalorPhoto(Screen):

    BINDINGS = [
        ("s","skip","Skip"),
        ("c", "showModal", "Continue")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card
        self.answer_shown = False
    
    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        
        md_question = MarkdownViewer(md_text[0], show_table_of_contents=False, id="questionMarkDown")
        md_question.border_title = "Question"
        
        md_answer = MarkdownViewer(md_text[1], show_table_of_contents=False, classes="hidden", id="answerMarkDown")
        md_answer.border_title = "Answer"
        
        yield Horizontal(
            md_question, 
            Container(
                md_answer,
                Button(
                    "Show Answer", variant="success", id="answerButton"
                ),
                id="Question_Display_answerContainer"
            )
        )
        yield Footer(show_command_palette=False)
    
    # thanks to https://textual.textualize.io/guide/actions/#__tabbed_4_1 (It took me like 3 hours to find a way to make the binding shit dynamic but it is like a gem in a fucking forest)
    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "showModal" and not self.answer_shown:
            return False 
        if action == "skip" and self.answer_shown:
            return False 
        return True

    def on_button_pressed(self,event:Button.Pressed):
        if(event.button.id == 'answerButton'):
            self.get_widget_by_id("answerButton").add_class("hidden") # add class here with the widget class not the styles 
            self.get_widget_by_id("answerMarkDown").remove_class("hidden")
            # self.BINDINGS.insert(1,("Enter" , "showModal" , "continue"))
            # BINDINGS is constant, as it is only rendered or made on the mount of the screen, or edited by app.bind
            self.answer_shown = True
            self.refresh_bindings() 
            

    def action_showModal(self):

        def check_answer(status:bool):
            if status:
                self.app.truePerSession.append(self.card)
            else:
                self.app.falsePerSession.append(self.card)

            self.app.pop_screen()

        self.app.push_screen(IsTrueOrFalseModalScreen() , check_answer)

    def action_skip(self):
        self.app.pop_screen()


class IsTrueOrFalseModalScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(
                "Did you answer this question right?" , id="isTrueOrFalseModa_QuestionLabel", classes="QuestionLabel"
            ),
            Button(
                "Yes", variant="success", id="isTrueOrFalseModal_YesButton"
            ),
            Button(
                "No" , variant="error",id="isTrueOrFalseModal_NoButton"
            ),
            id="isTrueOrFalseModal",
            classes="Modal"
        )
    
    def on_button_pressed(self, event:Button.Pressed):
        if(event.button.id == "isTrueOrFalseModal_YesButton"):
            self.dismiss(True) # pop and return a bool to the questionDisplay Screen
        elif(event.button.id == "isTrueOrFalseModal_NoButton"):
            self.dismiss(False) 


class Question_Display_MultipleChoices(Screen):

    BINDINGS = [
        ("s","skip","Skip"),
        ("u","answer","Submit"),
        ("c","continue","Continue")
    ]

    def __init__(self,card):
        super().__init__()
        self.card = card
        self.answered = False
        self.true_selections_as_indecies = []

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if(action == "continue"):
            return self.answered 
        if(action == "skip"):
            return not self.answered 
        if(action == "answer"):
            return not self.answered 
        return True

    def compose(self) -> ComposeResult:
        yield Header()
        md_text = MdParser.card_to_markdown(self.card)
        txt_bool_choices = MdParser.get_multipleChoices_as_text_bool(self.card)

        selections = []
        true_selections_as_labels = []
        
        for i in range(len(txt_bool_choices)):

            id_s = ""
            if(txt_bool_choices[i][1]):
                id_s = "True_Selection_" + f"{i}"
                true_selections_as_labels.append(Label(txt_bool_choices[i][0]))
                self.true_selections_as_indecies.append(i)
            else:
                id_s = "False_Selection_" + f"{i}"

            s_widget = Selection(txt_bool_choices[i][0] , i , id=id_s)
            selections.append(s_widget)

        md_question = MarkdownViewer(md_text[0], show_table_of_contents=False, id="multipleChoiceQuestionMarkDown")
        md_question.border_title = "Question"
        
        answer_container = Container(
            *true_selections_as_labels,
            id="Question_Display_MultipleChoices_answerContainer",
            classes="hidden"
        )
        answer_container.border_title = "Correct Answer(s)"
        
        selection_list = SelectionList[bool](
            *selections,
            id="sel"
        )
        selection_list.border_title = "Choices"
        
        yield Horizontal(
            md_question, 
            Container(
                selection_list,
                answer_container
            )
        )
        yield Footer(show_command_palette=False)   

    def action_answer(self):
        self.answered = True
        self.refresh_bindings()
        self.get_widget_by_id("Question_Display_MultipleChoices_answerContainer").remove_class("hidden")

        selected = self.query_one(SelectionList).selected

        if(len(selected) != len(self.true_selections_as_indecies)):
            self.app.falsePerSession.append(self.card)
            self.app.pop_screen()
            return

        for x in selected:
            if(x not in self.true_selections_as_indecies):
                self.app.falsePerSession.append(self.card)
                self.app.pop_screen()
                return
        self.app.truePerSession.append(self.card)
    
    def action_continue(self):
        self.app.pop_screen()


    def action_skip(self):
        self.app.pop_screen()

if __name__ == "__main__":
    app = MemoApp()
    app.run()