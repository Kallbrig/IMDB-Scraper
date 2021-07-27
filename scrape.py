import os
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


def write_to_csv(filename, field_names_list, list_of_dict_items,path):

    os.chdir(path)

    with open(filename, "w+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names_list)
        writer.writeheader()
        writer.writerows(list_of_dict_items)

    print("writing to {} is complete".format(filename))


def get_imdb_top(source_url):
    source = requests.get(source_url).text

    soup = BeautifulSoup(source, 'lxml')

    # search = 'https://yts.mx/movies/'

    table = soup.find('tbody')

    # print(table.prettify())
    index = 1
    list_for_csv = []

    for entry in table.findAll('tr'):
        # index_and_title = '{} - {}'.format(str(index).zfill(3), entry.find('td', class_='titleColumn').a.text)

        title = entry.find('td', class_='titleColumn').a.text
        year = entry.find('td', class_='titleColumn').find('span', class_='secondaryInfo').text.strip('()')

        if entry.find('td', class_='ratingColumn imdbRating').strong:
            rating = entry.find('td', class_='ratingColumn imdbRating').strong.text
        else:
            rating = 0.0

        film_dict = {'Title': title, 'Year': year, 'Rating': rating}

        index += 1

        list_for_csv.append(film_dict)

        # file_entry_name = '{} - {} - {} - {}'.format(str(index).zfill(3), title, year, rating)
        # pprint(list_for_csv)
    return list_for_csv


headings = ['Year', 'Title', 'Rating']

top_rated = get_imdb_top('https://www.imdb.com/chart/top/?sort=rk,asc&mode=simple&page=1')
most_popular = get_imdb_top(
    'https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=8X8KDYMAYZV88WJ8SWJ1&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=boxoffice&ref_=chtbo_ql_2')
top_rated_tv = get_imdb_top('https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250')

path = input('Please input the path to store the files.\n')

current_date = '{}'.format(str(datetime.date(datetime.today())).replace('-', ''))

write_to_csv(current_date + '_imdb_top_rated_movies.csv', headings, top_rated, path)
write_to_csv(current_date + '_imdb_most_popular_movies.csv', headings, most_popular, path)
write_to_csv(current_date + '_imdb_top_rated_tv.csv', headings, top_rated_tv, path)
