def mymax(iterable, key=lambda x: x):
  max_x=max_key=None

  for x in iterable:
    if (max_x is None and max_key is None) or key(x) > max_key:
      max_x = x
      max_key = key(x)

  return max_x

def main():
  maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
  maxchar = mymax("Suncana strana ulice")
  strings = ["Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"]
  maxstring = mymax(strings)
  D = {'burek':8, 'buhtla':5}
  maxdict = mymax(D, D.get)

  osoba = [('Pero', 'Nikic'), ('Niko', 'Peric'), ('Vasko', 'Vasic')]
  maxosoba = mymax(osoba, lambda x: (x[1], x[0]))

  print(maxint)
  print(maxchar)
  print(maxstring)
  print(mymax(strings, len))
  print(maxdict)
  print(maxosoba)



if __name__ == "__main__":
  main()
