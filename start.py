import sys
from International.ProductInfo.Analysis import ProductAnalysis
from International.Keywords.Analysis import KeywordsAnalysis

if len(sys.argv) < 2:
    raise ValueError('Please insert the type of analysis!')

type = sys.argv[1]

if type == 'product':
    country = sys.argv[2]
    while True:
        try:
            shop_id = input('Please enter shop id or any other characters to exit: \n')
            shop_id = int(shop_id)
            a = ProductAnalysis(country, str(shop_id), 'cli')
            a.analyze()
        except ValueError:
            print('Bye')
            break
    sys.exit(1)
elif type == 'kw':
    country = sys.argv[2]
    while True:
        try:
            shop_id = input('Please enter shop id or any other characters to exit: \n')
            shop_id = int(shop_id)
            a = KeywordsAnalysis(country, str(shop_id), 'cli')
            a.analyze()
        except ValueError:
            print('Bye')
            break
    sys.exit(1)
elif type == 'cat':
    pass
else:
    raise Exception('No such type of scraper!')
