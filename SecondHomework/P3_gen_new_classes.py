__author__="Marchelo Bragagnini <cesarbrma91@gmail>"
__date__="$Dic 09,2016"

import sys

from collections import defaultdict

CLASS_NUMERICAL = "_Numeric_"
CLASS_ALL_CAPITALS = "_All_Capitals_"
CLASS_LAST_CAPITAL = "_Last_Capitals_"
CLASS_RARE = "_RARE_"

class Gen_new_classes(object):
    def __init__(self):
        self.emission_counts = defaultdict(int)
    
    def read_data_train(self, corpus_file):
        self.__init__()
        for line_file in corpus_file:
            line = line_file.strip()
            if line:
                fields = line.split(" ")
                self.emission_counts[fields[0]] += 1
    
    def is_numeric(self, word):
        for x in word:
            if x >= '0' and x <= '9':
                return True
        return False

    def is_all_capitals(self, word):
        for x in word:
            if not (x >= 'A' and x <= 'Z'):
                return False
            return  True
    
    def is_last_capital(self, word):
        x = word[-1]
        return x >= 'A' and x <= 'Z'
            
    def map_word(self, word, ocurrence):
        if self.emission_counts[word] < ocurrence:
            if self.is_numeric(word):
                return CLASS_NUMERICAL
            elif self.is_all_capitals(word):
                return CLASS_ALL_CAPITALS
            elif self.is_last_capital(word):
                return CLASS_LAST_CAPITAL
            else:
                return CLASS_RARE
        return word
                            
    def gen_new_data_train(self, ocurrence, corpus_file, output):
        for line_file in corpus_file:
            line = line_file.strip()
            if line:
                fields = line.split(" ")
                if len(fields) > 1:
                    output.write("%s %s\n"%(self.map_word(fields[0], ocurrence), fields[1]))
                else:   
                    output.write("%s\n"%(self.map_word(fields[0])))
            else:
                output.write("\n")
                
def usage():
    sys.stderr.write(""" Usage python gen_new_classes.py [data_file])""")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)
    
    try:
        nameDataFile = sys.argv[1]        
    except IOError:
        sys.stderr.write("ERROR:Cannot read inputfile")
        sys.exit(1)
        
    data = Gen_new_classes()
    data.read_data_train(file(nameDataFile))    
    data.gen_new_data_train(5,file(nameDataFile), sys.stdout)
    
                