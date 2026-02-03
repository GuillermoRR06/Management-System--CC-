from datetime import *
# Funciones auxiliares, para buscar y ordenar fechas
#-----------------------------------------------------------------------------------------------------------
def BS_Date(l: list, d: date) -> int:
    if len(l) != 0:
        left = 0
        right = len(l)-1
        while left <= right:
            mid = (left + right)//2
            midDate = date(l[mid]["id"][0], l[mid]["id"][1], l[mid]["id"][2])
            if d == midDate: return mid
            elif d < midDate: right = mid - 1
            else: left = mid + 1
    return -1
#-----------------------------------------------------------------------------------------------------------
def Sort_Dates(l: list) -> None:
    if len(l) <= 1: return
    mid = len(l)//2
    left = l[:mid]
    right = l[mid:]
    
    Sort_Dates(left)
    Sort_Dates(right)
    
    i, j, k = 0, 0, 0
    while i < len(left) and j < len(right):
        d1 = date(left[i]["id"][0], left[i]["id"][1], left[i]["id"][2])
        d2 = date(right[j]["id"][0], right[j]["id"][1], right[j]["id"][2])
        if d1 <= d2:
            l[k] = left[i]
            i+=1
        else:
            l[k] = right[j]
            j+=1
        k+=1
    
    while i < len(left):
        d1 = date(left[i]["id"][0], left[i]["id"][1], left[i]["id"][2])
        l[k] = left[i]
        i+=1
        k+=1
    while j < len(right):
        d2 = date(right[j]["id"][0], right[j]["id"][1], right[j]["id"][2])
        l[k] = right[j]
        j+=1
        k+=1
#-----------------------------------------------------------------------------------------------------------