import re, collections
from typing import Optional, Union, List, Tuple

from YBIGTA.preprocessor import TextPreprocessor


# BPETokenizer와 WordTokenizer 클래스의 부모 클래스 정의
class Tokenizer:
    # 토크나이저를 훈련시킬 기본 코퍼스로 초기화.
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        self.record = {}
        processor = TextPreprocessor(corpus)
        self.corpus = processor.get_corpus()

    # 코퍼스를 새롭게 추가.
    def add_corpus(self, corpus: Union[List[str], str]):
        processor = TextPreprocessor(corpus)
        self.corpus = processor.get_corpus()
        
class WordTokenizer(Tokenizer):
    def __init__(self, corpus):
        super().__init__(corpus)

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
            
            #print("----------------------------------------------------------------------------")
            #print("Iteration     : ",i)
            #print("New Merge     : ", best)
            #print("Updated Corpus: ", self.corpus)
            #print("Record        : ", self.record)
    
    # 새로운 텍스트 인풋을 받아서 페어 반환.   
    def get_pairs(self, text: Union[List[str], str]) -> List[Tuple[str, str]]:
        pairs = set()
        prev_char = text[0]
        for char in text[1:]:
            pairs.add((prev_char, char))
            prev_char = char
        return pairs
    
    # 코퍼스로 학습한 내용을 바탕으로 새로운 인풋에 대한 토크나이즈.
    def tokenize(self, text: Union[List[str], str]) -> List[Tuple[str, int]]:
        
        text = list(text) + ["</w>"]
        pairs = self.get_pairs(text)
        iteration = 0
            
        while True:
            print("----------------------------------------------------------------------------")
            iteration += 1
            print("iteration            : {}".format(iteration))
            print("pairs in the text    : {}".format(pairs))
            candidate = min(pairs, key = lambda pair: self.record.get(pair, float('inf')))
            print("candidate for merging: {}".format(candidate))
                
            if candidate not in self.record:
                print("Candidate not in BPE merges, algorithm stops.")
                break
                
            first, second = candidate
            new_text = []
            i = 0
            while i < len(text):
                try:
                    j = text.index(first, i)
                    new_text.extend(text[i:j])
                    i = j
                except:
                    new_text.extend(text[i:])
                    break

                if text[i] == first and i < len(text)-1 and text[i+1] == second:
                    new_text.append(first+second)
                    i += 2
                else:
                    new_text.append(text[i])
                    i += 1
            text = new_text
                
            print("text after merging: {}".format(text))
                
            if len(text) == 1:
                break
            else:
                pairs = self.get_pairs(text)
                print(text)
                print(pairs)
                    
        return text

        


        
        
        
"""
vocab = {
'l o w </w>': 5,
'l o w e r </w>': 2,
'n e w e s t </w>': 6,
'w i d e s t </w>': 3
}
num_merges = 5

tokenizer = BPETokenizer(vocab)
tokenizer.train(num_merges)

text1 = 'highest'
text2 = "Usain Bolt rounded Horse neighed"

print(tokenizer.tokenize(text1))
"""