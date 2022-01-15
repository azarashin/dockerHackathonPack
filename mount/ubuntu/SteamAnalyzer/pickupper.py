
# coding: utf-8

import codecs
import sys
import re
import datetime
import os

class DiscountPriceInfo:
    def __init__(self, price, discounted_price):
        self.price = float(price.replace(',', ''))
        self.discounted_price = float(discounted_price.replace(',', ''))

    def __str__(self):
        return 'discount price: {}, discounted_price: {}'.format(self.price, self.discounted_price)

class PriceInfo:
    def __init__(self, country, price):
        self.country = country
        self.price = float(price.replace(',', ''))

    def __str__(self):
        return 'country: {}, price: {}'.format(self.country, self.price)

class ReviewInfo:
    def __init__(self, title, reviewCount, ratingValue, maxRating, minRating):
        self.title = title
        self.reviewCount = int(reviewCount)
        self.ratingValue = int(ratingValue)
        self.maxRating = int(maxRating)
        self.minRating = int(minRating)

    def __str__(self):
        return 'title: {}, reviewCount: {}, ratingValue: {}, maxRating: {}, minRating: {}'.format(self.title, self.reviewCount, self.ratingValue, self.maxRating, self.minRating)

class LanguageInfo:
    def __init__(self, title, interface, full_audio, subtitles):
        self.title = title
        self.interface = interface
        self.full_audio = full_audio
        self.subtitles = subtitles

    def __str__(self):
        return 'language: {}, interface: {}, full_audio: {}, subtitles: {}'.format(self.title, self.interface, self.full_audio, self.subtitles)

class ProductInfo:
    def __init__(self, id, path):
        if not os.path.exists(path):
            self.status = 'nothing'
            return
        body = codecs.open(path, 'r', 'utf-8').read()
        self.id = id

        if '[[error]]' in body:
            self.status = 'error'
            return
        elif '[[invalid]]' in body:
            self.status = 'invalid'
            return
        elif 'is no longer available for sale on Steam.' in body:
            self.status = 'closed'
        else:
            self.status = 'active'

        self.init_title(body)
        self.init_price(body)
        self.init_genre(body)
        self.init_review(body)
        self.init_releaseDate(body)
        self.init_publisher(body)
        self.init_tag(body)
        self.init_language(body)

    def init_language(self, body):
        p_language = re.compile(r'<td.*?class="ellipsis".*?>(.+?)</td>.*?<td class="checkcol">(.+?)</td>.*?<td class="checkcol">(.+?)</td>.*?<td class="checkcol">(.+?)</td>', flags=re.DOTALL)
        langs = p_language.findall(body)
        self.languages =[LanguageInfo(d[0].strip(), (d[1].strip() != ''), (d[2].strip() != ''), (d[3].strip() != '')) for d in langs]

    def init_tag(self, body):
        p_tag = re.compile(r'<a.*?class="app_tag".*?>(.+?)</a>', flags=re.DOTALL)
        m = p_tag.findall(body)
        self.tags = [d.strip() for d in m]

    def init_title(self, body):
        p_title = re.compile(r'<title>(.+?)</title>', flags=re.DOTALL)
        m = p_title.search(body)
        if m is None:
            self.title = None
        else:
            self.title = m.group(1)

    def init_publisher(self, body):
        p_developer = re.compile(r'<b>Developer:</b>.*?<a.*?>(.+?)</a>', flags=re.DOTALL)
        p_publisher = re.compile(r'<b>Publisher:</b>.*?<a.*?>(.+?)</a>', flags=re.DOTALL)
        m = p_developer.search(body)
        if m is None:
            self.developer = None
        else:
            self.developer = m.group(1)
        m = p_publisher.search(body)
        if m is None:
            self.publisher = None
        else:
            self.publisher = m.group(1)


    def init_releaseDate(self, body):
        mp = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12 
            , 'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8
            , 'September':9, 'October':10, 'November':11, 'December':12
            , 'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12 
            , 'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8
            , 'september':9, 'october':10, 'november':11, 'december':12
             }
        p_release = re.compile(r'<b>Release Date:</b> ([0-9]+?) ([^0-9]+?), ([0-9]+?)<br>', flags=re.DOTALL)
        m = p_release.search(body)
        if m:
            self.releaseDate = datetime.datetime(int(m.group(3)), mp[m.group(2)], int(m.group(1)))
            return

        p_release = re.compile(r'<b>Release Date:</b> ([^0-9]+?) ([0-9]+?), ([0-9]+?)<br>', flags=re.DOTALL)
        m = p_release.search(body)
        if m:
            self.releaseDate = datetime.datetime(int(m.group(3)), mp[m.group(1)], int(m.group(2)))
            return

        p_release = re.compile(r'<b>Release Date:</b>([0-9]+?), ([0-9]+?)<br>', flags=re.DOTALL)
        m = p_release.search(body)
        if m:
            self.releaseDate = datetime.datetime(int(m.group(2)), mp[m.group(1)], 1)
            return

        p_release = re.compile(r'<b>Release Date:</b> *Q([0-9])[^<>]+?, ([0-9]+?)<br>', flags=re.DOTALL)
        m = p_release.search(body)
        if m:
            # クオーター
            self.releaseDate = datetime.datetime(int(m.group(2)), int(m.group(1)) * 3 - 2, 1)
            return
        self.releaseDate = None

    def init_review(self, body):
        p_review_title = re.compile(r'<span class="game_review_summary.*?>(.*?)</span>', flags=re.DOTALL)
        p_review = re.compile(r'<meta itemprop="reviewCount" content="(.*?)">.*?<meta itemprop="ratingValue" content="(.*?)">.*?<meta itemprop="bestRating" content="(.*?)">.*?<meta itemprop="worstRating" content="(.*?)">', flags=re.DOTALL)

        m = p_review.search(body)
        if m is None:
            self.review = None
        else:
            m2 = p_review_title.search(body)
            if m2:
                title = m2.group(1)
            else:
                title = '-'
            reviewCount = m.group(1)
            ratingValue = m.group(2)
            maxRating = m.group(3)
            minRating = m.group(4)
            self.review = ReviewInfo(title, reviewCount, ratingValue, maxRating, minRating)

    def init_genre(self, body):
        p_genres = re.compile(r'<b>Genre:</b>.*?<br>')
        p_genre = re.compile(r'<a href=".*">(.*?)</a>')

        m = p_genres.search(body)
        if m is None:
            self.genres = None
        else:
            genres_body = m.group()
            self.genres = p_genre.findall(genres_body.replace(',', '\n'))


    def init_price(self, body):
        p_discount_price = re.compile(r'<div class="discount_original_price">¥ ([0-9,]*)</div><div class="discount_final_price">¥ ([0-9,]*)</div>', flags=re.DOTALL)
        p_prices = re.compile(r'<div class="game_purchase_price price" data-price-final="([0-9]+)">', flags=re.DOTALL)
        p_price = re.compile(r'<meta itemprop="priceCurrency" content="(.*?)">.*<meta itemprop="price" content="(.*?)">', flags=re.DOTALL)

        all_discount_prices = p_discount_price.findall(body)
        all_prices = p_prices.findall(body)
        price = p_price.search(body)
        self.discount_prices = [DiscountPriceInfo(d[0], d[1]) for d in all_discount_prices]
        self.prices = [float(d) / 100 for d in all_prices]
        if price:
            self.price = PriceInfo(price.group(1), price.group(2))
        else:
            self.price = None

    def __str__(self):
        ret = 'id: {}\n'.format(self.id)
        ret += 'status: {}\n'.format(self.status)
        if self.status != 'active' and self.status != 'closed':
            return ret

        ret += 'title: {}\n'.format(self.title)
        ret += 'tags: {}\n'.format(self.tags)
        ret += 'price: {}\n'.format(self.price)
        ret += 'prices: \n' + '\n'.join(['\t' + str(d) for d in self.prices])
        ret += '\n\nlanguages: \n' + '\n'.join(['\t' + str(d) for d in self.languages])
        ret += '\n\ndiscount prices: \n' + '\n'.join(['\t' + str(d) for d in self.discount_prices])
        ret += '\n\ngenres: ' + str(self.genres)
        ret += '\n\nreview: ' + str(self.review)
        ret += '\n\nrelease: ' + str(self.releaseDate)
        ret += '\n\npublisher: ' + str(self.publisher)
        ret += '\n\ndeveloper: ' + str(self.developer)

        return ret



if __name__=='__main__':
    id=sys.argv[1]
    id0 = int(int(id) / 100000)
    id1 = int(int(id) / 1000)
    path='html/{}/{}/{}.html'.format(id0, id1, id)
    p = ProductInfo(id, path)
    print(p)