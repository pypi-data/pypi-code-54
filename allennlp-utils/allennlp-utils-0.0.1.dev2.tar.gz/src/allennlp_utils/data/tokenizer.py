from typing import List

import jieba
from allennlp.data import Tokenizer, Token


@Tokenizer.register("utils-jieba")
class JiebaTokenizer(Tokenizer):
    def tokenize(self, text: str) -> List[Token]:
        tokens = [Token(token) for token in jieba.lcut(text)]
        return tokens
