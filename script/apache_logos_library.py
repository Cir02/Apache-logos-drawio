import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pathlib import Path
import json


def web_site(site):
    driver_path = Path(__file__).parent.joinpath("chromedriver.exe")
    service = Service(executable_path=driver_path)
    #local path for bravebrowser
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    option.add_argument("start-maximized")
    browser = webdriver.Chrome(service=service, options=option)
    browser.get(site)
    return browser

def scrapping_logos(browser, tag_name, class_name):
    all_cards = browser.find_elements(By.TAG_NAME, tag_name)
    wrapper = all_cards[4]
    time.sleep(10)
    logos_info = wrapper.find_elements(By.XPATH, f"//{tag_name}[@class='{class_name}']")
    logos_dict = list()
    values = dict()
    for card in logos_info:
        software_name = card.find_element(By.TAG_NAME, "h4").text
        for urls in card.find_elements(By.TAG_NAME, "a"):
            if 'png' in urls.get_property('attributes')[0]['value'] and 'highres' not in urls.get_property('attributes')[0]['value']:
                logo_png_1200_url = urls.get_property('attributes')[0]['baseURI'] + urls.get_property('attributes')[0]['value']
                try:
                    width = urls.text.split(" ")[1].split("(")[-1]
                    heigth = urls.text.split(" ")[-1].split(")")[0]
                except:
                    continue
                values = {'title': software_name, 'data': logo_png_1200_url, "w":width,"h":heigth,"aspect":"fixed"}
                logos_dict.append(values)
    return logos_dict

def main():
    site = "https://apache.org/logos/"
    tag_name = 'div'
    class_name = 'project_rect'
    browser = web_site(site)
    logos_dict = scrapping_logos(browser, tag_name, class_name)
    xml_logos = f"""<mxlibrary>{json.dumps(logos_dict)}</mxlibrary>"""
    with open(Path(__file__).parent.joinpath('../lib/apache_software_foundation_logos.xml'), 'w', encoding='utf-8') as file:
        file.write(xml_logos)
    return


if __name__ == '__main__':
    main()