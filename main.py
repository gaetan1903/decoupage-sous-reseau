'''
    Un script permettant de découper une addresse IP en des sous réseaux en
    fonction de nombre de sous réseaux et en fonction de nombre des machines.
'''


import re  # Module d'expression régulière en python
import math


def base2todec(bin):
    ''' Fonction de conversion de binaire en décimal '''
    cnv, n = 0, 0
    for i in bin[::-1]:
        cnv += int(i)*(2**n)
        n += 1
    return cnv


def maskIso(mask):
    ''' Fonction qui convertit le dernier octet de masque en binaire '''
    bt = list('00000000')
    val = mask % 8
    for i in range(val):
        bt[i] = '1'
    return "255.255.255.{}".format(base2todec(''.join(bt)))


ipd = ''
while not re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ipd):
    ipd = input("Entrer l'addresse réseau >>>  ")

nbSr = ''
while not re.match(r'\d', nbSr):
    nbSr = input("Entrer le nombre de sous réseau >>> ")

sR = {}
for i in range(int(nbSr)):
    name = input("Entrer le nom du sous réseau {}: ".format(i+1))
    nbrPC = ''
    while not re.match(r'\d', nbrPC):
        nbrPC = input("Entrer le nombre de PC: ")
    print("")
    sR[name] = int(nbrPC)

if sum(sR.values()) > 254:
    print('Oupss! Le total des PCs est superieurs à 254, \nCe qui n\'est pas \
possible pour un réseau de masque 24')
    exit()

# sR = {k: v for k, v in sorted(sR.items(), key=lambda kv: kv[1], reverse=True)}

for k,v in sorted(sR.items(), key=lambda kv: kv[1], reverse=True):
    sR[k] = v
# Triage par plus grand nombre de PC par sous-réseau d'où reverse.
sRdec = {}
lastIp = ipd
for nom, nbr in sR.items():
    n_s = math.log2(nbr+2)  # On cherche d'abord n.
    if n_s - int(n_s) == 0:
        n = int(n_s)
    else:
        n = int(n_s) + 1
    newmask = 32 - n  # La formule de nouveau masque des sous réseaux.
    ipsr = lastIp
    sRdec[nom] = (ipsr, nbr, (newmask, maskIso(newmask)))
    lastIp = lastIp.split('.')
    lastIp[-1] = str(int(lastIp[-1]) + 2**n)
    lastIp = '.'.join(lastIp)

for key, val in sRdec.items():  # Affichage des sous réseaux.
    print("""
        {}: {} PCs
        --------------------------------------------
        Adresse réseau: {}/{}
        Masque sous réseau: {}
    """.format(key, val[1], val[0], val[2][0], val[2][1]))
