#Contar cuantos de ellos superan el valor de 100

lista = [1000,6000,400,23,130,400,60,2000]

mayores100 = len({x for x in lista if x > 100})

print(mayores100)