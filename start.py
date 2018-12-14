# import sys
# from Germany.Gfk.Analysis import GfkAnalysis
# from Germany.Keywords.Analysis import KeywordsAnalysis
# from Germany.Category.Analysis import CategoryAnalysis
#
# if len(sys.argv) < 2:
#     raise ValueError('Please insert the type of analysis!')
#
# type = sys.argv[1]
#
# if type == 'gfk':
#     a = GfkAnalysis()
#     shop_id = input('Please enter shop id or any other characters to exit: \n')
#     try:
#         shop_id = int(shop_id)
#     except ValueError:
#         print('Bye')
#         sys.exit(1)
#     while True:
#         a.overallNumber(shop_id)
#         a.placementAnalysis(shop_id)
#         shop_id = input('Please enter shop id or any other characters to exit: \n')
#         try:
#             shop_id = int(shop_id)
#         except ValueError:
#             print('Bye')
#             break
#     sys.exit(1)
#
# elif type == 'keywords':
#     a = KeywordsAnalysis()
#     a.overallNumber()
#     shop_id = input('Please enter shop id or any other characters to exit: \n')
#     try:
#         shop_id = int(shop_id)
#     except ValueError:
#         print('Bye')
#         sys.exit(1)
#     while True:
#         a.analysisByShop(shop_id)
#         shop_id = input('Please enter shop id or any other characters to exit: \n')
#         try:
#             shop_id = int(shop_id)
#         except ValueError:
#             print('Bye')
#             break
#     sys.exit(1)
# elif type == 'category':
#     a = CategoryAnalysis()
#     a.overallNumber()
#     shop_id = input('Please enter shop id or any other characters to exit: \n')
#     try:
#         shop_id = int(shop_id)
#     except ValueError:
#         print('Bye')
#         sys.exit(1)
#     while True:
#         a.analysisByShop(shop_id)
#         shop_id = input('Please enter shop id or any other characters to exit: \n')
#         try:
#             shop_id = int(shop_id)
#         except ValueError:
#             print('Bye')
#             break
#     sys.exit(1)
#
# elif type == 'export_kws':
#     a = KeywordsAnalysis()
#     a.exportExcel()
#
# elif type == 'export_cat':
#     a = CategoryAnalysis()
#     a.exportExcel()
#
# else:
#     raise ValueError('There is no such type of data analysis!')

from International.ProductInfo.Analysis import ProductAnalysis

a = ProductAnalysis('ru', '1')
a.analyze()
