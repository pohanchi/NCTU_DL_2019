import numpy as np 
import pandas
import pickle
import nltk
from nltk.stem import PorterStemmer


class prepro_iter():
    def __init__(self,data,word2idx):
        super(prepro_batch).__init__()
        self.data = data
        self.word2idx = pickle.load(open(word2idx,'rb'))

    def __len__(self):
        return len(self.data)

    def batch_iter(self,bs=32):
        idx = 0
        while(idx+bs) < len(self):
            seq_len = self.seq_len[idx:idx+bs]
            max_len = max(seq_len)
            no_pads = self.data[idx:idx+bs]
            seqs = np.array([ x+word2idx['<pad>']*(max_len-len(x)) for x in no_pads['sequence']],dytpe=np.int8)
            labels = np.array([x for x in no_pads['label']],dtype=np.int8)
            idx+= bs
            yield seqs, labels

    def __shuffle__(self):
        self.data=shuffle(self.data)
        
    def epoch_iter(self):
        self.shuffle(self)
        self.seq_len = [len(x['sequence']) for x in self.data]
        return 
        
            
        
    



def filter_token(string):
    # Characters filters.
    filters = '!"#$%&()*+,./:;<=>?@[\\]^_{|}~\t\n'
    for c in filters:
        string = string.replace(c, ' ')
    return string

def tokenize(corpus):
    sentences = [filter_token(x.lower()).split() for x in corpus]
    
    return sentences

def prepro_xlsx(file_name):
    dF=pandas.read_excel(file_name)
    array = np.array(dF)
    lines=list(array[:,0])
    clean = tokenize(lines)
    return clean

if __name__ == "__main__":
    
    vocabulary = []
    all_corpus = []

    ac_token=prepro_xlsx("ICLR_accepted.xlsx")
    re_token=prepro_xlsx("ICLR_rejected.xlsx")
    all_corpus += ac_token
    all_corpus += re_token
    
    pickle.dump(ac_token,open('accepted_sentence.p','wb'))
    pickle.dump(re_token,open('rejected_sentence.p','wb'))

    pickle.dump(all_corpus,open('all_corpus.p','wb'))

    for sentence in all_corpus:
        for token in sentence:
                vocabulary.append(token)
    vocabulary=set(vocabulary)
    
    word2idx = {w: idx+1 for (idx, w) in enumerate(vocabulary)}
    print('origin_word2idx',word2idx)
    idx2word = {(idx+1): w for (idx, w) in enumerate(vocabulary)}
    print('origin_idx2word',word2idx)
    word2idx['<pad>'] = 0
    print('word2idx=',word2idx)
    idx2word[0] = '<pad>'
    print('idx2word=',idx2word)
    t_data = [{'sentence': [word2idx[k] for k in s], 'label': 1} for s in ac_token]
    f_data = [{'sentence': [word2idx[k] for k in s], 'label': 0} for s in re_token]

    pickle.dump(word2idx,open('word2idx.p','wb'))
    pickle.dump(idx2word,open('idx2word.p','wb'))

    pickle.dump(t_data,open("true_data.p",'wb'))
    pickle.dump(f_data,open("false_data.p",'wb'))
    


    

    
    



    









