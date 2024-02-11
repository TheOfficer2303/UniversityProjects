from pymongo import MongoClient
from datetime import datetime



def get_field(file_path):
  file = open(file_path, "r")
  videogames = []
  document = {}

  for line in file:
    if line == '\n':
      videogames.append(document)
      document = {}
      continue

    line_splitted = line.split('/')
    kv = line_splitted[1].split(':')

    field = kv[0]
    value = kv[1].strip()

    if field == 'time':
      value = datetime.fromtimestamp(int(value))
    elif field == 'price' or field == 'score':
      if value != 'unknown':
        value = float(value)

    document[field] = value

  file.close()
  return videogames


if __name__ == '__main__':
  client = MongoClient()

  db = client.projekt3

  file_path = input('File\'s absoulte path: ')

  videogames = get_field(file_path)

  result = db.videogames.insert_many(videogames)

  client.close()