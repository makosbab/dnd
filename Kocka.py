# -*- coding: utf-8 -*-
'''
Created on 2018. okt. 3.

@author: tothr
'''
import re
import random
class Kocka:

    def __init__ (self, oldalak, szazalekos = False, tizes = False):
        self.kocka_oldalak  = oldalak
        self.kocka_nev = 'd'+str(oldalak)
        if oldalak not in (2, 3, 4, 6, 8, 10, 12, 20, 100):
            raise Exception('Nem létezik {}-oldalú DnD kocka.'.format(oldalak))
        if oldalak is 10 and szazalekos:
            if tizes:
                self.kocka_ertekek = range(0,100,10)
            else:
                self.kocka_ertekek = range(0,10)
        else:
            self.kocka_ertekek = range(1, oldalak+1)

        self.minimum = min(self.kocka_ertekek)
        self.maximum = max(self.kocka_ertekek)

    def __str__(self):
        return 'Kocka típusa: d{}, értékei: {}'.format(self.kocka_oldalak, self.kocka_ertekek)

class Dobas:
    #(\d)?d(\d{1,2})([\s]?(\+|\-)[\s]?(\d*))?(x(\d))?(\+|\-)(\d*)
    #(\d)?d(\d{1,2})(x?(\d)+)?((\+|\-)(\d*))?
    REGKIF = '(\d)?d(\d{1,2})(x?(\d)+)?(\+|\-\d*)?'

    def __init__ (self, dobas='', kocka = None):
        self.kocka_oldalak = 0
        self.bonusz = 0
        self.dobas_eredmeny = 0
        self.dobott_ertekek = []
        self.pohar = []
        if dobas:
            self.dobando = dobas
        self.bonusz_elojel = ""
        self.szorzo = 0
        self.dobas_szorzo = 1
        talalat = re.match(self.REGKIF,self.dobando)
        if(talalat):
            if not talalat.group(1) or int(talalat.group(1)) == 0:
                self.kocka_db = 1
            else:
                self.kocka_db = int(talalat.group(1))

            self.kocka_oldalak = int(talalat.group(2))
            if talalat.group(4):
                self.dobas_szorzo = int(talalat.group(4))
            if talalat.group(5):
                self.bonusz = talalat.group(5)
        i = 0
        while i < self.kocka_db:
           kocka = Kocka(self.kocka_oldalak)
           self.pohar.append(kocka)
           i += 1

        for kocka in self.pohar:
            dobott_ertek = random.choice(kocka.kocka_ertekek)
            self.dobott_ertekek.append(dobott_ertek)

    @property
    def eredmeny(self):
        return sum(self.dobott_ertekek) * self.dobas_szorzo + self.bonusz

    def osszegezd(self):
        for i in self.dobott_ertekek:
            self.dobas_eredmeny += i
        self.dobas_eredmeny *= self.dobas_szorzo
        self.dobas_eredmeny += self.bonusz

    def __str__(self):
        return '{} dobás értékei: {}, dobás szorzó: {}, módosító: {}, eredménye: {}.'.format(self.dobando, self.dobott_ertekek, self.dobas_szorzo, self.bonusz, self.eredmeny)

class TulajdonsagDobas(Dobas):
    def __init__(self):
        super().__init__('4d6')
        self.dobott_ertekek.remove(min(self.dobott_ertekek))

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
