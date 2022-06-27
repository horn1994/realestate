from bs4 import BeautifulSoup
from requests import get

def PorpertyDetails(source_url, headers):

    url = source_url
    response = get(url, headers=headers)
    html_soup = BeautifulSoup(response.text,
                              'html.parser')

    spec_param_names = [
        html_soup.find_all(
            'tr',
            class_ = "text-onyx")[i]
        .find_all("td", class_=None)[0]
        .text
        .replace('\n', '')
        .strip() 
        for i in range(
            len(
                html_soup
                .find_all(
                    'tr',
                    class_ = "text-onyx")))]
    
    spec_param_values = [
        html_soup.find_all(
            'tr',
            class_ = "text-onyx")[i]
        .find_all("td", class_="fw-bold")[0]
        .text
        .replace('\n', '')
        .strip() 
        for i in range(
            len(
                html_soup
                .find_all(
                    'tr',
                    class_ = "text-onyx")))]

    details = {name:value for name,value in zip(spec_param_names, spec_param_values)}

    try:
        details["Leírás"] = html_soup.find_all('div', class_ = "lh-base px-0")[0].text.replace('\n', '').strip()
        
    except IndexError:
        details["Leírás"] = "nincs megadva"

    imgs = html_soup.find_all("meta", property="og:image")
    img_links = ''
    
    if len(imgs) > 0:
        for img in imgs:
            img_links += str(img["content"]) + ","
            details["Képek"] = img_links

    else:
        details["Képek"] = 'nincs megadva'

    return details