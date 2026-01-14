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
        
        print("=======",cards)
         

b = MdParser("format.md")
