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
    return f"255.255.255.{base2todec(''.join(bt))}"


def inverse(maskIS):
    spr = maskIS.split('.')
    inv_mask = []
    for bin in spr:
        bin = 255 - int(bin)
        inv_mask.append(str(bin))
    return '.'.join(inv_mask)


ipd, i = '', 0
while not re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ipd):
    ipd = input("Entrer l'addresse réseau >>>  "
        if i == 0 else "(Erreur) Entrer l'addresse réseau >>> ")
    i += 1

nbSr = ''
i = 0
while not re.match(r'\d+$', nbSr):
    nbSr = input("\nEntrer le nombre de sous réseau >>> "
        if i == 0 else "(Erreur) Entrer le nombre de sous réseau >>> ")
    i += 1

print()

sR = {}
for i in range(int(nbSr)):
    name = input(f"Entrer le nom du sous réseau {i+1}: ")
    nbrPC = ''
    while not re.match(r'\d', nbrPC):
        nbrPC = input(f"Entrer le nombre de PC: ")
    print("")
    sR[name] = int(nbrPC)

"""" 
if sum(sR.values()) > 254:
    print('Oupss! Le total des PCs est superieurs à 254, \nCe qui n\'est pas \
possible pour un réseau de masque 24')
    exit()
"""

sR = {k: v for k, v in sorted(sR.items(), key=lambda kv: kv[1], reverse=True)}
# Triage par plus grand nombre de PC par sous-réseau d'où reverse.
sRdec = {}
lastIp = ipd
for nom, nbr in sR.items():
    n_s = math.log2(nbr+2)  # On cherche d'abord n.
    n = int(n_s+1)
    newmask = 32 - n  # La formule de nouveau masque des sous réseaux.
    ipsr = lastIp
    nbrMax = 2**n - 2
    gateway = ipsr.split('.')
    gateway[-1] = str(int(gateway[-1])+1)
    gateway = '.'.join(gateway)

    broadcast = gateway.split('.')
    broadcast[-1] = str(int(broadcast[-1])+nbrMax)
    broadcast = '.'.join(broadcast)

    sRdec[nom] = (ipsr, nbr, (newmask, maskIso(newmask)), inverse(maskIso(newmask)), gateway, nbrMax, broadcast)
    lastIp = lastIp.split('.')
    newHostid = int(lastIp[-1]) + 2**n
    lastIp[-2] = str( int(lastIp[-2]) + (newHostid // 256) ) 
    lastIp[-1] = str( newHostid % 256)
    lastIp = '.'.join(lastIp)

for key, val in sRdec.items():  # Affichage des sous réseaux.
    print(f"""
        {key}: {val[1]} PCs
        --------------------------------------------
        Adresse réseau: {val[0]}/{val[2][0]}
        Masque sous réseau: {val[2][1]}
        Passerelle: {val[4]}
        Broadcast: {val[6]}
        Inverse Masque réseau: {val[3]}
        Nombre de Machine Max: {val[5]}
    """)
