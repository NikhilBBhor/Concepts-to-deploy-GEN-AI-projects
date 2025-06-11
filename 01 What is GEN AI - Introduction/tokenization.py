# Understanding tokenization

import tiktoken

# understanding vocab size
encoder = tiktoken.encoding_for_model('gpt-4o')
print("Vocab Size:", encoder.n_vocab)  # --> 200019

# encoding text to tokens
text = "The cat sat on the mat"
tokens = encoder.encode(text)
print("Tokens:", tokens)  # --> [976, 9059, 10139, 402, 290, 2450]

# decoding tokens to text
my_tokens = [976, 9059, 10139, 402, 290, 2450]
decoded_text = encoder.decode(my_tokens)
print("Decoded tokens:", decoded_text)

