#!/usr/bin/env python
# coding: utf-8

# # Text Summarization 

# In[ ]:


#fetching data from wikipedia
import bs4 as bs
import urllib.request
import re

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text


# In[ ]:


#The first preprocessing step is to remove references from the article. Wikipedia, references are enclosed in square brackets. The following script removes the square brackets and replaces the resulting multiple spaces by a single space.
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)


# In[ ]:


## Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


# In[ ]:


#We will use thearticle_text object for tokenizing the article to sentence since it contains full stops. 
sentence_list = nltk.sent_tokenize(article_text)


# In[ ]:


#finding weighted frequency
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


# In[ ]:


#we first store all the English stop words from the nltk library into a stopwords variable. Next, we loop through all the sentences and then corresponding words to first check if they are stop words. If not, we proceed to check whether the words exist in word_frequency dictionary i.e. word_frequencies, or not. If the word is encountered for the first time, it is added to the dictionary as a key and its value is set to 1. Otherwise, if the word previously exists in the dictionary, its value is simply updated by 1.


# In[ ]:


#find the weighted frequency, we can simply divide the number of occurances of all the words by the frequency of the most occurring word
maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


# In[ ]:


# Now is the time to calculate the scores for each sentence by adding weighted frequencies of the words that occur in that particular sentence.


# In[ ]:


sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


# In[ ]:


#We do not want very long sentences in the summary, therefore, we calculate the score for only sentences with less than 30 words


# In[ ]:


#To summarize the article, we can take top N sentences with the highest scores. 
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)

