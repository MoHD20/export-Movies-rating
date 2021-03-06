#!/usr/bin/env python3
import os
import csv
import re
from imdbpie import Imdb
import argparse

"""
export-Movies-rating.py
Mohamed Hamza
Exports IMDB's information for your movies to CSV file.
"""
__version__ = '1'

# def list_movies():
#     '''
#     identifies movies in the current directory
#     movies' names should be in a specific form which is 'name of the movie (year)'
#     for the script to work.
#     you can use "filebot" to do that.
#     https://www.filebot.net/forums/viewtopic.php?f=4&t=215

#     or you can make your own Regex
#     '''

#     u=[]

#     Regex = re.compile(r'(.+) \(\d+\)')
#     print()
#     for x in os.listdir(os.path.dirname(os.path.abspath(__file__))):
#         if Regex.search(x):
#             z = Regex.search(x).group(1)
#             print('this is z  ', z)
#             u.append(z)
#     # print(u)
#     return u


def name_grabber(medialst):
    """Gets the Movie Name and Year from the filename and other meta
    data is removed.
    For Example:
    - Doctor.Strange.2016.720p.BrRip.mkv [INPUT]
    - Doctor Strange 2016 [RETURN]
    This function is made mostly from: https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber
    """

    nameslist = {}
    for movies in medialst:
        yearRegex = re.compile(r'\d{4}')
        if yearRegex.search(movies):
            def get_year(filename):
                    searchitems = yearRegex.search(filename)
                    return searchitems.group()

            year = get_year(movies)
            # This is 2016 Movie --> This is | 2016 | Movie
            name, year, removal = movies.partition(year)
            
            if name[-1] == ' ':
                nameslist.setdefault(year, []).append(name.lower())

            else:
                nameslist.setdefault(year, []).append(name.lower()[:-1])

    nameslist = {key: [movie.strip(' ') for movie in val] for key, val in nameslist.items()}
    print('Found these movies', nameslist)
    return nameslist


def identify_movies (movies):
    """ identifying the movies from IMDB """
    imdb = Imdb()

    ids = []
    for key, vals in movies.items():
        for val in vals:
            for info in imdb.search_for_title(val):
                if key == info.get('year') and val == info.get('title').lower():
                    ids.append(info.get('imdb_id'))

    return [imdb.get_title_by_id(id) for id in ids]


def csv_rows(imdbobjs):
    """ get CSV's rows """
    csv_rows = []
    for i in imdbobjs:
        temp = [getattr(i, z) for z in ['title', 'year', 'rating', 'certification', 'runtime', 'genres', 'plot_outline']]
        # convert time form Seconds to H:M
        temp[4] = _timehm(temp[4])
        csv_rows.append(temp)

    write_csv(csv_rows)

def _timehm(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{}h:{:0=2d}min".format(h, m)

def write_csv(csv_rows):
    """write csv using csv module."""

    # csv setting
    csv_fields = ['Title', 'Year', 'imdbRating', 'Rated', 'Runtime', 'Genre', 'Plot']
    delimiter = ','

    # write csv using csv module
    with open(os.path.join(os.path.abspath(path), 'movies.csv'), "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='export Movies-rating to CSV')

    parser.add_argument('d', metavar='DirPath', nargs='*', default=os.getcwd(),
                        help="your movies Directory's PATH")

    parser.add_argument(
        '--version',
        action='version', version=__version__,
        help='Print program version and exit')

    args = parser.parse_args()

    if isinstance(args.d, list):
        path = args.d[0]
    else:
        path = args.d

    movies_names = name_grabber(os.listdir(os.path.abspath(path)))
    identifies = identify_movies(movies_names)
    csv_rows(identifies)


