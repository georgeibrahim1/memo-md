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
                    print(data)
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

        print("Caaaaaaarrrrrrrrrrrdddddddssss" , cards)
        return cards

    def cards_to_markdown(self):
        q = ""
        for card in self.cards:
            for x in range(len(card[0])):
                q += card[0][x]
                q += "\n"
        
        return q
    
    @staticmethod
    def card_to_markdown(card):
        q = ""
        for x in range(len(card[0])):
            q += card[0][x]
            q += "\n"
        
        return q
    
    @staticmethod
    def get_type_of_question(card):

        # normal question
        # multiple choices (one)
        # multiple choices (multiple)
        # fill in gaps
        # order 
            ######## all above can have like open a photo in the question
        # photo (Just open the photo in the answer)


        question = card[0]
        answer = card[1]

        modified_answer = [] # delete spaces

        for line in range(0,len(answer)):
            if(answer[line].strip() == ""):
                pass 
            else:
                modified_answer = answer[line]

        for line in modified_answer:

            edited_line = line.strip()

            first_underline = False
            vertical_line = False
            # second_underline = False


            for x in edited_line:
                if(x == "_"):
                    if(not first_underline):
                        first_underline = True
                    elif(first_underline):
                        if(vertical_line):
                            return "Fill_In_Gap"
                elif(x == "|"):
                    if(first_underline):
                        vertical_line = True


            if(edited_line[0] == "-" or edited_line[0] == "*"):
                return "MultipleChoice_One"
            elif(edited_line[0:2] == "[ ]" or edited_line[0:2] == "[*]"):
                return "MultipleChoice_Multiple"
            elif(edited_line[0:1] == "1." or edited_line[0:1] == "2." or edited_line[0:1] == "3." or edited_line[0:1] == "4."):
                return "Order"
            elif(edited_line[0:10] == "Open Photo:"): 
                return "Photo_Answer" # To be edited, I still didn't decide how to add photo feature
            else: 
                return "Normal"
        
        @staticmethod
        def true_or_false(card):
            pass
    
         

b = MdParser("format.md")
