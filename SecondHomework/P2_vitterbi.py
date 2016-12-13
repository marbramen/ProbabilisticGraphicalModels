__author__="Marchelo Bragagnini <cesarbrma91@gmail>"
__date__="$Dic 09,2016"

import sys
from collections import defaultdict

CLASS_WORD_LOW_FREQUENT = "_RARE_"
CLASS_NUMERICAL = "_Numeric_"
CLASS_ALL_CAPITALS = "_All_Capitals_"
CLASS_LAST_CAPITAL = "_Last_Capitals_"
CLASS_RARE = "_RARE_"
WORD_INI = "*"
WORD_FIN = "STOP"
IS_4_CLASS = "1"

class Cla_4_words(object):
    @staticmethod
    def is_numeric(word):
        for x in word:
            if x >= '0' and x <= '9':
                return True
        return False
    
    @staticmethod
    def is_all_capitals(word):
        for x in word:
            if not (x >= 'A' and x <= 'Z'):
                return False
            return  True
    @staticmethod
    def is_last_capital(word):
        x = word[-1]
        return x >= 'A' and x <= 'Z'

class Vitterbi(object):
    def __init__(self, flag):
        self.flag= flag
        self.s_all_tags = list()
        self.all_words = set()
        self.c_tags = defaultdict(int)
        self.emission_counts = defaultdict(int)        
        self.q_ubt = defaultdict(float) # q parameter(unigram, bigram, trigram)        
        self.bp = defaultdict
        
    def gen_attributes(self, count_file):
        self.__init__(self.flag)
        set_all_tags = set()        
        total_tags = 0
        c_ubt = defaultdict(int) # counts for unigram, bigram, trigram
        for line_file in count_file:
            line = line_file.strip()            
            fields = line.split(" ")
            # generate e(xi|yi) and c()
            # gen the unigram (q(u)=c(u)/c()),bigram(q(v|u)=c(u,v)/c(u)) is not 
            # neccesarily because is not usefull smothing the trigram model            
            if fields[1] == "WORDTAG":                
                set_all_tags.add(fields[2])
                self.all_words.add(fields[3])
                self.emission_counts[(fields[2], fields[3])] += int(fields[0])            
                total_tags += int(fields[0])                
            elif fields[1] == "1-GRAM":
                self.c_tags[fields[2]] = int(fields[0])
            elif fields[1] == "2-GRAM":
                c_ubt[(fields[2], fields[3])] = int(fields[0])
            elif fields[1] == "3-GRAM":
                c_ubt[(fields[2],fields[3],fields[4])] = int(fields[0])
                self.q_ubt[(fields[4],fields[2],fields[3])] = (1.0 * c_ubt[(fields[2],fields[3],fields[4])]) / c_ubt[(fields[2], fields[3])]
                                         
        self.s_all_tags = list(set_all_tags)          

    def mapWo(self, word):
        if word not in self.all_words:
            if self.flag == IS_4_CLASS:                        
                if Cla_4_words.is_numeric(word):
                    return CLASS_NUMERICAL
                elif Cla_4_words.is_all_capitals(word):
                    return CLASS_ALL_CAPITALS
                elif Cla_4_words.is_last_capital(word):
                    return CLASS_LAST_CAPITAL
                else:
                    return CLASS_RARE
            else:
                return CLASS_WORD_LOW_FREQUENT            
        return word

    def get_emmi_value(self, x, y):
        return (1.0 * self.emission_counts[(y,x)]) / self.c_tags[y]
            
    def execute_with_bp(self, words):    
        n = words.__len__()
        tags = [None] * (n+1)
        bp = defaultdict()      
        pi = defaultdict(float)
        pi[(0,WORD_INI,WORD_INI)] = 1.0
        tup_pro = (-1.0,"")   
        
        for k in xrange(1,n+1):
            x_k = self.mapWo(words[k-1])
            for u in self.s_all_tags:                
                if k == 1:
                    u = WORD_INI
                for v in self.s_all_tags:
                    tup_pro = (-1.0, "")
                    for w in self.s_all_tags:
                        if k <= 2:
                            w = WORD_INI
                        temp = pi[k-1,w,u] * self.q_ubt[v,w,u] * self.get_emmi_value(x_k,v)
                        if tup_pro[0] < temp:
                            tup_pro = (temp, w)                   
                    pi[(k,u,v)] = tup_pro[0]    
                    bp[(k,u,v)] = tup_pro[1]   
                   
        prob = -1.0
        for u in self.s_all_tags:
            if n == 1:
                u = WORD_INI
            for v in self.s_all_tags:
                temp = pi[n,u,v] * self.q_ubt[(WORD_FIN,u,v)]
                if prob < temp:
                    prob = temp
                    tags[n-1] = u
                    tags[n] = v
                       
        for k in xrange(n-2,-1,-1):
            tags[k] = bp[(k+2, tags[k+1],tags[k+2])]        
        return tags                       
                       
    def calculate_tags(self, corpus_file, output):
        words = list()
        for line_file in corpus_file:         
            line = line_file.strip()
            if line:
                line = line.split(" ")
                words.append(line[0])                        
            else:                            
                tags = self.execute_with_bp(words)            
                for i in xrange(0, words.__len__()):
                    output.write("%s %s\n"%(words[i],tags[i+1]))
                words = list()                
                output.write("\n")
        tags = self.execute_with_bp(words)        
        for i in xrange(0,words.__len__()):
            output.write("%s %s\n"%(words[i], tags[i+1]))
                                    
def usage():
    sys.stderr.write(""" Usage python emission_tag.py [count_file] [test_file]  \n""")                           
                           
if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)
    
    try:
        nameCountFile = sys.argv[1]
        nameTestFile = sys.argv[2]
        flag = sys.argv[3]
        inputCountFile = file(nameCountFile)
        inputTestFile = file(nameTestFile)
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfiles %s and %s \n" % sys.argv[1])
        sys.exit(1)    
    vit = Vitterbi(flag)    
    vit.gen_attributes(inputCountFile)    
    vit.calculate_tags(inputTestFile, sys.stdout)
                                        