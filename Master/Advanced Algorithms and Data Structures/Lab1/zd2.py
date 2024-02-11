person_data = {
  'Ana': 1995,
  'Zoran': 1978,
  'Lucija': 2001,
  'Anja': 1997
}

for key, val in person_data.items():
  person_data[key] = val - 1

year_age = []

for val in person_data.values():
  year_age.append((val, 2022 - val))
