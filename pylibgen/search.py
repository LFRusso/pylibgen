"""
    Not an API for libgen
"""
import requests
from bs4 import BeautifulSoup


BASE_URLS = ["https://libgen.is/", "http://libgen.li/"]
COL_LABELS = ["ID", "Author", "Title", "Publisher", "Year", "Pages", 
        "Language", "Size", "Extension", "Mirror_1", "Mirror_2", "Mirror_3", "Mirror_4", "Mirror_5", "Edit"]  

def search_book(query, column="book"):
    # Iterating over urls (just in case the main one is not working)
    for site in BASE_URLS:
        url = build_url(site, query, column)
        response = requests.request(method='GET', url=url)
        
        if (response.status_code != 200):
            pass
        raw_html = response.text
        return extract_data(raw_html) 
    return None

def build_url(base, query, column="book"):
    return f"{base}search.php?req={query.replace(' ', '_')}&view=simple&column={column}"

def extract_data(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Selcting 3rd table (that contains the data)
    content_table = soup.find_all("table")[2]
    data = parse_table(content_table)
    return data

def parse_table(table):
    # Selecting all tr's but the 1st (header)
    rows = table.find_all("tr")
    if (len(rows) <= 1):
        return None
    rows = rows[1:]

    data_dict = list()
    for row in rows:
        fields = row.find_all("td")
        cols = [r.text for r in fields[:9]]
        cols += [r.find("a").get("href") for r in fields[9:]]
        data_elem = dict([ [col_label, col] for col_label, col in zip(COL_LABELS, cols) ])
        
        data_dict.append(data_elem)
    return data_dict
