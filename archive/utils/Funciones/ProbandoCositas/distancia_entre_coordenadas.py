import math
def distancia_entre_coordenadas(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    distacia = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distacia

x = (0.3516070725109587*800, 0.8611643721901525*740)
y = (0.44646617207348965*800, 0.698442479173005*740)

print(x, y)

dist = distancia_entre_coordenadas(x,y)
print(dist)