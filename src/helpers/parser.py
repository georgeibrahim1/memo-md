import re

class MdParser():
    def __init__(self , path):
        self.path = path

        self.data = self._load(path)
        self.filteredData = self._filter_data(self.data)
        self.cards = self._getCards(self.filteredData)

    @staticmethod # static private method as helper ya3ne (gamed walahy)
    def _load(path): 
            try:
                with open(path) as f:
                    data = f.readlines()
                    return data
            except:
                return "Error" # ToDo : Handle Errors (not .md , invalid format)
         
    @staticmethod
    def _filter_data(data):
         
         n = len(data)

         # remove \n from each line
         for x in range(n):
              m = len(data[x])
              if(x != n-1): # last line doesn't have \n 
                data[x] = data[x][0:m-1] 
         return data

    @staticmethod
    def _getCards(data):

        cards = []

        state = "Q" # or "A" for answer concatenation
        question = []
        answer = []

        for line in data:
            if(line.strip() != '<!--seperator-->' and state == "Q"):
                question.append(line)
            elif(line.strip() == '<!--seperator-->' and state == "Q"):
                state = "A"
            elif(line.strip() == "---" and state == "A"):
                cards.append([question,answer]) # [0,1]
                state = "Q"
                question = []
                answer = []
            elif(line.strip() != '<!--seperator-->' and state == "A"):
                answer.append(line)
        return cards

    @staticmethod
    def cards_to_markdown_file(cards):
        md_text = ""
        for card in cards:
            q = ""
            a = ""
            for x in range(len(card[0])):
                q += card[0][x]
                q += "\n"
            for x in range(len(card[1])):
                a += card[1][x]
                a += "\n"
            md_text += q
            md_text += "<!--seperator-->\n"
            md_text += a
            md_text += "---\n"
        return md_text
    
    @staticmethod
    def card_to_markdown(card):
        q = ""
        a = ""
        for x in range(len(card[0])):
            q += card[0][x]
            q += "\n"
        for x in range(len(card[1])):
            a += card[1][x]
            a += "\n"
        
        return [q,a]
    
    @staticmethod
    def get_multipleChoices_as_text_bool(card):
        md_choices = card[1]
        txt_bool_choices = []
        for md_choice in md_choices:
            status = False
            if(len(md_choice) > 2):
                if(md_choice[1] == "*"):
                    status = True
                txt_choice = md_choice[3:]
                txt_bool_choices.append([txt_choice,status])

        return txt_bool_choices
    
    @staticmethod
    def get_question_of_fill_in_gap(card):
        question = card[0]
        return re.sub("__g.__" , "_____", question)

    @staticmethod
    def get_type_of_question(card):

        question = card[0]
        answer = card[1]

        modified_answer = [] # delete spaces

        for line in range(0,len(answer)):
            if(answer[line].strip() == ""):
                pass 
            else:
                modified_answer.append(answer[line])

        for line in modified_answer:

            edited_line = line.strip()

            if(edited_line[0:3] == "[ ]" or edited_line[0:3] == "[*]"):
                return "MultipleChoice_Multiple"
            else: 
                return "Normal"
        
    @staticmethod
    def true_or_false(card):
        pass
    
         

b = MdParser("format.md")
