# Custom tokenizer

class Tokenizer:
    def __init__(self):
        self.vocab=[]

    def encode(self, text:str):
        tokens=[]
        for word in text.split():
            if word not in self.vocab:
                tokens.append(len(self.vocab))
                self.vocab.append(word)
            else:
                tokens.append(self.vocab.index(word))
        return tokens
    
    def decode(self, tokens):
        try:
            tokens = list(map(int, tokens.split()))
            words=[]
            for token in tokens:
                try:
                    words.append(self.vocab[token])
                except IndexError:
                    words.append("<UNWN-TKN>")
            return " ".join(words)
        except ValueError:
            return "Please provide valid input"

tokenizer = Tokenizer()
instructions = "Please enter '--encode' to encode, '--decode' to decode and '--vsize' for vocab size --> "

while True:    
    user_input = input(instructions)
    if user_input == '--encode':
        print("Tokens:", tokenizer.encode(input("--> ")))
    elif user_input == '--decode':
        print("Please enter 'Space' separated tokens")
        print("Output:", tokenizer.decode(input("--> ")))
    elif user_input == '--vsize':
        print("Vocab Size:", len(tokenizer.vocab))
    else:
        print("Please provide valid input")
        print(instructions)