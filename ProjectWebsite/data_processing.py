import numpy as np
import pandas as pd
import urllib.parse
from urllib.parse import urlparse
import math
import tldextract, re
from collections import Counter
import sklearn, joblib
from alexa_parsing import whitelist



def convertToDf(url):
    # Convert Url into Dataframe With Features
    data = [url]
    df = pd.DataFrame(data, columns=['url'])
    return df

def symbolCounts(df, features):
    symbols = ['@', '?', '-', '=', '.', '#',
               '%', '+', '$', '!', '*', ',', '/', '//']
    
    for s in symbols:
        features[s] = df['url'].apply(lambda i: i.count(s))


def path_length(url):
    urlpath = urlparse(url).path  # returns '/path'
    try:
        return len(urlpath)  # return only characters after 1st '/'
    except:
        return 0


def fd_length(url):
    urlpath = urlparse(url).path  # returns '/path'
    try:
        # return only characters between first and second '/'
        return len(urlpath.split('/')[1])
    except:
        return 0


def calculate_entropy(s):
    # Counter() returns a dictionary of character counts
    p, lns = Counter(s), float(len(s))
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())
    # high entropy for more complex names


def http(url):
    scheme = urlparse(url).scheme
    match = str(scheme)
    if match == 'http':
        return 1
    else:
        return 0


def https(url):
    scheme = urlparse(url).scheme
    match = str(scheme)
    if match == 'https':
        return 1
    else:
        return 0


def sus_words(url):
    match = re.search('password|login|signin|bank|account|update|free|lucky|service|bonus|official|verify|confirm|secure|pay|reset',
                      url)
    if match:
        return 1
    else:
        return 0


def preProcess(url):
    df = convertToDf(url)
    df['url'] = df['url'].replace('www.', '', regex=True)
    

    features = pd.DataFrame()  
    features['url_length'] = df['url'].apply(len)

    features['letter_count'] = df['url'].str.count(r'[a-zA-Z]')
    features['digit_count'] = df['url'].str.count(r'\d')



    symbolCounts(df, features)

    features['path_length'] = df['url'].apply(lambda i: path_length(i))
    features['fd_length'] = df['url'].apply(lambda i: fd_length(i))

    # extract hostname and length of hostname (e.g., only 'www.domain.com')
    features['hostname'] = df['url'].apply(lambda x: urlparse(x).netloc)
    features['hostname_length'] = features['hostname'].apply(len)

    features['hostname_entropy'] = features['hostname'].apply(
        calculate_entropy)
    
    features['domain'] = df['url'].apply(
        lambda x: tldextract.extract(x).domain)

    features['domain_length'] = features['domain'].apply(len)

    features['domain_entropy'] = features['domain'].apply(calculate_entropy)

    # extract tld and length of tld
    features['tld'] = df['url'].apply(lambda x: tldextract.extract(x).suffix)
    # print(features[features['tld'] != ''])
    features['tld_length'] = features['tld'].apply(len)

    features['http'] = df['url'].apply(lambda x: http(x))
    features['https'] = df['url'].apply(lambda x: https(x))
    features['sus_words'] = df['url'].apply(lambda x: sus_words(x))

    return features

def runModel(url):
    
    features = preProcess(url)
    
    hostname = features["hostname"].iloc[0]
    
    print(hostname)

    if hostname in whitelist:
        return "benign"
    
    
    features = features.drop(columns=['domain', 'tld', 'hostname'])
    dt_classifier = joblib.load("models/model.joblib")
    prediction = dt_classifier.predict(features)
    
    return prediction[0]

