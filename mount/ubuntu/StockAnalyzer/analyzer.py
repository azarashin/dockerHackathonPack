
import glob
import re
import pickle
import codecs

def analyze(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        data = f.read()
    pattern = r'<div class="md_target_box_price">([^<]+?)<span class="decimal">円</span></div>'
    re_pattern = re.compile(pattern, flags=re.DOTALL)
    target_price = [d.replace(',', '') for d in re_pattern.findall(data)]
    if len(target_price) != 1:
        target_price = ['-']

    pattern = r'<div class="stock_price">\s*?([^\s.<]+?)\.?<'
    re_pattern = re.compile(pattern, flags=re.DOTALL)
    current_price = [d.replace(',', '') for d in re_pattern.findall(data)]
    if len(current_price) != 1:
        current_price = ['-']

    pattern = r"<p class='md_stockBoard_stockName'>(.+?)</p>"
    re_pattern = re.compile(pattern, flags=re.DOTALL)
    name = re_pattern.findall(data)

    pattern = r'<p class="label">([^<]+?)</p>\s*<span class="md_picksPlate ([^\s]+) size_s dpbl">([^<]+?)</span>'
    re_pattern = re.compile(pattern, flags=re.DOTALL)
    evals = re_pattern.findall(data)

    pattern = r'<td class="tac">([^<]+?)</td>'
    re_pattern = re.compile(pattern, flags=re.DOTALL)
    ana_evals = re_pattern.findall(data)
    if len(ana_evals) != 5:
        ana_evals = ['-', '-', '-', '-', '-']

    ret = name + [evals[0][2], evals[1][2], evals[2][2]] + current_price + target_price + ana_evals
    return [d.replace('\n', '') for d in ret]


files = glob.glob("./html/**/*.html")
m = re.compile(r'./html/.+?/(.+?)\.html', flags=re.DOTALL)
datas = []
with codecs.open('result.csv', 'w', 'utf-8') as f:
    f.write('証券コード\t銘柄名\t株価診断\t個人予想\tアナリスト\t株価\t目標株価\t強気買い\t買い\t中立\t売り\t強気売り\n')
    for file in files:
        id = m.search(file.replace('\\', '/')).group(1)
        line = [id] + analyze(file)
        f.write('\t'.join(line)+'\n')


