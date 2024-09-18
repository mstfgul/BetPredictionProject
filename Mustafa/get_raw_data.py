from bs4 import BeautifulSoup
import requests


url = 'https://www.football-data.co.uk/belgiumm.php'
string_to_find = 'Jupiler League'

def get_links(url, string_to_find):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_of_links = []
    for link in soup.find_all('a'):
        if string_to_find in link.text:
            list_of_links.append (link.get('href'))
    return list_of_links



def get_csv_files(list_of_links):
    base_url = 'https://www.football-data.co.uk/'
    for link in list_of_links:
        response = requests.get(base_url + link)
        with open('/Users/mustafagul/Desktop/fixture_project/data/allcsv/'+ link.split('/')[1]+('.csv'), 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    list_of_links = get_links(url, string_to_find)
    get_csv_files(list_of_links[:24])