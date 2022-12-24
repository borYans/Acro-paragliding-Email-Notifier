N_1 = range(348, 360)
N_2 = range(0, 11)
NNE = range(11, 34)
NE = range(34, 56)
ENE = range(56, 79)
E = range(79, 101)
ESE = range(101, 124)
SE = range(124, 146)
SSE = range(146, 169)
S = range(169, 191)
SSW = range(191, 214)
SW = range(214, 236)
WSW = range(236, 259)
W = range(259, 281)
WNW = range(281, 304)
NW = range(304, 326)
NNW = range(326, 348)


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius)


def get_wind_direction(direction_in_degrees):
    if direction_in_degrees in N_1 or N_2:
        return "Sever"
    elif direction_in_degrees in NNE:
        return "Sever-Severoistok"
    elif direction_in_degrees in NE:
        return "Severoistok"
    elif direction_in_degrees in ENE:
        return "Istok-Severoistok"
    elif direction_in_degrees in E:
        return "Istok"
    elif direction_in_degrees in ESE:
        return "Istok-Jugoistok"
    elif direction_in_degrees in SE:
        return "Jugoistok"
    elif direction_in_degrees in SSE:
        return "Jug-Jugoistok"
    elif direction_in_degrees in S:
        return "Jug"
    elif direction_in_degrees in SSW:
        return "Jug-Jugozapad"
    elif direction_in_degrees in SW:
        return "Jugozapad"
    elif direction_in_degrees in WSW:
        return "Zapad-Jugozapad"
    elif direction_in_degrees in W:
        return "Zapad"
    elif direction_in_degrees in WNW:
        return "Zapad-Severozapad"
    elif direction_in_degrees in NW:
        return "Severozapad"
    elif direction_in_degrees in NNW:
        return "Sever-Severozapad"
    else:
        return "Nepoznat pravec na veter"
