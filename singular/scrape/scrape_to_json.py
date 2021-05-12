from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


from datetime import date, datetime
from bs4 import BeautifulSoup

import dateutil.parser
import pandas as pd
import random
import time


opt = Options()
# opt.add_argument('--headless')
# opt.add_argument('--disable_gpu')

driver = webdriver.Chrome('/home/agupta/bin/chromedriver', options=opt)

def process_dates(date_str):
  if 'current' in date_str.lower() or 'present' in date_str.lower():
    return datetime.now()
  
  else:
    try:
      return dateutil.parser.parse(date_str.strip())
    except:
      return None

def scrape(url):
  driver.get(url)
  time.sleep(1.5)

  # Fake human behavior
  height = driver.execute_script('return document.body.scrollHeight')

  position = int(random.random() * height / 8)
  clicked = False
  while position < height:

    if position > height / 2 and not clicked:
      try:
        button = driver.find_element_by_css_selector('button.pv-profile-section__see-more-inline')
        driver.execute_script("arguments[0].click();", button)
      except:
        pass
    
      clicked = True

    driver.execute_script('window.scrollTo({top:' + str(position) + ', left:0, behavior: "smooth"});')
    time.sleep(random.uniform(.33, .5))
    position += int(random.random() * height / 4)
  
  WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'experience-section')))
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  info = {}
  info['url'] = url
  info['name'] = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text.strip()

  info['academic'] = []
  edu = soup.find('section', id='education-section')
  try:
    for i, school in enumerate(reversed(edu.find_all('li'))):
      degree = {}
      degree['order'] = i
      degree[f'name'] = school.find('h3').text.strip()
      try:
        degree[f'type'] = school.find('span', class_='pv-entity__comma-item').text.strip()
      except:
        pass
      info['academic'].append(degree)
  except:
    pass

  info['professional'] = []
  jobs = soup.find('section', id='experience-section')
  for job in reversed(jobs.find_all('section', class_='pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view')):
    work = {}

    promotions = job.find('ul')
    if promotions:
      company = job.find('div', class_='pv-entity__company-summary-info')
      work['company'] = company.find('h3').find_all('span')[-1].text.strip()

      for position in promotions.find_all('li'):
        position_dict = work.copy()
        position_dict['position'] = position.find('h3').find_all('span')[-1].text.strip()

        dates = position.find('h4', class_='pv-entity__date-range').find_all('span')[-1].text.strip()
        start, _, end = dates.partition(' – ')
        position_dict['start'] = process_dates(start)
        position_dict['end'] = process_dates(end)
        
        position_dict['order'] = len(info['professional'])
        info['professional'].append(position_dict)
      
    else:
      work['order'] = len(info['professional'])
      work['position'] = job.find('h3').text.strip()
      work['company'] = job.find('p', class_='pv-entity__secondary-title t-14 t-black t-normal').text.strip()

      dates = job.find('h4').find_all('span')[-1].text.strip()
      start, _, end = dates.partition(' – ')
      work['start'] = process_dates(start)
      work['end'] = process_dates(end)
      info['professional'].append(work)


  return info


if __name__ == '__main__':
  input()
  # urls = [
  #   'https://www.linkedin.com/in/oscarxavierquint',
  #   'https://www.linkedin.com/in/anthony-smith-19bb127',
  #   'https://www.linkedin.com/in/ben-english-46a746183',
  #   'https://www.linkedin.com/in/kyle-costa-b0550641',
  # ]
  # dicts = []
  # for u in urls:
  #   alum = scrape(u)
  #   dicts.append(alum)
  #   print(dicts)
