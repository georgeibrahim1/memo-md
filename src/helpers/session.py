class Session:
    def __init__(self,cards,no_of_questions): # TODO : pass the cards.len or customized no.
        self.cards = cards
    
    @staticmethod
    def _get_type_of_question(card):

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

        for line in answer:
            if(line.strip() == ""):
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
        pass