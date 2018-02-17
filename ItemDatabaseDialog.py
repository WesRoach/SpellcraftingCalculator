# HEADER PLACE HOLDER

from json import load

data = load(open(r'database/ItemDatabase.json'))
meta = load(open(r'database/ItemDatabaseMetaData.json'))


for item in data['items']:
    print(
        'ID:', item['id'],
        ', Name:', item['name'],
        ', Realm:', meta['realm'][str(item['realm'])],
    )

# for item in data['items']:
#     for key, value in item.items():
#         if key in ('realm', 'slot'):
#             for index in meta[key]:
#                 if str(value) == index:
#                     print(meta[key][index])
