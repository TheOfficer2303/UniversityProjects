import psycopg2

def connect():
  conn = psycopg2.connect(
    host="localhost",
    database="projekt1",
    user="postgres",
    password="bazepodataka")
  
  return conn


def get_field(file_path, field):
  file = open(file_path, "r")
  fields = []
  for line in file:
    if line.startswith(f'product/{field}:'):
      splitted = line.split(f'product/{field}: ')
      fields.append(splitted[1].strip())
    elif line.startswith(f'review/{field}:'):
      splitted = line.split(f'review/{field}: ')
      fields.append(splitted[1].strip())
      
  file.close()
  return fields


def prepare_values(values):
  val = len(values[0])
  prepared_values = []

  for i in range(val):
    t = (f"{values[0][i]}", f"{values[1][i]}", f"{values[2][i]}")
    prepared_values.append(t)

  return prepared_values


def insert_rows(connection, table, values): 
  cur = connection.cursor()
  prep_values = prepare_values(values)

  args = ','.join(cur.mogrify("(%s,%s,%s)", i).decode('utf-8') for i in prep_values)

  sql = f'INSERT INTO {table} VALUES {args}'
  cur.execute(sql)

  connection.commit()
  cur.close()


if __name__ == '__main__':
  file_path = input('File\'s absoulte path: ')
  
  titles = get_field(file_path, 'title')
  summaries = get_field(file_path, 'summary')
  texts = get_field(file_path, 'text')

  insert_rows(connect(), 'reviews', [titles, summaries, texts])

  
  