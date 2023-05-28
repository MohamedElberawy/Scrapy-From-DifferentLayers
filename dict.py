import scrapy

import string


class Dict(scrapy.Spider):
    name = 'urban'

    url = 'https://www.urbandictionary.com/popular.php?character='

    def start_requests(self):
        # loop over all the letters in alphabet
        for letter in string.ascii_uppercase:
            next_page = self.url + letter
            yield scrapy.Request(url=next_page, callback=self.parse)

            # comment to crawl ALL letters
            # break

    def parse(self, res):
        # extract data
        links = []

        for item in res.css('ul.mt-3.columns-2').css('li'):
            word = item.css('a::text').get()

            links.append({
                'word': word,
                'link': item.css('a::attr(href)').get()
            })

            # uncomment break statement to crawl only the first word within a page
            break

        # follow links recursively
        for link in links:
            yield res.follow(url=link['link'], meta={
                'word': link['word']
            }, callback=self.parse_link)

    def parse_link(self, res):
        # forward data from the above level
        word = res.meta.get('word')

        # extract full description from link
        full_description = ' '.join(
            res.css('div.md\:p-8').css('div.meaning::text').getall())

        items = {
            'word': word,
            'full_description': full_description
        }
        yield items
