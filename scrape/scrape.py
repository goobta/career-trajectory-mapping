from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import date, datetime
from bs4 import BeautifulSoup

import pandas as pd
import random
import time


opt = Options()
opt.add_argument('--headless')
opt.add_argument('--disable_gpu')
driver = webdriver.Chrome('/bin/chromedriver', options=opt)


def scrape(url):
  driver.get('https://linkedin.com')
  time.sleep(random.uniform(0.25, 1))

  driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  info = {}
  info['name'] = soup.find('h1', class_='top-card-layout__title').text.strip()

  for i, school in enumerate(soup.find_all('li', class_='education__list-item')):
    info[f'School {i} Name'] = school.find('h3', class_='result-card__title').text.strip()
    info[f'School {i} Degree'] = school.find('span', class_='education__item--degree-info').text.strip()
    
    start, end = school.find_all('time')
    info[f'School {i} Start'] = start.text.strip()
    info[f'School {i} End'] = end.text.strip()

  for i, job in enumerate(reversed(soup.find_all('li', class_='experience-item'))):
    info[f'Job {i} Position'] = job.find('h3', class_='result-card__title').text.strip()
    info[f'Job {i} Company'] = job.find('h4', class_='result-card__subtitle').text.strip()
    
    dates = job.find_all('time')
    start_month, _, start_year = dates[0].text.strip().partition(' ')
    info[f'Job {i} Start Month'] = start_month
    info[f'Job {i} Start Year'] = start_year

    if len(dates) == 2:
      end_month, _, end_year = dates[1].text.strip().partition(' ')
      info[f'Job {i} End Month'] = end_month
      info[f'Job {i} End Year'] = end_year
    else:
      today = datetime.today()
      info[f'Job {i} End Month'] = today.strftime('%b')
      info[f'Job {i} End Year'] = today.year

  orgs = soup.find('ul', class_='organizations__list') 
  info['organizations'] = orgs and [o.text.strip() 
                                    for o in orgs.find_all('h3', class_='result-card__title')]

  for k,v in info.items():
    print(f'{k}: {v}')

  # Fake human behavior
  time.sleep(random.uniform(.75, 2))
  height = driver.execute_script('return document.body.scrollHeight')

  position = int(random.random() * height / 8)
  while position < height:
    driver.execute_script('window.scrollTo({top:' + str(position) + ', left:0, behavior: "smooth"});')
    time.sleep(random.uniform(.33, 1.5))
    position += int(random.random() * height / 4)

  return info


if __name__ == '__main__':
  urls = []
  dicts = []
  for u in urls:
    try:
      alum = scrape(u)
      dicts.append(alum)
    except:
      pass