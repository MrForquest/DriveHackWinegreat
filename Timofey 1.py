import requests
from bs4 import BeautifulSoup

url = 'https://techcrunch.com/2022/08/24/privado-is-grammarly-for-code-privacy-issues/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')

images = []

images_code = soup.find_all('img', class_="article__featured-image")
for image_code in images_code:
    images.append(image_code)
    print(images)
#print(soup.find_all('<time>', class_="full-date-time"))