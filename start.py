import sys
from Gfk.Analysis import GfkAnalysis
from Keywords.Analysis import KeywordsAnalysis
from Category.Analysis import CategoryAnalysis

if len(sys.argv) < 2:
    raise ValueError('Please insert the type of analysis!')

type = sys.argv[1]

if type == 'gfk':
    a = GfkAnalysis()
    shop_id = input('Please enter shop id or any other characters to exit: \n')
    try:
        shop_id = int(shop_id)
    except ValueError:
        print('Bye')
        sys.exit(1)
    while True:
        a.overallNumber(shop_id)
        a.placementAnalysis(shop_id)
        shop_id = input('Please enter shop id or any other characters to exit: \n')
        try:
            shop_id = int(shop_id)
        except ValueError:
            print('Bye')
            break
    sys.exit(1)

elif type == 'keywords':
    a = KeywordsAnalysis()
    a.overallNumber()
    shop_id = input('Please enter shop id or any other characters to exit: \n')
    try:
        shop_id = int(shop_id)
    except ValueError:
        print('Bye')
        sys.exit(1)
    while True:
        a.analysisByShop(shop_id)
        shop_id = input('Please enter shop id or any other characters to exit: \n')
        try:
            shop_id = int(shop_id)
        except ValueError:
            export = input('Do you want to make an export for all shops? (y|n)')
            if export == 'y':
                a.exportExcel()
            print('Bye')
            break
    sys.exit(1)
elif type == 'category':
    a = CategoryAnalysis()
    a.overallNumber()
    shop_id = input('Please enter shop id or any other characters to exit: \n')
    try:
        shop_id = int(shop_id)
    except ValueError:
        print('Bye')
        sys.exit(1)
    while True:
        a.analysisByShop(shop_id)
        shop_id = input('Please enter shop id or any other characters to exit: \n')
        try:
            shop_id = int(shop_id)
        except ValueError:
            export = input('Do you want to make an export for all shops? (y|n) ')
            if export == 'y':
                a.exportExcel()
            print('Bye')
            break
    sys.exit(1)

else:
    raise ValueError('There is no such type of data analysis!')
