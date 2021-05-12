<h1 align="center"> 
  WPI Alumni Career Mapper<br/>
  <img src="https://upload.wikimedia.org/wikipedia/en/1/1b/WPI_logo.png" 
    alt="WPI Logo" width=75px/> <br />
</h1>

<p align='center'>
  <i>An interactive dashboard to evaluate alumni's post-WPI experience</i>
  <br/>
  <br/>
  <a href='https://observablehq.com/@agupta/wpi-alumni-dashboard' target='_blank' ><img src="https://i.imgur.com/4I3NwSv.png" alt="screenshot" width=600/></a>
</p>

---

# Execution Directions
The entire stack is built off of Jupyter notebooks with inline comments. Each
notebook corresponds to a different part of the pipeline and can be run
independently.

## Environment Configuration
Only python libraries are required to run this pipeline. To set up a simple
virtual environment, simply open a terminal at the root of the repository and:

1. `python3 -m venv venv-career-mappper`
2. `source venv-career-mappper/bin/activate`
3. `pip install -U pip wheel setuptools` (Need to bootstrap pip)
4. `pip install -r bin/requirements.txt`
5. `pip install jupyter` OR `pip install jupyterlab`
6. `jupyter notebook`

## Required APIs
Two Google APIs are needed to run this pipeline:

### Custom Search Engine
We use Google CSEs as an efficient way to query the internet. We've built and 
used [this CSE](https://cse.google.com/cse?cx=2b3406adf5aac7e25) to only search
LinkedIn. However, this CSE is owned by the owner of this repo and please reach
out to [gr-career-path-iqp@wpi.edu](mailto:gr-career-path-iqp@wpi.edu).

### Site Restricted Search
To query the CSE, you will need an API key for Google's
[Custom Site Restricted Search](https://developers.google.com/custom-search/v1/site_restricted_api)
service. Note that this is a **paid** service from Google. You can learn how 
to set up billing and get an API key [here](https://developers.google.com/custom-search/v1/site_restricted_api).

## A note about data
Since we are considering the data of WPI alumni, we want to respect their privacy
as much as possible. All data sets will need to be requested internally from WPI.
As the scripts are run, they will prompt to you to enter the respective data sets
when needed.