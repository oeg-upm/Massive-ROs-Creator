# Requirements:

## Python 3 or superior:
Make sure to have a version 3+ python installed in your machine. 
You can install python from: \
https://www.python.org/downloads/ \

## pip installation:
Usually, pip is automatically installed. In case it's not, please install it following the steps in: \
https://pip.pypa.io/en/stable/installation/ \

## Selenium library installation:
In your terminal, type and excute the next command: \
`pip install selenium`  \

## Download the newest version of chromedriver:
You can download the latest version of the Chromedriver from this link: \
https://chromedriver.chromium.org/downloads \

## ROHub library installation
In your terminal, type and excute the next command: \
`pip install rohub` \

# How to use Massive-ROs-Creator?
After fulfilling the requirements' mentioned before, please follow the next steps to excute the program:

1. Download a local version of the project in your machine
2. Modify entery parameters in the script called "SearchEngine.py" to match your search (domain, field....)
3. Fill in the variable PATH with the local absolute path of your ChromeDriver in both SearchEngine.py and WebScraper.py scripts
4. In your terminal navigate to your project folder then type and excute the next command: \
`py SearchEngine.py`
5. A json file called "ToScrape.json" is created in you project folder. This file contains the IDs of the resourses matching the anterior search and their respective titles.
6. In your terminal, supposing that you are still in the project's folder, type and excute the next command: \
`py WebScraper.py`


