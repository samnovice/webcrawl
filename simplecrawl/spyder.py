from urllib.request import urlopen
from linkfinder import LinkFinder
from util import *


class Spyder:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = ''
    crawled = ''

    def __init__(self, project_name, base_url, domain_name):
        Spyder.project_name = project_name
        Spyder.base_url = base_url
        Spyder.domain_name = domain_name
        Spyder.queue_file = Spyder.project_name + '/queue.txt'
        Spyder.crawled_file = Spyder.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First Spider', Spyder.base_url)

    @staticmethod
    def boot():
        create_directory(Spyder.project_name)
        create_data_file(Spyder.project_name, Spyder.base_url)
        Spyder.queue = filecontent_to_set(Spyder.queue_file)
        Spyder.crawled = filecontent_to_set(Spyder.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spyder.crawled:
            print('Thread name ' + thread_name + ' Started Crawling  ' + page_url)
            print('Queue Length = ' + str(len(Spyder.queue)) + '|  Crawled Length  = ' + str(len(Spyder.crawled)))
            Spyder.add_links_to_queue(Spyder.gather_links(page_url))
            Spyder.queue.remove(page_url)
            Spyder.crawled.add(page_url)
            Spyder.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''

        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spyder.base_url, page_url)
            finder.feed(html_string)

        except Exception as e:
            print(str(e))
            return set()

        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            if (link in Spyder.queue) or (link in Spyder.crawled):
                continue
            if Spyder.domain_name != get_domain_name(link):
                continue
            Spyder.queue.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spyder.queue, Spyder.queue_file)
        set_to_file(Spyder.crawled, Spyder.crawled_file)