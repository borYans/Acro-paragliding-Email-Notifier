N_1 = range(348, 361)
N_2 = range(0, 12)
NNE = range(11, 35)
NE = range(34, 57)
ENE = range(56, 80)
E = range(79, 102)
ESE = range(101, 125)
SE = range(124, 147)
SSE = range(146, 170)
S = range(169, 192)
SSW = range(191, 215)
SW = range(214, 237)
WSW = range(236, 260)
W = range(259, 282)
WNW = range(281, 305)
NW = range(304, 327)
NNW = range(326, 349)


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius)


def get_wind_direction(direction_in_degrees):
    if direction_in_degrees in NNE:
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
        return "Sever"
