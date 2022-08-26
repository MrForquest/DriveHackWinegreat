from nltk.tokenize import word_tokenize
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt')
df = pd.read_csv("../static/data_startup.csv")


def tokenize_sentence(sentence: str, remove_stop_words: bool = True):
    tokens = word_tokenize(sentence, language="english")
    tokens = [i for i in tokens if i not in string.punctuation]
    if remove_stop_words:
        tokens = [i for i in tokens if i not in eng_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens


sentence_example = df.iloc[1]["startup"]
tokens = word_tokenize(sentence_example, language="english")
tokens_without_punctuation = [i for i in tokens if i not in string.punctuation]
eng_stop_words = stopwords.words("english")
tokens_without_stop_words_and_punctuation = [i for i in tokens_without_punctuation if i not in eng_stop_words]
snowball = SnowballStemmer(language="english")
stemmed_tokens = [snowball.stem(i) for i in tokens_without_stop_words_and_punctuation]