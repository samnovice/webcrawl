import threading
from queue import Queue
from spyder import Spyder
from util import *

PROJECT_NAME = 'static_site'
HOME_PAGE = 'http://myrandomthoughts.in/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spyder(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)


def crawl():
    queued_link = filecontent_to_set(QUEUE_FILE)
    if len(queued_link) > 0:
        print(str(len(queued_link)) + "Links in queue")
        create_jobs()

def create_jobs():
    for link in filecontent_to_set(QUEUE_FILE):
        queue.put(link)
        queue.join()
        crawl()


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Spyder.crawl_page(threading.current_thread().name, url)
        queue.task_done()


create_workers()
crawl()
