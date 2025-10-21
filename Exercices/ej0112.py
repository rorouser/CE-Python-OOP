#Contar cuantos de ellos tienen más de 5 char

lista = ["juan","ana","carlos","marcos","luis"]

mayores5char = len({x for x in lista if len(str(x))>5})

print(mayores5char)