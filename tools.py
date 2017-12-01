"""Main PyQuran Library  Module

* Data: Sat Nov 18 03:30:41 EET 2017

This module contains tools for `Quranic Analysis`
(More expressive description later) 

"""
from xml.etree import ElementTree
import numpy
from collections import Counter
import operator
from audioop import reverse


# Parsing xml
xml_file_name = 'QuranCorpus/quran-simple-clean.xml'
quran_tree = ElementTree.parse(xml_file_name)


def get_sura(sura_number):
    """gets an sura by returning a list of ayat al-sura.

    Args: 
        param1 (int): the ordered number of sura in The Mushaf.

    Returns:
         [str]: a list of ayat al-sura.

    Usage Note:
        Do not forget that the index of the reunred list starts at zero.
        So if the order aya number is x, then it's at (x-1) in the list.

    """
    sura_number -= 1
    sura = []
    suras_list = quran_tree.findall('sura')
    ayat = suras_list[sura_number]
    for aya in ayat:
        sura.append(aya.attrib['text'])
    return sura





def fetch_aya(sura_number, aya_number):
    """

    Args:
        param1 (int): the ordered number of sura in The Mus'haf.
        param2 (int): the ordered number of aya in The Mus'haf.

    Returns:
        str: an aya as a string

    """
    aya_number -= 1
    sura = get_sura(sura_number)
    return sura[aya_number]


def parse_sura(n, alphabets=['ل', 'ب']):
    """parses the sura and returns a matrix (ndarray),
    the rows number equals to the ayat number,
    and the columns number equals to the length of alphabets

    What it does:
        it calculates number of occurrences of each on of letters
        in the alphabets for each aya.

        If `A` is a ndarray, 
        then A[i,j] is the number of occurrences of the letter 
        alphabets[j] in the aya i.

    Args:
        param1 (int): the ordered number of sura in The Mus'haf.
        param2 ([str]): a list of alphabets

    Returns:
        ndarray: with dimensions (a * m), where
        `a` is the number of ayat el-sura and
        `m` is the number of letters passed to the function through alphabets[]

    Issue:
        1. A list of Arabic letters maybe flipped by your editor,
           so, the first char will be the most-right one,
           unlike a list of English char, the first element 
           is the left-most one.

        2. I didn't make alphabets[] 29 by default. 
           Just try it by filling the alphabets with some letters.
    

    """
    # getting the nth sura
    sura  = get_sura(n)
    # getting the ndarray dimensions 
    a = len(sura)
    m = len(alphabets)
    # building ndarray with appropriate dimensions 
    A = numpy.zeros((a,m), dtype=numpy.int)


    # Filling ndarray with alphabets[] occurrences
    i = 0 # number of current aya
    j = 0 # occurrences
    for aya in sura:
        for letter in alphabets:
            A[i,j] = aya.count(letter)
            j += 1
        j = 0
        i += 1
 
    print(A)
    return A





def get_frequancy(sentence):
    """it take sentence that you want to compute it's 
       frequency.

    Args:
        sentence (string): sentece that compute it's frequency. 

    Returns:
        dict: {str: int}
    """
    # split sentence to words     
    word_list = sentence.split()
    #compute count of uniqe words 
    frequency = Counter(word_list)
    #sort frequency descending
    sorted_freq = dict(sorted(frequency.items(),key=operator.itemgetter(1),reverse=True))
    return sorted_freq
    

    
def generate_frequancy_dictionary(suraNumber=None):
    """It takes and ordered number of a sura, and returns the dictionary:
       * key is the word.  value is its frequency in the Sura.
       - If you don't pass any parameter, then the entire Quran is targeted.
       - This function have to work on the Quran with تشكيل, because it's an
         important factor.

    Args:
        suraNumber (int): it's optional 

    Returns:
        dict: {str: int}
    """
    frequency = {}
    #get all Quran if suraNumber is None
    if suraNumber == None:
        #get all Quran as one sentence
        Quran = ' '.join([' '.join(get_sura(i)) for i in range(1,115)])
        #get all Quran frequency
        frequency=get_frequancy(Quran)
    #get frequency of suraNumber
    else:
        #get sura from QuranCorpus
        sura = get_sura(sura_number=suraNumber)
        ayat = ' '.join(sura)
        #get frequency of sura 
        frequency = get_frequancy(ayat)

    return frequency


def check_sura_with_frequency(sura_num,freq_dec):
    """this function check if frequency dictionary of specific sura is
    compatible with original sura in shapes count

    Args:
        suraNumber (int): sura number 

    Returns:
        Boolean: True :- if compatible 
                 Flase :- if not
    """
    #get number of chars in frequency dec
    num_of_chars_in_dec = sum([len(word)*count for word,count in freq_dec.items()])
    #get number of chars in  original sura
    num_of_chars_in_sura = sum([len(aya.replace(' ',''))  for aya in get_sura(sura_num)])
    print(num_of_chars_in_dec)
    if num_of_chars_in_dec == num_of_chars_in_sura:
        return True
    else:
        return False
    
    
    
def generate_latex_table(dictionary,filename):
    """generate latex code of table of frequency 
    
    Args:
        dictionary (dict): frequency dictionary
        filename (string): file name 
    """
    head_code = """\\documentclass[a4paper,10pt]{article}
%In the preamble section include the arabtex and utf8 packages
\\usepackage{arabtex}
\\usepackage{utf8}
\\usepackage{longtable}    
\\usepackage{color, colortbl}
\\usepackage{supertabular}
\\usepackage{multicol}


\\begin{document}
\\setcode{utf8}
\\twocolumn


\\begin{longtable}{ P{2cm}  P{1cm} P{2cm}  P{1cm}}    
      
      \\textbf{\\Large{words}}    & \\textbf{\\Large{frequancy}}  & \\textbf{\\Large{words}}    & \\textbf{\\Large{frequancy}}  & \\textbf{\\Large{words}}    & \\textbf{\\Large{frequancy}} \\\\
      \\hline"""
            
    tail_code = """\\end{longtable}
\\end{document}"""
      
    file  = open(filename+'.tex', 'w', encoding='utf8')
    file.write(head_code+'\n')
    n = 0
    l = ""
    num_of_words_per_row = 3
    for word, frequancy in dictionary.items():
        line = "\\<"+word+"> & "+str(frequancy)
        n = n+1
        if n!=num_of_words_per_row:
            l = l+line+" & "
        else:
            l = l+line
        if(n==num_of_words_per_row):
            file.write(l+' \\\\ \n')
            l=""
            n=0
            
    file.write(tail_code)
    file.close()
    
    
    
    

def main():
    # testing
#    print(fetch_aya(10, 107))
#    print(get_sura(10)[107-1])
#    parse_sura(111, ['م', 'ا', 'ب'])
    # print(get_sura(1))
    # a = generate_frequancy_dictionary()
    # num = [v for k,v in a.items()]
#   # print(sum(num))
#   # print(get_sura(22))
    # print(len(a))
#   # print(a['الجنة'])

    #check function of sura el hage
    import time
    start = time.time()
    freq = generate_frequancy_dictionary(22)
    print(time.time()-start)
    start = time.time()
    print(check_sura_with_frequency(sura_num=22,freq_dec=freq))
    print(time.time()-start)
    print(freq)
    generate_latex_table(freq,"test")
#     write in file
#     su = open('sura_Al_hag_freq.txt','w',encoding='utf8')
#     n = 0
#     l = ""
#     for key, values in freq.items():
#         line='{},{}'.format(key,values)
#         su.write(line+"\n")
# #         n=n+1
# #         if n !=3:
# #             l = l+line +" & "
# #         else:
#         l = l+line
#         if(n==3):
#            su.write(l+" | \n")
#            n=0
#            l=""
#     su.close()
#     from fpdf import FPDF
# 
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 16)
#     pdf.cell(40, 10, 'Hello World!')
#     pdf.output('tuto1.pdf', 'F')
     
   
     
if __name__ == '__main__':
    main()

        
