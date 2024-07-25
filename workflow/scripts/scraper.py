from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from bs4 import SoupStrainer, BeautifulSoup
import threading


main_url = 'https://www.merriam-webster.com/dictionary/'


class Scraper():
    def __init__(self):
        # Create a headless browser
        opts = Options()
        opts.add_argument("-headless") 
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait(1)
        #WebDriverWait(self.browser, 20).until(wait_condition)

    def get_definition(self, word):
        definition = None
        self.browser.get(main_url + word)
        meta_tags = BeautifulSoup(self.browser.page_source, 'html.parser', parse_only=SoupStrainer("meta"))
        if meta_tags:
            description = meta_tags.find(attrs={'name': 'description'})
            if description:
                definition = description['content'].split('.')[0]
        return word, definition
    

THREAD_LOCAL = threading.local()  # thread-local is not shared between threads

def get_thread_local_scraper(thread_local):
    # Create a new WebDriver instance in thread-local if it doesn't exist
    # This is to avoid creating a new WebDriver instance for each URL
    # https://stackoverflow.com/questions/53475578/python-selenium-multiprocessing
    scraper = getattr(thread_local, 'scraper', None)
    if scraper is None:
        scraper = Scraper()
        print('Created Scraper instance')
        setattr(thread_local, 'scraper', scraper)
    return scraper

def scrape(word):
    scraper = get_thread_local_scraper(THREAD_LOCAL)
    return scraper.get_definition(word)

