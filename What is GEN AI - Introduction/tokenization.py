# Understanding tokenization

import tiktoken

encder = tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size: ", encder.n_vocab)  # --> 200019