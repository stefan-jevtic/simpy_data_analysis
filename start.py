import sys
from Gfk.Analysis import GfkAnalysis
from Keywords.Analysis import KeywordsAnalysis

if len(sys.argv) < 3:
    raise ValueError('Please insert the type of analysis!')

shop_id = sys.argv[2]
type = sys.argv[1]

if type == 'gfk':
    a = GfkAnalysis(shop_id)
    a.overallNumber()
    a.placementAnalysis()

elif type == 'keywords':
    a = KeywordsAnalysis(shop_id)
    a.overallNumber()
    # a.analysisByShop()

elif type == 'category':
    a = GfkAnalysis(shop_id)
    a.overallNumber()
    a.placementAnalysis()

else:
    raise ValueError('There is no such type of data analysis!')
