# uso de print en lugar de retorno
def say_hello():
    print("estoy ejecutando la función")


# basta con invocar
say_hello()


# uso de retorno
def say_goodbye():
    return "adiós mundo cruel"


# almaceno el valor devuelto por la función en una variable
variable = say_goodbye()
# imprimo la variable
print(variable)
