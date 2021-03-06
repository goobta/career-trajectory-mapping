from datetime import date, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import time


driver = webdriver.Chrome('/home/agupta/bin/chromedriver')


def scrape(url):
  driver.get('https://linkedin.com')
  time.sleep(0.75)

  driver.get(url)
  time.sleep(0.5)
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

  for k,v in info.items():
    print(f'{k}: {v}')