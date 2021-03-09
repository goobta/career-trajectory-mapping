from concurrent import futures

import pandas as pd
import random
import os


DEGREES = ['CS', 'MA', 'PSY', 'WR', 'ME', 'IE', 'RBE', 'ECE']
PROBS = {
  'masters': (0.5, 2),
  'phd': (0.1, 4),
}

GRAD_YEARS = (1990, 2021)
SALARY_RANGE = (50000, 1e6)

JOB_TITLE = ['Accountant', 'SWE1', 'SWE2', 'SWE3', 'Salesmen']
JOB_DUR_BOUNDS = (1, 10)
COMPANY = ['Pfizer', 'Moderna', 'Raytheon', 'Google', 'Amazon', 'Facebook', 
           'Amazon', 'WPI'] 
LOCATIONS = ['MA', 'CA', 'CT', 'NY', 'MD', 'RI', 'NJ']
SECTORS = ['Big Tech', 'BioTech', 'Automotives', 'Finance', 'Research']

_MAX_JOBS = 4


def generate_person_dict(_):
  person = {}
  person['major'] = random.choice(DEGREES)
  person['major_2'] = random.choice(DEGREES) if random.random() < .5 else None
  person['grad_year'] = random.randint(*GRAD_YEARS)

  last_year = person['grad_year']
  for degree, (prob, length) in PROBS.items():
    person[degree] = random.choice(DEGREES) if random.random() < prob else None
    person[f'{degree}_location'] = random.choice(LOCATIONS)
    person[f'{degree}_start'] = last_year

    last_year += int(length)
    person[f'{degree}_end'] = last_year

  job_cnt = random.randint(1, _MAX_JOBS)
  last_job = last_year
  for i in range(job_cnt):
    job_id = 'job{}'.format(i + 1)
    job_end = last_job + random.randint(*JOB_DUR_BOUNDS)

    person[job_id] = random.choice(JOB_TITLE)
    person['{}_start'.format(job_id)] = last_job
    person['{}_end'.format(job_id)] = job_end
    person['{}_sector'.format(job_id)] = random.choice(SECTORS)
    person['{}_location'.format(job_id)] = random.choice(LOCATIONS)

    last_job = job_end

  return person
  

def create_dataset(count):
  print('Generating data...')
  with futures.ProcessPoolExecutor(max_workers=os.cpu_count() or 2) as exec:
    data = exec.map(generate_person_dict, range(count), chunksize=100)

  return pd.DataFrame((list(data)))
  

if __name__ == '__main__':
  count = int(input('How many people do you want to generate?: '))

  filename = 'fake-trajectories-{}.csv'.format(count)
  df = create_dataset(count)  
  df.to_csv(filename, index_label='id')

  print('Done. Written to {}'.format(filename))
