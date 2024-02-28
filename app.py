import json
import requests
# from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://laptopfriendly.co/tokyo"
data = []

criterion_list = ["Stable Wi-Fi", "Power sockets", "Quiet", "Coffee", "Food"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    print(url)
    page.goto(url)
    video_links = [ video_link.get_attribute("href") for video_link in page.query_selector_all('a.place') ]
    for video_link in video_links:
        video_url = "https://laptopfriendly.co" + video_link
        print(video_url)
        page.goto(video_url)
        title = page.query_selector("h1").inner_text()
        print(title)
        picture = page.query_selector("#place-photos img").get_attribute('src')
        address_div = page.query_selector("#information > div:nth-child(3) a")
        address = ""
        gmaps_url = address_div.get_attribute('href')
        if address_div:
            address = address_div.inner_text()
        informations = {}
        for info_div in page.query_selector_all("#information>div:first-child .col-10>div"):
            informations[f"{info_div.query_selector('div:first-child').inner_text()}"] = [ hour.inner_text() for hour in info_div.query_selector_all("div")[1:]]
        criterion = [ crit_div.inner_text().split("\n")[0].strip() for crit_div in page.query_selector_all(".criterion:not(.gray-font)")]
        criterion = [ criteria for criteria in criterion if criteria in criterion_list]
        data.append({
            'picture': "https://laptopfriendly.co" + picture,
            'title': title,
            'informations': informations,
            'address': address,
            'criterion': criterion,
            'gmaps_url': gmaps_url
        })
    page.context.close() 
    browser.close()
    json_object = json.dumps(data, indent=4)
    with open('./cafe.json', 'w') as f:
        f.write(json_object)
        

        
# html_doc = requests.get(url).text

# soup = BeautifulSoup(html_doc, 'html.parser')

# places = soup.find_all('a', class_='place')
# data = []
# for place in places:
#     place_url = "https://laptopfriendly.co" + place.attrs['href']
#     print(place_url)
#     html_doc = requests.get(place_url).text
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     title = soup.find("h1").text
#     info_divs = soup.find(id="information").find_all("div")
#     informations = [ info.text for info in info_divs]
#     criterion = []
#     def class_selection(c):
#         return 'criterion' in c and 'gray-font' not in c
#     crit_divs = soup.find(class_=class_selection)
#     for crit_div in crit_divs:
#         criterion.append(crit_div.text)
#     data.append({
#         'title': title,
#         'informations': informations,
#         'criterion': criterion
#     })
    
# json_object = json.dumps(data, indent=4)
# with open('./cafe.json', 'w') as f:
#     f.write(json_object)