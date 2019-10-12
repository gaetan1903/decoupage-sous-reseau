'''
    script permettant de decouper une addresse IP en sous reseaux en fonction
        en  de nombre de departements
'''
import re
import math


def base2todec(bin):
    cnv = 0
    n = 0
    bin = list(bin)
    for i in bin[::-1]:
        cnv += int(i)*(2**n)
        n += 1
    return cnv


def maskIso(mask):
    bt = list('00000000')
    val = mask % 8
    for i in range(val):
        bt[i] = '1'
    print(bt)
    return f"255.255.255.{base2todec(''.join(bt))}"

    return ''


ipd = ''
while not re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ipd):
    ipd = input("Entrer addresse réseau:  ")

maskd = ''
while not re.match(r'^\d{1,2}$', maskd):
    maskd = input("Entrer son masque : ")

nbSr = ''
while not re.match(r'\d', nbSr):
    nbSr = input("Entrer nombre de sous Réseaux: ")

sR = {}
for i in range(int(nbSr)):
    name = input(f"Entrer le nom du sous réseaux {i+1}: ")
    nbrPC = input(f"Entrer le nombre de PC: ")
    sR[name] = int(nbrPC)

sR = {k: v for k, v in sorted(sR.items(), key=lambda kv: kv[1], reverse=True)}
sRdec = {}
lastIp = ipd
for nom, nbr in sR.items():
    n = int(math.log2(nbr)) +  1
    newmask = 32 - n
    ipsr = lastIp
    sRdec[nom] = (ipsr, newmask, maskIso(newmask))
    lastIp = lastIp.split('.')
    lastIp[-1] = str(int(lastIp[-1]) + 2**n)
    lastIp = '.'.join(lastIp)

print(sRdec)

