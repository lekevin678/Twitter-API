import json
import re
import operator 
from collections import Counter
import string
import random
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase == False:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
# creates list of dictionaries for each tweet
with open('tweets.json', 'r') as f:
    for line in f:
        d = json.loads(line)


# creates words, numbers, punctuations to remove from most common terms
stopList = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', "with", 'they', 'own', 'an', 'be', 'some', "for", 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', "is", 's', 'am', "or", 'who', "as", "from", 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', "while", 'above', 'both', 'up', 'to', 'ours', 'had', 'she', "all", 'no', 'when', 'at', "any", 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', "not", 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', "if", 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
punctuation = list(string.punctuation)
numbers = ["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10"]
etc = ['’' , '…' , 'amp', 'like' , "re-tweeted" , "#win" , "@"]
stop = stopList + punctuation + numbers + etc +['rt', 'via']


fname = 'tweets.json'

# most common terms
with open(fname, 'r') as f:
    count_all = Counter()
    for i in d:
        terms_stop = [term for term in preprocess(i['text']) if term not in stop and term[0] != '@' and "https" not in term]
        count_all.update(terms_stop)
    print(count_all.most_common(10))





# number of unique users
userdict = {}
real_total = 0
total = 0
with open(fname, 'r') as f:
    for i in d:
        user = i['user']["screen_name"]
        total += 1
        if not user in userdict:
            userdict[user] = 1
            real_total += 1
        else:
            userdict[user] += 1
    print(total)
    print(real_total)





# get 10 random tweets
i = 1;
for x in range(0,10):
    rand = random.choice(d)
    print( i , rand['text'], '\n\n')
    i += 1





# create word cloud txt file with words that have more than 50 occurances
output = open('wordcloud.txt', 'w') 
for i in count_all:
    if count_all[i] > 50:
        print(count_all[i] , " " , i, file = output)





# get 50 different tweets
i = 1;
for x in range(0,50):
    rand = random.choice(d)
    print( i , rand['text'], '\n\n')
    i += 1

