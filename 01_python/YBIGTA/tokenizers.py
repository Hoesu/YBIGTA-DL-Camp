import re, collections
from typing import Optional, Union, List, Tuple

# BPETokenizer와 WordTokenizer 클래스의 부모 클래스 정의
class Tokenizer:
    # 토크나이저를 훈련시킬 기본 코퍼스로 초기화.
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        self.record = {}
        self.corpus = corpus
    # 코퍼스를 새롭게 추가.
    def add_corpus(self, corpus: Union[List[str], str]):
        self.corpus = corpus

class BPETokenizer(Tokenizer):
    def __init__(self, corpus):
        super().__init__(corpus)
        
    # 코퍼스로부터 캐릭터 페어 별로 빈도 수를 받아오기.
    def get_stats(self, corpus):
        pairs = collections.defaultdict(int)
        for word, freq in corpus.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                pairs[symbols[i], symbols[i+1]] += freq
        return pairs
    
    # 페어 병합.
    def merge_vocab(self, pair, v_in):
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\\S)' + bigram + r'(?!\\S)')
        for word in v_in:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out
    
    # 코퍼스를 기준으로 가장 빈도 수가 높은 페어들을 순서대로 병합한다.
    # 페어 병합 순서대로 토큰 ID를 지정하고, record에 저장한다.
    def train(self, n_iter: int) -> None:
        for i in range(n_iter):
            pairs = self.get_stats(self.corpus)
            best = max(pairs, key=pairs.get)
            self.corpus = self.merge_vocab(best, self.corpus)
            self.record[best] = i
            
            print("----------------------------------------------------------------------------")
            print("Iteration     : ",i)
            print("New Merge     : ", best)
            print("Updated Corpus: ", self.corpus)
            print("Record        : ", self.record)
    
    # 새로운 텍스트 인풋을 받아서 페어 반환.   
    def get_pairs(self, text: Union[List[str], str] ) -> List[Tuple[str, str]]:
        pairs = set()
        
        if isinstance(text, str):
            text = tuple(text) + ("</w>",)
            prev_char = text[0]
            for char in text[1:]:
                pairs.add((prev_char, char))
                prev_char = char
            return pairs
        
        elif isinstance(text, list) and all(isinstance(elem, str) for elem in text):
            for line in text:
                line = tuple(line) + ("</w>",)
                prev_char = line[0]
                for char in line[1:]:
                    pairs.add((prev_char, char))
                    prev_char = char
            return pairs

        else:
            raise ValueError("Input must be a string or a list of strings")
    
    # 코퍼스로 학습한 내용을 바탕으로 새로운 인풋에 대한 토크나이즈.
    def tokenize(self, text: Union[List[str], str]) -> List[Tuple[str, int]]:
        pairs = self.get_pairs(text)
        
        
        
        
        
        return pairs


        
        
        
        
    
vocab = {
'l o w </w>': 5,
'l o w e r </w>': 2,
'n e w e s t </w>': 6,
'w i d e s t </w>': 3
}
num_merges = 5

tokenizer = BPETokenizer(vocab)
tokenizer.train(num_merges)

text = ['Hoesu','Chung','Ybigta']
print(tokenizer.tokenize(text))