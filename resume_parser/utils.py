import io
import os
import re
from typing import Optional, List, Dict

import docx2txt
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from spacy.tokens import Doc

from . import constants as cs
from .constants import *

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted
    :return: string of extracted text
    """
    with open(pdf_path, 'rb') as fh:
        text = ""
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text += fake_file_handle.getvalue()

            converter.close()
            fake_file_handle.close()
        return text

def extract_text_from_doc(doc_path: str) -> str:
    """
    Helper function to extract plain text from .doc or .docx files

    :param doc_path: path to .doc or .docx file to be extracted
    :return: string of extracted text
    """
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def extract_text(file_path: str) -> str:
    """
    Wrapper function to detect the file extension and call text extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :return: string of extracted text
    """
    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif extension in ['.docx', '.doc']:
        return extract_text_from_doc(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

def extract_entity_sections(text: str) -> Dict[str, List[str]]:
    """
    Helper function to extract all the raw text from sections of resume

    :param text: Raw text of resume
    :return: dictionary of entities
    """
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    return entities

def extract_email(text: str) -> Optional[str]:
    """
    Helper function to extract email id from text

    :param text: plain text extracted from resume file
    :return: email id if found, else None
    """
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
    return None

def extract_name(nlp_text: Doc, matcher) -> Optional[str]:
    """
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    """
    pattern = [cs.NAME_PATTERN]
    matcher.add('NAME', None, *pattern)
    matches = matcher(nlp_text)
    for _, start, end in matches:
        span = nlp_text[start:end]
        return span.text
    return None

def extract_mobile_number(text: str) -> Optional[str]:
    """
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    """
    # Moroccan phone number pattern
    pattern = r"(\+212|0)([ \-_/]*)(\d[ \-_/]*){9}"
    match = re.search(pattern, text)
    if match:
        return match.group().replace(" ", "").replace("-", "").replace("_", "").replace("/", "")
    return None

def extract_skills(nlp_text: Doc, noun_chunks: List) -> List[str]:
    """
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    """
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv'))
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def cleanup(token: str, lower: bool = True) -> str:
    if lower:
        token = token.lower()
    return token.strip()

def extract_education(nlp_text: List[str]) -> List[str]:
    """
    Helper function to extract education from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: list of education
    """
    edu_keywords = []
    combined_text = ' '.join(nlp_text)
    for word in combined_text.split():
        cleaned_word = re.sub(r'[?|$|.|!|,]', r'', word)
        if cleaned_word.upper() in (kw.upper() for kw in EDUCATION):
            edu_keywords.append(cleaned_word)
    return list(set(edu_keywords))

def extract_experience(resume_text: str) -> List[str]:
    """
    Helper function to extract experience from resume text

    :param resume_text: Plain resume text
    :return: list of experience
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('french'))

    # word tokenization
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize
    filtered_sentence = [w for w in word_tokens if w.lower() not in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)

    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label() == 'P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search for experience keywords
    experience_keywords = ['expérience', 'professionnelle', 'stage', 'stagiaire', 'internship', 'intern', 'experience',
                           'professional experience', 'projet', 'pfe', 'pfa']
    x = [i for i in test if any(word in i.lower() for word in experience_keywords)]

    y = [y[y.lower().index('experience') + 10:] for y in test if 'experience' in y.lower()]

    return x + y

def extract_competencies(text: str, experience_list: List[str]) -> Dict[str, List[str]]:
    """
    Helper function to extract competencies from resume text

    :param text: Plain resume text
    :param experience_list: list of experience items
    :return: dictionary of competencies
    """
    experience_text = ' '.join(experience_list)
    competency_dict = {}

    for competency in cs.COMPETENCIES.keys():
        for item in cs.COMPETENCIES[competency]:
            if string_found(item, experience_text):
                if competency not in competency_dict.keys():
                    competency_dict[competency] = [item]
                else:
                    competency_dict[competency].append(item)
    return competency_dict

def extract_measurable_results(text: str, experience_list: List[str]) -> Dict[str, List[str]]:
    """
    Helper function to extract measurable results from resume text

    :param text: Plain resume text
    :param experience_list: list of experience items
    :return: dictionary of measurable results
    """
    experience_text = ' '.join([text[:len(text) // 2 - 1] for text in experience_list])
    mr_dict = {}

    for mr in cs.MEASURABLE_RESULTS.keys():
        for item in cs.MEASURABLE_RESULTS[mr]:
            if string_found(item, experience_text):
                if mr not in mr_dict.keys():
                    mr_dict[mr] = [item]
                else:
                    mr_dict[mr].append(item)
    return mr_dict

def string_found(string1: str, string2: str) -> bool:
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False