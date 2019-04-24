import os
import random
import time

import requests
from bs4 import BeautifulSoup


class Crawling():
    def __init__(self, n):
        self.set_link_list = []
        self.n = n

    # basic crawling function
    def crawling(self, link):
        self.link = link
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            r = requests.get(self.link, headers=headers, timeout=20)
            html = r.text
            html_content = r.content
            html_data = BeautifulSoup(html, 'lxml')
            return html_content, html_data
        except Exception as e:
            print('该地址下载失败: ', self.link)
            print(e)

    # crawling first n pages
    def get_sets(self):
        for i in range(1, self.n):
            main_site_link = 'https://wear.jp/coordinate/?pageno=' + str(i)
            main_site_data = self.crawling(main_site_link)[1]

            # get individual links from shopping guides
            set_divs = main_site_data.find_all(name="div", attrs={"class": "image"})
            for set_div in set_divs:
                set_link_text = set_div.find_all(name="a")
                set_links = [l['href'] for l in set_link_text]
                for set_link1 in set_links:
                    set_link = "https://wear.jp" + set_link1
                    self.set_link_list.append(set_link)

            # sleep
            sleep_time = random.randint(0, 1) + random.random()
            time.sleep(sleep_time)

    # get pics from set_link_list and return image link
    def get_pic(self, link):
        self.link = link
        img_set = []
        set_data = self.crawling(self.link)[1]
        section = set_data.find(name="section", attrs={"id": "item", "class": "content_bg"})
        img = section.find_all(name="img")
        for i in img:
            img_address = 'http:' + i['src']
            img_set.append(img_address)
        return img_set

    def save_pic(self, link):
        self.link = link
        for each in self.link:
            filename = each.split('/')[-1]
            img = self.crawling(each)[0]
            with open(filename, 'wb')as f:
                f.write(img)

    # save pics in to folders
    def download_pic(self, link, page_num):
        self.link = link
        self.page_num = page_num
        folder = str(self.page_num)
        os.mkdir(folder)
        os.chdir(folder)

        self.save_pic(self.link)
        os.chdir('..')


if __name__ == "__main__":
    time1 = time.time()
    data = Crawling(3)
    time2 = time.time()
    total_time = time2 - time1
    print(total_time)
    set_num = 0
    for add in data.set_link_list:
        set_num += 1
        i = data.get_pic(add)
        data.download_pic(i, set_num)
