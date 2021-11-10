# coding: utf-8

import pickle
import datetime
import MySQLdb

def escape_qt(src):
    if src:
        return src.replace("'", "''")
    return ''

cnn = MySQLdb.connect(host='db',
                                  port=3306,
                                  db='db_steam_product',
                                  user='root',
                                  passwd='root',
                                  charset="utf8mb4")

cur = cnn.cursor(MySQLdb.cursors.DictCursor)

cur.execute("DELETE FROM product;")
cur.execute("DELETE FROM user_language;")
cur.execute("DELETE FROM tag;")
cur.execute("DELETE FROM genre;")
cur.execute("DELETE FROM price;")
cur.execute("DELETE FROM discount_price;")

datas = pickle.load(open('steam.pickle', 'rb'))

for d in datas:
    if d.status == 'error' or d.status == 'invalid':
        continue
    releaseDate = d.releaseDate
    if releaseDate == None:
        releaseDate = datetime.datetime(1900, 1, 1)
    if d.price:
        product = [d.id, d.status, escape_qt(d.title), escape_qt(d.publisher), escape_qt(d.developer), releaseDate, d.price.price, d.price.country]
    else:
        product = [d.id, d.status, escape_qt(d.title), escape_qt(d.publisher), escape_qt(d.developer), releaseDate, 0, '']
    if d.languages:
        languages = [[d0.title, d0.interface, d0.full_audio, d0.subtitles] for d0 in d.languages]
    else:
        languages = []
    if d.tags:
        tags = [escape_qt(d0) for d0 in d.tags]
    else:
        tags = []
    if d.review:
        review = [d.review.title, d.review.reviewCount, d.review.ratingValue, d.review.maxRating, d.review.minRating]
    else:
        review = ['', 0, -1, -1, -1]
    if d.genres:
        genres = d.genres # [string]
    else:
        genres = []
    if d.prices:
        prices = d.prices # [float]
    else:
        prices = []
    if d.discount_prices:
        discount_prices = [[d0.price, d0.discounted_price] for d0 in d.discount_prices if d0 != None]
    else:
        discount_prices = []

    #cur.execute
    try:
        cur.execute("INSERT INTO product(id,status_flag,title,publisher,developer,release_date,price,price_country,review_type, review_count, rating_value, max_rating, min_rating) VALUES({},'{}','{}','{}','{}','{}',{},'{}','{}',{},{},{},{});"
            .format(product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], review[0], review[1], review[2], review[3], review[4]))
        for lang in languages:
            cur.execute("INSERT INTO user_language(id, lang_title, interface, full_audio, subtitles) VALUES({}, '{}', {}, {}, {});".format(product[0], lang[0], lang[1], lang[2], lang[3]))
        for tag in tags:
            cur.execute("INSERT INTO tag(id, tag) VALUES({}, '{}');".format(product[0], tag))
        for genre in genres:
            cur.execute("INSERT INTO genre(id, genre) VALUES({}, '{}');".format(product[0], genre))
        for price in prices:
            cur.execute("INSERT INTO price(id, price) VALUES({}, {});".format(product[0], price))
        for discount_price in discount_prices:
            cur.execute("INSERT INTO discount_price(id, original_price, discouted_price) VALUES({}, {}, {});".format(product[0], discount_price[0], discount_price[1]))
    except Exception as e:
        print (e)
        print('id: ', d.id)
        exit()


cnn.commit()

cur.close()
cnn.close()
