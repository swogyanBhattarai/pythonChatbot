from googlesearch import search
from bs4 import *
import requests
import nltk

def query_wikipedia(query):
    query_pedia = f"{query} site:wikipedia.org"
    result = search(query_pedia, num_results=1)
    result_list = list(result)
    if result:
        top_result = result_list[0]
        return top_result
    else:
        return None
    
def query_wikihow(query):
    query_how = f"{query} site:wikihow.com"
    result = search(query_how, num_results=1)
    result_list = list(result)
    if result:
        top_result = result_list[0]
        return top_result
    else:
        return None

def query_google(query):
    result = search(query, num_results=1)
    result_list = list(result)
    if result:
        top_result = result_list[0]
        return top_result
    else:
        return None
    
def scrape(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs[1:2]])
        sentenses = nltk.sent_tokenize(content)
        formatted_content = '\n\n'.join(sentenses)
        return formatted_content
    else:
        return 'No content found'
    
def get_result_google(user_query):
    print('\n')
    top_result = query_google(user_query)
    if top_result:
        content = scrape(top_result) + f"\n\nTo learn more, visit: <a href='{top_result}'>{top_result}</a>"
        return content
    else:
        return "No Content found"
    
def get_result_wikipedia(user_query):
    print('\n')
    top_result = query_wikipedia(user_query)
    if top_result:
        content = scrape(top_result) + f"\n\nTo learn more, visit: <a href='{top_result}'>{top_result}</a>"
        return content
    else:
        return "No content found"
    
def get_result_wikihow(user_query):
    print('\n')
    top_result = query_wikihow(user_query)
    if top_result:
        content = scrape(top_result) + f"\n\nTo learn more, visit: <a href='{top_result}'>{top_result}</a>"
        return content
    else:
        return "No content found"


if __name__ == "__main__":
    get_result_google()
    get_result_wikipedia()
    get_result_wikihow()