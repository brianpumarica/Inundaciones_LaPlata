# Filtros

# Mapea un string a un booleano
from app import db


def from_string_to_bool(status):
    if status == "1":
        status = True
    else:
        status = False
   

# Mapea un valor booleano a un mensaje especifico


def boolean_converter(value, true_message, false_message):
    if bool(value):
        return true_message
    return false_message


# Mapea un valor none a un mensaje especifico


def none_converter(value, message):
    if value == None:
        return message
    else:
        return value


# Mapea un arreglo, y devuelve el elemento de esa posicion
def int_converter(value, messages):
    return messages[int(value)]

# Devuelve las coordenadas en forma de lista


def list_converter(coord):
    #  Remuevo el primer y el ultimo caracter de cada lista de coordenadas
    aux = coord[1:-1]

    # Reemplazo los ],[ por espacios
    aux = aux.replace("],[", " ")

    # Armo una lista con coordenadas separadas por espacios
    aux = aux.split()

    # Para iterar por cada coordenada
    # for i in range(0, len(aux), 1):
    #     print(aux[i])

    return aux


# Devuelve la cantidad de coordenadas


def list_counter(coord):
    return len(list_converter(coord))


# Mapea el string que indica el orden de los listados al correspondiente ascendente o descendente


def order_converter(word, asc, desc):
    if word[0].lower() == "a":
        return asc
    else:
        return desc


def parse_input(input):
    if input == "first_name":
        return "Nombre"
    elif input == "last_name":
        return "Apellido"
    elif input == "username":
        return "Nombre de usuario"
    elif input == "email":
        return "Email"
    else:
        return "Contraseña"


def get_config():
    return "#CD5C5C"
