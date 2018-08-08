import sys
from Analysis.Analysis import Analysis

shop_id = sys.argv[1]
a = Analysis(shop_id)
a.overallNumber()
a.placementAnalysis()
