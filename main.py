from operaciones import resta, suma, MiClase

resultado_suma = suma(5, 3)
print("Resultado de la suma:", resultado_suma)

resultado_resta = resta(10, 4)
print("Resultado de la resta:", resta.__doc__)

a = [1, 2, 3]
b = a.copy()
print(a is b)

x = 10
y = 10

print(x is not y)

print(MiClase.__doc__)
