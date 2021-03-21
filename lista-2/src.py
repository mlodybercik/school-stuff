import numpy as np
import random
import time
from matplotlib import pyplot as plt

def generuj_tablice(wielkosc: int, a: int = -1e7, b: int = +1e7) -> np.array:
    assert wielkosc > 0 and type(wielkosc) == int
    tab = np.zeros(wielkosc)
    for entry in range(wielkosc):
        tab[entry] = random.randint(a, b)
    return tab

def timeit(fn, size, **kwargs):
    tablica = generuj_tablice(size, **kwargs)
    start = time.time()
    fn(tablica)
    return time.time() - start

def bubble(tab):
    for i in range(len(tab)):
        for j in range(0, len(tab)-1):
            if (tab[j]>tab[j+1]):
                temp=tab[j]
                tab[j]=tab[j+1]
                tab[j+1]=temp
    return tab

def insert(tab):
    for i in range(len(tab)):
        for j in range(0,i):
            if (tab[i]<tab[j]):
                temp=tab[i]
                tab[i]=tab[j]
                tab[j]=temp
    return tab

def select(tab):
    for i in range(len(tab)):
        for j in range(i+1,len(tab)):
            if (tab[i]>tab[j]):
                temp=tab[i]
                tab[i]=tab[j]
                tab[j]=temp
    return tab

print(bubble(generuj_tablice(5, -10, 10)))
print(insert(generuj_tablice(5, -10, 10)))
print(select(generuj_tablice(5, -10, 10)))

wielkosci = list(range(1, 101, 5))
# wielkosci = list(range(1, 10001, 50))
# Nie radze liczyć dla tych ^^ parametrów. Mi sie liczyło >12h
czasy = []
for funkcja in [bubble, insert, select]:
    czas = []
    for size in wielkosci:
        czas_per_wielkosc = []
        for _ in range(10):
            czas_per_wielkosc.append(timeit(funkcja, size))
        czas.append(np.mean(czas_per_wielkosc))
    czasy.append(czas)

fig = plt.figure()
ax = plt.subplot()
for i in zip(enumerate([bubble, insert, select]), ["red", "green", "blue"]):
    ax.plot(wielkosci, czasy[i[0][0]], color=i[1], label=str(i[0][1]).split()[1])
    ax.legend()
plt.xlabel("wielkość zbioru [1]")
plt.ylabel("czas [s]")
plt.show()

def bubble_mod1(tab):
    # przerwanie gdy nie było żadnej zamiany
    for i in range(len(tab)):
        for j in range(0, len(tab)-1):
            if (tab[j]>tab[j+1]):
                temp=tab[j]
                tab[j]=tab[j+1]
                tab[j+1]=temp
            else:
                continue
    return tab

def bubble_mod2(tab):
    # jedno mniej co iteracje
    for i in range(len(tab)):
        for j in range(0, len(tab)-1 - i):
            if (tab[j]>tab[j+1]):
                temp=tab[j]
                tab[j]=tab[j+1]
                tab[j+1]=temp
    return tab

print(bubble_mod1(generuj_tablice(5, -10, 10)))
print(bubble_mod2(generuj_tablice(5, -10, 10)))

wielkosci = list(range(1, 1001, 10))
czasy = []
for funkcja in [bubble, bubble_mod1, bubble_mod2]:
    czas = []
    for size in wielkosci:
        print(size)
        czas_per_wielkosc = []
        for _ in range(10):
            czas_per_wielkosc.append(timeit(funkcja, size))
        czas.append(np.mean(czas_per_wielkosc))
        clear_output(wait = True)
    czasy.append(czas)
    
fig = plt.figure()
ax = plt.subplot()
for i in zip(enumerate([bubble, bubble_mod1, bubble_mod2]), ["red", "green", "blue"]):
    ax.plot(wielkosci, czasy[i[0][0]], color=i[1], label=str(i[0][1]).split()[1])
    ax.legend()
plt.xlabel("wielkość zbioru [1]")
plt.ylabel("czas [s]")
plt.show()
