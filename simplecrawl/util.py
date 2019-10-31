import os
from urllib.parse import urlparse


def create_directory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def create_data_file(dirname, baseurl):
    queue = os.path.join(dirname, 'queue.txt')
    crawled = os.path.join(dirname, 'crawled.txt')

    if not os.path.isfile(queue):
        create_file(queue, baseurl)

    if not os.path.isfile(crawled):
        create_file(crawled, '')


def create_file(file_path, data):
    with open(file_path, 'w') as fobj:
        fobj.write(data)


def append_to_file(file_path, data):
    with open(file_path, 'a') as fobj:
        fobj.write(data + '\n')


def delete_file_content(file_path):
    open(file_path, 'w').close()


def filecontent_to_set(file_path):
    links = set()
    with open(file_path, 'rt') as fp:
        for line in fp:
            links.add(line.replace('\n', ''))
    return links


def set_to_file(links, file_path):
    with open(file_path, 'w') as fp:
        for link in sorted(links):
            fp.write(link + '\n')


def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


