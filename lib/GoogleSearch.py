# This file will be dedicated for GoogleSearch. They will return list of string of name and link
# from Google Search

from google import google
from itertools import islice


class GoogleSearch():
    def __init__(self, search_key=None, num_search=0):
        self.search_key=search_key
        self.number_search=num_search

    def search(self):
        data = google.search(self.search_key)
        selected_data = []
        for result in data:
            result = {result.name: result.link}
            selected_data.append(result)
        return list(islice(selected_data,self.number_search))


if __name__ == '__main__':
    query = GoogleSearch('cat',3)
    g_result = query.search()
    print (g_result)