# If on Python 2.X
#from _future_ import print_function
import pysolr
import NLPFeatures as fl
import glob
import errno
import os
from spacy import displacy
from nltk.tokenize import sent_tokenize, word_tokenize
# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/Question_Answering', timeout = 1000)
path = '/Users/ramesh/Documents/GitHub/Question-Answering-System/WikipediaArticles/*.txt'
docs = []
sent_tokens = []
def readFiles(path):
    files = glob.glob(path)
    for name in files:
        nameOfFile = (os.path.basename(name))
        print("Started indexing for ",nameOfFile)
        try:
            with open(name,encoding="utf-8-sig") as f:
            #with open(name,encoding="latin-1") as f:
                file = f.read()
                docs.append(file)
                sent_tokens = [] ## bugfix
                sent_tokens.extend(sent_tokenize(file))
                doc_sentences = [dict() for x in range(len(sent_tokens))]
                word_tokens=[]
                lemmatize_word=[]
                rootOfSentence=[]
                synonymns_list=[]
                hypernyms_list=[]
                hyponyms_list=[]
                meronyms_list=[]
                holonyms_list=[]
                entities_list = []
                entity_labels_list = []
                stemmatize_word = []
                dependency_parsed_tree =[]
                POS_tags = []
                for i in range(0,len(sent_tokens)):
                    a,b,c,d,e,f,g,h,i1,j,k,l,m = fl.getNLPFeatures(sent_tokens[i])
                    #print("sentence", i, "done")
                    word_tokens.append(a)
                    lemmatize_word.append(b)
                    rootOfSentence.append(c)
                    synonymns_list.append(d)
                    hypernyms_list.append(e)
                    hyponyms_list.append(f)
                    meronyms_list.append(g)
                    holonyms_list.append(h)
                    entities_list.append(i1)
                    entity_labels_list.append(j)
                    stemmatize_word.append(k)
                    dependency_parsed_tree.append(l)
                    POS_tags.append(m)
                indexSolr(nameOfFile,doc_sentences,sent_tokens,word_tokens,lemmatize_word,rootOfSentence,
                          synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list, entities_list, entity_labels_list, stemmatize_word, dependency_parsed_tree, POS_tags)
        except IOError as exc: #Not sure what error this is
            if exc.errno != errno.EISDIR:
                raise

def indexSolr(name, doc_sentences,sentences, word_tokens,lemmatize_word,rootOfSentence,
              synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list,entities_list, entity_labels_list, stemmatize_word, dependency_parsed_tree, POS_tags):
    for i in range(0,len(sentences)):
        doc_sentences[i]["name"] = name
        doc_sentences[i]["sentence"] = sentences[i] 
        doc_sentences[i]["word_tokens"] = word_tokens[i]
        doc_sentences[i]["POS_tags"] = POS_tags[i]
        doc_sentences[i]["lemmatize_word"] = lemmatize_word[i] 
        doc_sentences[i]["rootOfSentence"] = rootOfSentence[i]
        doc_sentences[i]["synonymns_list"] = synonymns_list[i] 
        doc_sentences[i]["hypernyms_list"] = hypernyms_list[i]
        doc_sentences[i]["hyponyms_list"] = hyponyms_list[i] 
        doc_sentences[i]["meronyms_list"] = meronyms_list[i]
        doc_sentences[i]["holonyms_list"] = holonyms_list[i]
        doc_sentences[i]["entities_list"] = entities_list[i]
        doc_sentences[i]["entity_labels_list"] = entity_labels_list[i]
        doc_sentences[i]["stemmatize_word"] = stemmatize_word[i]
        doc_sentences[i]["dependency_parsed_tree"] = dependency_parsed_tree[i]
        
        
    solr.add(doc_sentences, commit = True)
    print("**************Indexing done for the file ",name)


readFiles(path)