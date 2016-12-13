__author__="Marchelo Bragagnini <cesarbrma91@gmail.com>"
__date__ ="$Dic 09, 2016"

import sys
from collections import defaultdict
    
class EmissioTags(object):
    def __init__(self):
        self.all_tags = list()
        self.all_words = set()
        self.tags_counts = defaultdict(int)
        self.emission_counts = defaultdict(int)
        
    def obtain_tags_words(self, count_file):
        self.__init__()
        set_all_tags = set()        
        for line_file in count_file:
            line = line_file.strip()
            fields = line.split(" ")
            if fields.__len__() != 4:
                break
            set_all_tags.add(fields[2])
            self.all_words.add(fields[3])            
            
        self.all_tags = list(set_all_tags)        
        count_file.close()            
                            
    def count_tags_wordsTags(self, count_file):
        for line_file in count_file:
            line = line_file.strip()
            fields = line.split(" ")
            if fields.__len__() != 4:
                break
            self.tags_counts[fields[2]] += int(fields[0])
            # first element: tag | second element: word
            self.emission_counts[(fields[2], fields[3])] += int(fields[0])
        count_file.close()    
    
    def gen_tagger(self, corpus_file, output):
        for line_file in corpus_file:
            line = line_file.strip()            
            if line: #Nonempty line
                word = line.split(" ")[0]                
                tag = ""
                probabilitie  = -1.0
                if word not in self.all_words:
                    word = "__RARE__"                
                # Exist the word in the train set                
                # Disease
                for i in xrange(0, self.all_tags.__len__()):
                    emission_probabilitie = float(self.emission_counts[(self.all_tags[i], word)]) / float(self.tags_counts[self.all_tags[i]])
                    if emission_probabilitie > probabilitie:
                        probabilitie = emission_probabilitie
                        tag = self.all_tags[i]
                output.write("%s %s\n" %(line.split(" ")[0], tag))                    
            else:
                output.write(line_file)
                    
        corpus_file.close()        
            
def usage():
    sys.stderr.write(""" Usage python emission_tag.py [key_file] , just one file \n""")

if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        usage()
        sys.exit(2)
    try:
        nameCountFile = sys.argv[1]
        nameDevFile = sys.argv[2]
        inputCountFile = file(nameCountFile)
        inputDevFile = file(nameDevFile)
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % sys.argv[1])
        sys.exit(1)
        
    emiHMM = EmissioTags()    
    emiHMM.obtain_tags_words(file(nameCountFile))
    emiHMM.count_tags_wordsTags(file(nameCountFile))
    emiHMM.gen_tagger(file(nameDevFile), sys.stdout)
