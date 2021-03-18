from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import date, datetime
from bs4 import BeautifulSoup

import pandas as pd
import random
import time


opt = Options()
# opt.add_argument('--headless')
# opt.add_argument('--disable_gpu')
driver = webdriver.Chrome('/home/agupta/bin/chromedriver', options=opt)


def scrape(url):
  driver.get('https://linkedin.com')
  time.sleep(random.uniform(0.25, 1))

  driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  info = {}
  info['name'] = soup.find('h1', class_='top-card-layout__title').text.strip()

  info['academic'] = []
  for i, school in enumerate(reversed(soup.find_all('li', class_='education__list-item'))):
    degree = {}
    degree['order'] = i
    degree[f'name'] = school.find('h3', class_='result-card__title').text.strip()
    degree[f'type'] = school.find('span', class_='education__item--degree-info').text.strip()
    
    start, end = school.find_all('time')
    degree[f'start'] = start.text.strip()
    degree[f'end'] = end.text.strip()
    info['academic'].append(degree)

  info['professional'] = []
  for i, job in enumerate(reversed(soup.find_all('li', class_='experience-item'))):
    work = {}
    work['order'] = i
    work['position'] = job.find('h3', class_='result-card__title').text.strip()
    work['company'] = job.find('h4', class_='result-card__subtitle').text.strip()
    
    dates = job.find_all('time')
    start_month, _, start_year = dates[0].text.strip().partition(' ')
    work['start_month'] = start_month
    work['start_year'] = start_year

    if len(dates) == 2:
      end_month, _, end_year = dates[1].text.strip().partition(' ')
      work[f'end_month'] = end_month
      work[f'end_year'] = end_year
    else:
      today = datetime.today()
      work['end_month'] = today.strftime('%b')
      work['end_year'] = today.year
    info['professional'].append(work)

  orgs = soup.find('ul', class_='organizations__list') 
  info['organizations'] = orgs and [o.text.strip() 
                                    for o in orgs.find_all('h3', class_='result-card__title')]

  # for k,v in info.items():
  #   print(f'{k}: {v}')

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
  urls = [
    # LinkedIn URLs go here...
  ]
  dicts = []
  for u in urls:
    try:
      alum = scrape(u)
      dicts.append(alum)
    except:
      pass
