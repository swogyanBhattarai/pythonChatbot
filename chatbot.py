import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
from keras._tf_keras.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from datetime import *
from project import train_chatbot
from searcher import *

previous_input = ''
previous_response = ''

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words (sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class (sentence):
    bow = bag_of_words (sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes [r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json, message, last_message = None):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    
    if tag == 'refresh':
        with open('intents.json', 'w') as file:
            json.dump(intents, file, indent=4)
        train_chatbot(50, 0) 
        return "Chatbot has been refreshed and trained."
    
    if tag == 'datetime':
        return datetime.now()
    
    if tag == 'google':
        
        if message.startswith("google:"):
            message = message[len("google:"):].strip() 
            return get_result_google(message)
        
        elif message.startswith("search:"):
            message = message[len("search:"):].strip()
            return get_result_google(message)
        
        elif message.startswith("wikipedia:"):
            message = message[len("wikipedia:"):].strip()
            return get_result_wikipedia(message)
        
        elif message.startswith("wiki:"):
            message = message[len("wiki:"):].strip()
            return get_result_wikipedia(message)
        
        elif message.startswith("wikihow:"):
            message = message[len("wikihow:"):].strip()
            return get_result_wikihow(message)
        
        elif message.startswith("how:"):
            message = message[len("how:"):].strip()
            return get_result_wikihow(message)
        
    # if tag == 'save':
    #     with open('intents.json', 'r') as file:
    #         intents = json.load(file)
            
    #     new_intent = {
    #         "tag": message,
    #         "patterns": [message],
    #         "responses": [res]
    #     }
        
    #     intents_json['intents'].append(new_intent)       
    #     with open('intents.json', 'w') as file:
    #         json.dump(intents, file, indent=4)

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice (i['responses'])
            previous_input = message
            # previious_response = result
            break
    return result

def update_intents_file(intents_list, sentence):
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            if sentence not in i['patterns']:
                i['patterns'].append(sentence)
                print("Sentence appended in corresponding tag's pattern")
            break
    
    with open('intents.json', 'w') as file:
        json.dump(intents, file, indent=4)

print("\n\nBot is running!\n\n")

def output(message):
    ints = predict_class(message)
    if float(ints[0]['probability']) < 0.6:
        print("\nI'm sorry, I'm not sure how to respond to that.\n\n")
        return
    res = get_response(ints, intents, message)
    update_intents_file(ints, message)
    return res
    
# while True:
#     print("Enter your message:\n")
#     message = input("")
#     # train_chatbot(50, 0)
#     print("\n\n")
#     ints = predict_class(message)
#     if float(ints[0]['probability']) < 0.6:
#         print("\nI'm sorry, I'm not sure how to respond to that.\n\n")
#         continue
#     res = get_response(ints, intents, message)
#     print (res)
#     print ('\n\n')
#     update_intents_file(ints, message)

if __name__ == '__main__':
    clean_up_sentence()
    update_intents_file()
    get_response()
    predict_class()
    bag_of_words()
    