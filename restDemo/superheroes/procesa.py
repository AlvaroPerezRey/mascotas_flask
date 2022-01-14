import json

t = list()
manf = open("list.txt")
for line in manf:
	data = line.strip().split()
	t.append({"id": data[0], "name": ' '.join(data[1:])})

with open("list.json", "w") as f:
	json.dump(t, f) 
