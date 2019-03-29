FILENAME = ".csv"

file = open("data/wellness.csv")
n = 20
head = [next(file) for x in range(20)]
print(head)
