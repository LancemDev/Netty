import requests 
from bs4 import BeautifulSoup 

URL = "http://results.knec.ac.ke/Home/CheckResults" 
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://results.knec.ac.ke",
    "Referer": "http://results.knec.ac.ke/",
    "Upgrade-Insecure-Requests": "1"
}
data = {'indexNumber': '12363111028', 'name': 'Ratemo'}  # replace with your actual data

r = requests.post(URL, headers=headers, data=data)

soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())