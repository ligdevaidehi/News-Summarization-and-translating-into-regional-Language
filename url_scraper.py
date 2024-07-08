import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import math
from nltk.tokenize import word_tokenize
from googletrans import Translator
import nltk
nltk.download('punkt')

# Set Streamlit page config
st.set_page_config(
    page_title="News Summarizer",
    page_icon="📰",
    layout="centered",
)

def get_article_body(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

import re
import math
from nltk.tokenize import word_tokenize
nltk.download('punkt')

def get_article_body(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the article text from the webpage
    article_text = ""
    for paragraph in soup.find_all('p'):
        article_text += paragraph.get_text() + " "
    
    return article_text

def clean_text(article_body):
    article = article_body.split(". ")
    sentences = []

    # removing special characters and extra whitespaces
    for sentence in article:
        sentence = re.sub('[^a-zA-Z]', ' ', str(sentence))
        sentence = re.sub('[\s+]', ' ', sentence)
        sentences.append(sentence)
    sentences.pop()
    display = " ".join(sentences)
    # print('Initial Text: ')
    # print(display)
    # print('\n')
    return sentences

def cnt_words(sent):
    cnt = 0
    words = word_tokenize(sent)
    for word in words:
        cnt = cnt + 1
    return cnt

def cnt_in_sent(sentences):
    txt_data = []
    i = 0
    for sent in sentences:
        i = i+1
        cnt = cnt_words(sent)
        temp = {'id' : i, 'word_cnt' : cnt}
        txt_data.append(temp)
    return txt_data

def freq_dict(sentences):
    i=0
    freq_list = []
    for sent in sentences:
        i = i+1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] = freq_dict[word]+1
            else:
                freq_dict[word] = 1
            temp = {'id' : i, 'freq_dict' : freq_dict}
        freq_list.append(temp)
    return freq_list

def calc_TF(text_data, freq_list):
    tf_scores = []
    for item in freq_list:
        ID = item['id']
        for k in item['freq_dict']:
            temp = {
                'id': item['id'],
                'tf_score': item['freq_dict'][k]/text_data[ID-1]['word_cnt'],
                'key': k
                }
            tf_scores.append(temp)
    return tf_scores

def calc_IDF(text_data, freq_list):
    idf_scores =[]
    cnt = 0
    for item in freq_list:
        cnt = cnt + 1
        for k in item['freq_dict']:
            val = sum([k in it['freq_dict'] for it in freq_list])
            temp = {
                'id': cnt,
                'idf_score': math.log(len(text_data)/(val+1)),
                'key': k}
            idf_scores.append(temp)
    return idf_scores

def calc_TFIDF(tf_scores, idf_scores):
    tfidf_scores = []
    for j in idf_scores:
        for i in tf_scores:
            if j['key'] == i['key'] and j['id'] == i['id']:
                temp = {
                    'id': j['id'],
                    'tfidf_score': j['idf_score'] * i['tf_score'],
                    'key': j['key']
                    }
                tfidf_scores.append(temp)
    return tfidf_scores

def sent_scores(tfidf_scores, sentences, text_data):
    sent_data = []
    for txt in text_data:
        score = 0
        for i in range(0, len(tfidf_scores)):
            t_dict = tfidf_scores[i]
            if txt['id'] == t_dict['id']:
                score = score + t_dict['tfidf_score']
        temp = {
            'id': txt['id'],
            'score': score,
            'sentence': sentences[txt['id']-1]}
        sent_data.append(temp)
    return sent_data

def summary(sent_data, threshold_value):
    cnt = 0
    summary = []
    for t_dict in sent_data:
        cnt  = cnt + t_dict['score']
    avg = cnt / len(sent_data)
    for sent in sent_data:
        if sent['score'] >= (avg):
            summary.append(sent['sentence'])
    # Limit the summary to the threshold value
    if threshold_value == "Medium":
        summary = ". ".join(summary[:7]) + "."
    elif threshold_value == "High":
        summary = ". ".join(summary[:10]) + "."
    else:
        summary = ". ".join(summary[:3]) + "."
    return summary


def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='hi').text
    return translated_text

def translate_to_marathi(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='mr').text
    return translated_text

def translate_to_telugu(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='te').text
    return translated_text

def translate_to_tamil(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='ta').text
    return translated_text

def main():
    st.sidebar.title("What's on your mind :face_with_monocle:")
    tabs = ["Full Text", "Summary"]
    page = st.sidebar.radio("Want Full Text or Summary ?", tabs)

    if page == "Full Text":
        st.title("News Summarizer and Translator:newspaper:")
        st.markdown("## Full Text !")
        url = st.text_input("Enter the URL of the news article:")
        if st.button("Get Text"):
            article_body = get_article_body(url)
            st.write(article_body)
    
    if page == "Summary":
        st.title("News Summarizer and Translator:newspaper:")
        st.markdown("## Summary !")
        st.write("Enter the URL of the news article you want to summarize:")
        url = st.text_input("URL:")
        st.write("Select the language you want the summary to be translated to:")
        
        # Define the language options
        languages = {
            "English": "en",
            "Hindi": "hi",
            "Marathi": "mr",
            "Telugu": "te",
            "Tamil": "ta"
        }
        
        lang = st.selectbox("Language", list(languages.keys()))

        # Define the threshold options
        threshold_options = {
            "Low": 3,
            "Medium": 5,
            "High": 7
        }

        threshold = st.radio("Select the length of the summary:", list(threshold_options.keys()))

        if st.button("Summarize"):
            article_body = get_article_body(url)
            sentences = clean_text(article_body)
            text_data = cnt_in_sent(sentences)
            freq_list = freq_dict(sentences)
            tf_scores = calc_TF(text_data, freq_list)
            idf_scores = calc_IDF(text_data, freq_list)
            tfidf_scores = calc_TFIDF(tf_scores, idf_scores)
            sent_data = sent_scores(tfidf_scores, sentences, text_data)
            result = summary(sent_data, threshold)  # Pass the threshold value here

            # Translate the summary to the selected language
            translator = Translator()
            translated_result = translator.translate(result, dest=languages[lang]).text
            
            st.write(f"Summary (Translated to {lang}):")
            st.write(translated_result)

if __name__ == "__main__":
    main()
