#Import libraries
import re
import requests
import pandas as pd
from .constants import OMIM_MAPPING_URL, URL

def get_data(url):
    """
    A function to get data from url ('http://www.uniprot.org/docs/mimtosp.txt')
    and parse it to a list of lists contains OMIM IDs, genes or proteins names
    and uniprot IDs.

    :param str url: http://www.uniprot.org/docs/mimtosp.txt
    :rtype: list
    """
    # get data from url as text and save it in 'txt'
    resp = requests.get(url)
    txt = resp.text
    #txt=open("mimtosp.txt","r").readlines()

    final_text=[] # a list to have final list that returned by the function.
    start_reading_bol = False # a semaphore to allow or deny reading lines.
    prev_list=[] # a list to save the previous line if it has OMIM id.
    for line in txt.split('\n'): # split the text by 'new line' and loop.
        start_reading_bol = start_reading(line, start_reading_bol) # open or close the semaphore.
        if start_reading_bol: # if the semaphore is opened
            # get each line as a list after filtering it
            text_list = list(filter(filter_text,re.split(" |  |'|(|)", re.sub('[:,(,),\n]','',line))))
            length_list=len(text_list) # get the lenght of the list
            """
            if the line contains OMIM id and have more than one protein
            then create a new record for each protein
            """
            if not length_list % 2==0 and length_list>3:
                final_text.append([text_list[0],text_list[1],text_list[2]])
                for i in range(3,length_list,2):
                    new_text_list=[text_list[0],text_list[i],text_list[i+1]]
                    final_text.append(new_text_list)
            elif length_list%2 == 0:
                """
                if the line doesn't contain OMIM id, the it related to the previous line
                """
                for i in range(0,length_list,2):
                    new_text_list=[prev_list[0],text_list[i],text_list[i+1]]
                    final_text.append(new_text_list)
            else:
                """
                if the OMIM id has only one protein
                """
                final_text.append(text_list)
            if not length_list % 2==0:
                """
                if the line has OMIM id, then save it as a list to use it when we have new line without OMIM id
                """
                prev_list=text_list

    omim_pheno = get_omim_phenotype_ids()

    s1 = set([entry[0] for entry in final_text[1:-1]])

    return [entry for entry in final_text[1:-1] if entry[0] in omim_pheno]

"""
A function uses to filter lists
"""
def filter_text(text):
    remove = [",","",None]
    if text in remove:
        return False
    else:
        return True

"""
Controling the semaphore
"""
def start_reading(line, reading_bool):
    """This function is checking the start of the lines

    :param str line: line
    :rtype: bool
    """
    if line.startswith("_"):
        return True
    elif line.startswith("-"):
        return False
    else:
        return reading_bool

def get_omim_phenotype_ids():
    """This function will return a list of OMIM Ids that link to phenotypes"""
    mapping = pd.read_csv(OMIM_MAPPING_URL, sep="\t", header=4)
    mapping = mapping.loc[mapping["MIM Entry Type (see FAQ 1.3 at https://omim.org/help/faq)"].isin(["phenotype", "predominantly phenotypes"])]
    return set(mapping["# MIM Number"].apply(str))
