import json

# estructura de datos
alumnado = [ 
			 {"nombre": "Luisa"},
			 {"nombre": "Maria"}
		   ]

# guardar en formato json
manf = open("datos.json", "w")
json.dump(alumnado, manf)
manf.close()

with open("datos.json", "w") as manf:
	json.dump(alumnado, manf) 

# leer datos del archivo
manf = open("datos.json")
alumnado2 = json.load(manf) 
print(alumnado2)
