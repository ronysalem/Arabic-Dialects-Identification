# imports 
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import string
import argparse
import re

nltk.download('stopwords')
stop_words = set(stopwords.words('arabic'))

arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations


def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def remove_links(text):
    URL_REGEX =r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|(www\.[a-zA-Z0-9\-\._~:/?#\[\]@!$&'()*+,;=%]+)"
    text = re.sub(URL_REGEX, '', text)
    return text

def remove_usernames(text):
  text= re.sub(r'@\w+','',text)
  return text

def remove_english(text):
  text=re.sub(r"[a-zA-Z]+", '', text)
  return text

def remove_numbers(text):
  text=re.sub(r"\d+", '', text)
  return text

def remove_punctuation(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

def remove_diacritics(text):
  arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida

                         """, re.VERBOSE)
  return re.sub(arabic_diacritics, '', text)

def removing_redundant_chars(text):
  text=re.sub(r"(.)\1{2,}", r'\1\1', text)
  return text

def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_special_chars(text):
  # Regex to keep only Arabic letters
  text= re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+', ' ', text)
  return text


def remove_extra_whitespaces(text):
  text= re.sub(r'\s+', ' ', text)
  return text.strip()

def normalize_chars(text):
    preprocessed_text = re.sub("[إأآا]", "ا", text)
    preprocessed_text = re.sub("ى", "ي", preprocessed_text)
    preprocessed_text = re.sub("ؤ", "ء", preprocessed_text)
    preprocessed_text = re.sub("ئ", "ء", preprocessed_text)
    preprocessed_text = re.sub("ة", "ه", preprocessed_text)
    preprocessed_text = re.sub("گ", "ك", preprocessed_text)
    preprocessed_text = re.sub("ڤ", "ف", preprocessed_text)
    preprocessed_text = re.sub("چ", "ج", preprocessed_text)
    preprocessed_text = re.sub("ژ", "ز", preprocessed_text)
    preprocessed_text = re.sub("پ", "ب", preprocessed_text)
    return preprocessed_text

def preprocess(text):
  text = remove_stopwords(text)

  text = remove_usernames(text)

  text = remove_emojis(text)

  text = remove_numbers(text)

  text = remove_links(text)

  text= remove_english(text)

  text=remove_diacritics(text)

  text=remove_special_chars(text)

  text=remove_punctuation(text)

  text = remove_extra_whitespaces(text)

  text=normalize_chars(text)

  text = removing_redundant_chars(text)

  return text


