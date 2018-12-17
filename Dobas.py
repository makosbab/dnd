# -*- coding: utf-8 -*-
'''
Created on 2018. okt. 3.

@author: tothr
'''
import re
import random
from collections import namedtuple

REGKIF_DOBAS = r'(?P<db_kocka>\d+)d(?P<oldalak>\d{2|3|4|6|8|10|20|100})(?:x(?P<szorzo>\d)+)?(?P<bonusz>[\+|\-]\d+)?'

Dobas = namedtuple("Dobas", ("db_kocka", "oldalak", "szorzo", "bonusz"))

def dobas_tisztits(dobas):
    talalat = re.match(REGKIF_DOBAS, dobas).groupdict()
    return {
        k : (int(e) if e is not None else 0) for k, e in talalat.items()
    }

def dobj(dobas):
    eredmeny = 0
    dobas = Dobas(**dobas_tisztits(dobas))
    kockak = [range(1, dobas.oldalak + 1)] * dobas.db_kocka
    for kocka in kockak:
        dobott_ertek = random.choice(kocka)
        eredmeny += dobott_ertek

    eredmeny += dobas.bonusz
    return eredmeny


class Mento():
    teljes_mento = 0
    alap_mento = 0
    tulajdonsag_modosito = 0
    varazslat_modosito = 0
    kieg_modosito = 0
    ideiglenes_modosito = 0
    felteteles_modosito = 0

    def __init__(self):
        pass


class SzivossagMento(Mento):
    pass

class GyorsasagMento(Mento):
    pass

class AkarateroMento(Mento):
    pass


"""
Mentődobás
3 md értéke lehet: erősebb vagy gyengébb
A gyengébb fejlődése: 3-1 táblátzatban mentő módosító gyenge/erős
"""
class Fejlesztes():
    def __init__(self, eletkocka, tamadas_bonusz, jo_mentodobas, szakertelem_pontok):
        self.eletkocka = eletkocka
        self.tamadas_bonusz = tamadas_bonusz
        self.jo_mentodobas = jo_mentodobas
        self.szakertelem_pontok = szakertelem_pontok


    def __str__(self):
        return "Fejlesztés:- életkocka = {}, támadás bónusz = {}, jó mentődobás = {}, szakértelem pontok = {}".format(
            self.eletkocka,
            self.tamadas_bonusz,
            self.jo_mentodobas,
            self.szakertelem_pontok)
