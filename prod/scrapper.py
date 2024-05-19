import requests
from bs4 import BeautifulSoup

def get_header_paragraph(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  print("FULL SOUP",soup)
  header = soup.find('h1').text.strip() if soup.find('h1') else "No H1 found"
  paragraphs = [p.text.strip() for p in soup.find_all('p')]
  return header, paragraphs



def get_all_visible_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    text = []
    for element in soup.find_all():
        if element.name not in ['script', 'style'] and element.text.strip():
            text.append(element.text.strip())
    return ' '.join(text)


def get_text_containing(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    text = []
    for element in soup.find_all(string=lambda text: keyword in text):
        text.append(element.strip())
    return ' '.join(text)

def get_elements_containing_text(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all(string=lambda text: keyword in text if text else False)
    return [element.text.strip() for element in elements]



"""
# Example usage (assuming 'data' is your JSON response)
url = data['items'][0]['link']
header, paragraphs = get_header_paragraph(url)
print(f"Header: {header}")
print(f"Paragraphs: {paragraphs}")

#"""