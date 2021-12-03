# Python program to read
# json file


import json

# Opening JSON file
f = open('wallets.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data:
    print(data[i]['address'])
    print(type(data[i]['address']))

# Closing file
f.close()
