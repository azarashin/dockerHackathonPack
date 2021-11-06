# coding: utf-8

import pickle
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import numpy as np
import codecs

class SpotIndex:
    def __init__(self, datas, number_of_separator):
        spot = sorted(datas)
        outspot = int(len(spot) * 0.05)
        print(outspot)
        spot = spot[outspot:-outspot]

        self.number_of_separator = number_of_separator
        self.max = max(spot)
        self.min = min(spot)
        self.width = (self.max - self.min) / number_of_separator
        self.separators = [self.min + d * self.width for d in range(number_of_separator + 1)]

    def label(self, index):
        if index == 0:
            return '~ {}'.format(self.separators[0])
        if index >= len(self.separators):
            return '{} ~'.format(self.separators[-1])
        return '{} ~ {}'.format(self.separators[index - 1], self.separators[index])

    def index(self, value):
        if value < self.separators[0]:
            return 0
        if value > self.separators[-1]:
            return self.number_of_separator + 1
        return int((value - self.min) / self.width) + 1

class HtmlGenerator:
    def __init__(self, dir):
        self.fd = None
        self.dir = dir
        self.chart_id = 0
        self.index = [[None, []]]

    def set_group(self, group):
        self.index.append([group, []])
    
    def output_index(self):
        with codecs.open(self.dir + '/index.html', 'w', 'utf-8') as f:
            f.write('<html>\n<head>\n</head>\n<body>\n')
            for g in self.index:
                title = g[0]
                items = g[1]
                if title:
                    f.write('\t<h1>{}</h1>\n'.format(title))
                    f.write('\t<ul>\n')
                for item in items:
                    f.write('\t<li><a href="{}">{}</a></li>\n'.format(item[0], item[1]))
                if title:
                    f.write('\t</ul>\n')

    def open(self, name, title):
        self.name = name
        self.fd = codecs.open(self.dir + '/' + self.name, 'w', 'utf-8')
        self.fd.write('<html>\n')
        self.fd.write('<head>\n')
        self.fd.write('<title>{}</title>\n'.format(title))
        self.fd.write('</head>\n')
        self.fd.write('<body>\n')
        self.fd.write('<h1>{}</h1>\n'.format(title))
        self.index[-1][1].append((name, title))

    def close(self):
        self.fd.write('</body>\n')
        self.fd.write('</html>\n')
        self.fd.close()
        self.fd = None

    def hist(self, datas, selectors, number_of_separator=16):
        filename = '{}.png'.format(self.chart_id)
        filepath = '{}/{}'.format(self.dir, filename)
        sorted_datas = sorted([[d.title, d.id] + [s[1](d) for s in selectors] for d in datas], key = lambda x : x[2])
        values = [d[2] for d in sorted_datas]
        fig = plt.figure()
        plt.hist(values, bins=number_of_separator, ec='black')
        fig.savefig(filepath)
        self.chart_id += 1

        info = self.table([[len(values)], [np.mean(values)], [statistics.median(values)], [np.std(values)], [min(values)], [max(values)]], None, ['count', 'mean', 'median', 'std', 'min', 'max'], False)

        self.fd.write('<table border="0">\n\t<tr>\n')
        self.fd.write('\t\t<td>\n{}\t\t</td>\n'.format(info))
        self.fd.write('\t\t<td><img src="{}"/></td>\n'.format(filename))
        self.fd.write('\t</tr>\n</table>\n')

        attribs = ['title', 'id'] + [s[0] for s in selectors]

        limit = 16
        high_data = sorted_datas[:limit]
        low_data = sorted_datas[-limit:]
        sample_data = sorted_datas[::int(len(sorted_datas)/limit)]
        table_high = self.table([d[1:] for d in high_data], attribs, [d[0] for d in high_data], False)
        table_low = self.table([d[1:] for d in low_data], attribs, [d[0] for d in low_data], False)
        table_sample = self.table([d[1:] for d in sample_data], attribs, [d[0] for d in sample_data], False)

        self.fd.write('<table border="0">\n\t<tr>\n')
        self.fd.write('\t\t<td>\n{}\t\t</td>\n'.format(table_high))
        self.fd.write('\t\t<td>\n{}\t\t</td>\n'.format(table_low))
        self.fd.write('\t\t<td>\n{}\t\t</td>\n'.format(table_sample))
        self.fd.write('\t</tr>\n</table>\n')
    
    def table_product_info(self, datas, selectors):
        self.table([[s[1](d) for s in selectors] for d in datas], [s[0] for s in selectors], [d.title for d in datas])

    def table(self, datas, attribs, labels, write_flag):
        ret = ''
        if attribs != None:
            ret += '<table border="1">\n\t<tr>\n\t\t<th>' + '</th><th>'.join(attribs) + '</th>\n\t</tr>\n'
        else:
            ret += '<table border="1">\n'
        for i in range(len(datas)):
            if labels != None:
                ret += '\t<tr>\n\t\t<td>{}</td><td>{}</td>\n\t</tr>\n'.format(labels[i], '</td><td>'.join([str(s) for s in datas[i]]))
            else:
                ret += '\t<tr>\n\t\t<td>{}</td>\n\t</tr>\n'.format(labels[i], '</td><td>'.join([str(s) for s in datas[i]]))
        ret += '</table>\n'
        if write_flag:
            self.fd.write('{}\n'.format(ret))

        return ret

def hist(datas, number_of_separator=16):
    spot_index = SpotIndex(datas, number_of_separator)
    ret = [0] * (number_of_separator + 2)
    for d in datas:
        ret[spot_index.index(d)] += 1
    return [(spot_index.label(d), ret[d]) for d in range(number_of_separator+2)]



datas = pickle.load(open('steam.pickle', 'rb'))

errors = [d for d in datas if d.status == 'error']
invalids = [d for d in datas if d.status == 'invalid']
closed = [d for d in datas if d.status == 'closed']
actives = [d for d in datas if d.status == 'active']

review_count_selector = [
    ('review count', lambda d: d.review.reviewCount  if d.review != None else 0)
]

price_review_selector = [
    ('price', lambda d: d.price.price  if d.price != None else 0), 
    ('review count', lambda d: d.review.reviewCount  if d.review != None else 0)
]

reviewCounts = [review_count_selector[0][1](d) for d in actives]
max_review = max(reviewCounts)

print('max_review: {}\n'.format(max_review))

hist_review_count = hist(reviewCounts)
print(hist_review_count)

gen = HtmlGenerator('output')

gen.set_group('概要')
gen.open('titles.html', 'タイトル数')
gen.table([[len(datas), len(actives), len(closed), len(invalids), len(errors)]]
    , ['', '全ID', '販売中タイトル', '販売終了したタイトル', '無効なID', '読み込みエラー'], ['タイトル数'], True)
gen.close()

gen.set_group('レビュー数の分布')

gen.open('all_reviews.html', '全レビュー中のレビュー数分布')
gen.hist(actives, review_count_selector)
gen.close()

class Company:
    def __init__(self, name):
        self.name = name
        self.publish = 0
        self.develop = 0
        self.sum_publish_prices = []
        self.sum_devlop_prices = []

    def add(self, product):
        if product.publisher == self.name:
            self.publish += 1
            if product.price:
                self.sum_publish_prices.append(product.price.price)
            else:
                self.sum_publish_prices.append(None)
        if product.developer == self.name:
            self.develop += 1
            if product.price:
                self.sum_devlop_prices.append(product.price.price)
            else:
                self.sum_devlop_prices.append(None)

    @classmethod
    def attribs(cls):
        return ['name', 'publish', 'develop', 'publish(on sale)', 'develop(on sale)']

companies = {}
for d in datas:
    if d.status != 'active' and d.status != 'closed':
        continue
    tasks = []
    if d.publisher != None and d.developer == d.publisher:
        tasks.append(d.publisher)
    if d.publisher != None and d.developer != d.publisher:
        tasks.append(d.publisher)
    if d.developer != None and d.developer != d.publisher:
        tasks.append(d.developer)
    for t in tasks:
        if not t in companies:
            companies[t] = Company(t)
        companies[t].add(d)
    



review_threthold = [1000, 5000, 10000, 50000, 100000]

gen.open('low_reviews.html', 'レビュー数{}件未満のゲームにおけるレビュー数分布'.format(review_threthold[0]))
gen.hist([d for d in actives if d.review == None or d.review.reviewCount < review_threthold[0]], review_count_selector)
gen.close()

for i in range(len(review_threthold) - 1):
    gen.open('reviews_{}_{}.html'.format(review_threthold[i], review_threthold[i+1]),
         'レビュー数{}件以上{}件未満のゲームにおけるレビュー数分布'.format(review_threthold[i], review_threthold[i+1]))
    gen.hist([d for d in actives if d.review != None and d.review.reviewCount >= review_threthold[i] and d.review.reviewCount < review_threthold[i+1]], review_count_selector)
    gen.close()


gen.open('high_reviews.html', 'レビュー数{}件以上のゲームにおけるレビュー数分布'.format(review_threthold[-1]))
gen.hist([d for d in actives if d.review != None and d.review.reviewCount >= review_threthold[-1]], review_count_selector)
gen.close()



gen.set_group('価格の分布')

gen.open('low_reviews_price.html', 'レビュー数{}件未満のゲームにおける価格分布'.format(review_threthold[0]))
gen.hist([d for d in actives if d.review == None or d.review.reviewCount < review_threthold[0]], price_review_selector)
gen.close()

for i in range(len(review_threthold) - 1):
    gen.open('reviews_{}_{}_price.html'.format(review_threthold[i], review_threthold[i+1]),
         'レビュー数{}件以上{}件未満のゲームにおける価格分布'.format(review_threthold[i], review_threthold[i+1]))
    gen.hist([d for d in actives if d.review != None and d.review.reviewCount >= review_threthold[i] and d.review.reviewCount < review_threthold[i+1]], price_review_selector)
    gen.close()


gen.open('high_reviews_price.html', 'レビュー数{}件以上のゲームにおける価格分布'.format(review_threthold[-1]))
gen.hist([d for d in actives if d.review != None and d.review.reviewCount >= review_threthold[-1]], price_review_selector)
gen.close()


gen.output_index()
