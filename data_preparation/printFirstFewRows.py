FILENAME = ".csv"

file = open("data/games.csv")
n = 20
head = [next(file) for x in range(20)]
for line in head:
  print(line)
