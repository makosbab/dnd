#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import Dobas
import sys
import csv
import io
import Szabalyok
import tkinter as tk
from tkinter import ttk
from collections import namedtuple
import re
# from tkinter import Tk, RIGHT, BOTH, RAISED
# from tkinter.ttk import Frame, Button, Style


REGKIF_KTAM = r'(\w+)'
REG_TAMADAS = r'(\w+) ([\+|\-]\d+) kh.'
REGKIF_DOBAS = r'(\d+)d(\d{2,3|4|6|8|10|20|100})(x(\d)+)?((\+|\-)\d+)'

REGKIF_SEBZES = r'(\w+)+ ' + REGKIF_DOBAS
REGKIF_JARTASSAGOK = r'(?P<nev>\w+)+ (?P<pont>[\+|\-]\d+)'
REGKIF_MENTOK = r'(?P<rovid_nev>\w+)+ (?P<pont>[\+|\-]\d+)'
REGKIF_TULAJDONSAGOK = r'(?P<rovid_nev>\w+)+ (?P<ertek>\d+|\-)'
REGKIF_VF = r'(\d+) \((?P<meret_mod>\+|\-\d+) termet, (?P<tul_mod>\+\d+) Ügy, (?P<term_mod>\+\d+) természetes\)'
REGKIF_ELETERO = r"(?P<dobas>\d?d\d+\+\d+) (?:\((?P<eletpont>\d+) ép\))"
REGKIF_KEZDEMENYEZES = r'(?P<modosito>\+\d+) \((?P<eredet>\w+)\)'
REGKIF_TAMADAS = r'(?P<szam>\d+) (?P<nev>[\w\s]+) (?P<bonusz>\+\d+) (?P<forma>\w+.)'
REGKIF_OLDAL_ELERES = r'(?P<szelesseg>\d+) x (?P<hosszusag>\d+) \/ (?P<tav>.+)'
REGKIF_FEJLESZTES = r'(?P<min>\d+)-(?P<max>\d+) ÉK \((?P<valtozat>\S+)\)'
MENTO_NEVEK = {
    'Szív': 'Szívósság',
    'Gyors': 'Gyorsaság',
    'Akarat': 'Akaraterő',
}
csv_szorny_nevek = list()
with open("szornyek.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        csv_szorny_nevek.append(row['nev'])


# with open('szornyek.csv', 'r', encoding='utf-8') as g:
#     uj = {sor['név']}


def keress(csv_fajl, kulcs, ertek):
    with open(csv_fajl, 'r', encoding='utf-8') as c:
        csv_olvaso = csv.DictReader(c)
        for sor in csv_olvaso:
            if sor[kulcs] == ertek:
                return sor


class Tulajdonsag(object):

    def __init__(self, rovid_nev, ertek, ideig_ertek=0, ideig_mod=0):
        self.rovid_nev = rovid_nev
        try:
            self.ertek = int(ertek)
        except ValueError:
            self.ertek = 'Nincs'
        self.ideiglenes_ertek = ideig_ertek or 0
        self.ideiglenes_modosito = ideig_mod or 0
    @property
    def modosito(self):
        try:
            return math.floor((self.ertek - 10 ) / 2)
        except TypeError:
            return 0

    def __str__(self):
        return '{} értéke {}, módosító: {}'.format(self.rovid_nev, self.ertek, self.modosito)


class Eletero(object):
    def __init__(self, **kwargs):
        self.dobas = Dobas.Dobas(kwargs['dobas'])
        self.eletpont = kwargs['eletpont']

        # self.alap_allokepesseg_mento = alap_allokepesseg_mento
        # self.ideig_mod = 0
    #
    # @property
    # def dobas(self):
    #     return self.__dobas
    #
    # @dobas.setter
    # def dobas(self, uj):
    #     self.__dobas = uj
    #
    # @property
    # def szorny_szintje(self):
    #     return self.__dobas.kocka_db
    #
    # @szorny_szintje.setter
    # def szorny_szintje(self, szint):
    #     self.__szorny_szintje = szint
    #
    # @property
    # def eletpont(self):
    #     return self.__eletpont
    #
    # @eletpont.setter
    # def eletpont(self, bonusz):
    #     self.__eletpont += bonusz


class Vf:
    def __init__(self, meret_mod, tul_mod, term_mod):
        self.meret_mod = int(meret_mod) if meret_mod else 0
        self.tul_mod = int(tul_mod) if tul_mod else 0
        self.term_mod = int(term_mod) if term_mod else 0

    @property
    def osszes(self):
        return 10 + self.meret_mod + self.tul_mod + self.term_mod

    def __str__(self):
        return 'VF:= {}, ({}, {}, {})'.format(self.osszes, self.meret_mod, self.tul_mod, self.term_mod)

class Mento:
    def __init__(self, rovid_nev, pont):
        self.rovid_nev = rovid_nev
        self.pont = pont
        self.nev = MENTO_NEVEK[self.rovid_nev]
        self.varazslat_modosito = 0
        self.kieg_modosito = 0
        self.ideiglenes_modosito = 0
        self.felteteles_modosito = 0

    def __str__(self):
        return '{} mentő értéke: {}'.format(self.nev, self.pont)


Valtozat = namedtuple('Valtozat', ['min', 'max', 'meret'])
Fejlesztes = namedtuple('Fejlesztes', ['leggyengebb_valtozat', 'legerosebb_valtozat'])


class Kezdemenyezes:
    def __init__(self, modosito, eredet):
        self.modosito = int(modosito)
        self.eredet = eredet

    def __str__(self):
        return '{} ({})'.format(self.modosito, self.eredet)


class Tamadas:
    def __init__(self, szam, nev, bonusz, forma):
        self.szam = int(szam) if szam else 1
        self.nev = nev
        self.bonusz = bonusz
        self.forma = forma

    def __str__(self):
        return '{} {} + {} {}'.format(
            self.szam,
            self.nev,
            self.bonusz,
            self.forma)


class Sebzes:
    def __init__(self, tamadas_nev, dobas, kulonleges):
        self.tamadas_nev = tamadas_nev
        self.dobas = dobas
        self.kulonleges = kulonleges


class Kepesseg(object):
    def __init__(self, nev):
        self.nev = nev
class KulonlegesKepesseg(Kepesseg):
    pass


class Jartassag(object):
    def __init__(self, nev, pont):

        self.nev = nev
        self.pont = pont


class OldalEleres(object):
    def __init__(self, szelesseg, hosszusag, tav):
        pass
        self.szelesseg = szelesseg
        self.hosszusag = hosszusag
        self.tav = tav


talalat = keress('szornyek.csv', 'nev', 'Aboleth')

def tisztit(**sor):

    def olvass(regkif, szoveg):
        olvasas = re.compile(regkif)
        talalatok = olvasas.search(szoveg)
        return talalatok.groups()

    def listaz(regex, kulcs):

        return list(
            i.groupdict() for i in re.finditer(
                regex,
                sor[kulcs]
                )
            )

    def szotaraz(regex, kulcs):
        return re.match(regex, sor[kulcs]).groupdict()

    def tordel(kulcs, kar):
        return list(
            str.capitalize(i) for i in sor[kulcs].split(kar)
            )
    # self.eletero = Eletero(
    #     # *olvass(REGKIF_ELETERO, kwargs['eletero_dobas']),
    #     self.tulajdonsagok[2].ertek,
    #     **re.search(REGKIF_ELETERO, kwargs['eletero_dobas']).groupdict(),
    #     )
    token = {}
    token['nev'] = str.strip(sor['nev'])
    token['meret'] = str.strip(sor['meret'])
    token['tipus'] = str.strip(sor['tipus'])
    token['vf'] = Vf(**szotaraz(REGKIF_VF, 'vf'))
    token['tamadasok'] = listaz(REGKIF_TAMADAS, 'tamadasok')
    token['tipus_modosito'] = str.capitalize(sor['tipus_modosito'])
    token['kezdemenyezes'] = listaz(REGKIF_KEZDEMENYEZES, 'kezdemenyezes')
    token['mentok'] = list(
        Mento(**m) for m in listaz(REGKIF_MENTOK, 'mentok')
    )
    token['eletero_dobas'] = szotaraz(REGKIF_ELETERO, 'eletero_dobas')
    token['eletpont'] = int(token['eletero_dobas']['eletpont'])
    token['szint'] = Dobas.Dobas(**Dobas.dobas_tisztits(token['eletero_dobas']['dobas'])).db_kocka
    token['jartassagok'] = listaz(REGKIF_MENTOK, 'jartassagok')
    token['kepessegek'] = tordel('kepessegek', ', ')
    token['kihivasi_ertek'] = int(sor['kihivasi_ertek'])
    token['kulonleges_tamadasok'] = tordel('kulonleges_tamadasok', ', ')
    token['kulonleges_kepessegek'] = tordel('kulonleges_kepessegek', ', ')
    token['oldal_eleres'] = szotaraz(REGKIF_OLDAL_ELERES, 'oldal_eleres')
    token['tamadasok'] = listaz(REGKIF_TAMADAS, 'tamadasok')
    token['tulajdonsagok'] = list(
        Tulajdonsag(**t) for t in listaz(REGKIF_TULAJDONSAGOK, 'tulajdonsagok')
    )
    # Valtozat = namedtuple('Valtozat', ['min', 'max', 'meret'])
    # Fejlesztes = namedtuple('Fejlesztes', ['leggyengebb_valtozat', 'legerosebb_valtozat'])

    token['fejlesztes'] = listaz(REGKIF_FEJLESZTES, 'fejlesztes')

        # Valtozat(*re.findall(REGKIF_FEJLESZTES, sor['fejlesztes'])[0]),
        # Valtozat(*re.findall(REGKIF_FEJLESZTES, sor['fejlesztes'])[1])

    return token

leny = tisztit(**talalat)
leny['hord_fegyvert'] = False
leny['van_pajzsa'] = False
leny['van_vertezete'] = False


def fejlessz(szorny):

    def noveld_eletpontot(szorny):
        elet_kocka = keress('fejlesztes.csv', 'tipus', szorny['tipus'])['eletero_dobas']        
        szorny['eletpont'] += Dobas.dobj(elet_kocka)

    def noveld_szintet(szorny):
        szorny['szint'] += 1

    print(szorny['oldal_eleres'])
    print(szorny['tamadasok'])
    print(szorny['tulajdonsagok'])
    print(szorny['tamadasok'])
    print(szorny['eletero_dobas'])
    print(szorny['eletpont'])
    noveld_eletpontot(szorny)
    print(szorny['szint'])
    noveld_szintet(szorny)
    print(szorny['eletpont'])
    print(szorny['szint'])

fejlessz(leny)
# def toltds_be(esemeny):
#     # mezo_tul.config(state = 'enabled')
#     for gomb in keret_tulajdonsagok.winfo_children():
#         gomb.config(state='normal')
#
#
#     for t in l.tulajdonsagok:
#         gombok_tulajdonsagokhoz[t.rovid_nev].delete(0, "end")
#         gombok_tulajdonsagokhoz[t.rovid_nev].insert(0, t.ertek)
#     print('VF: {}'.format(str(l.vf.osszes)))
#     for t in l.tamadasok:
#         print(t)
#     print(l.oldal_eleres.tav)
#     mezo_vf_teljes.config(state='normal')
#     mezo_vf_teljes.delete(0, "end")
#     mezo_vf_teljes.insert(0, l.vf.osszes)
#     print(l.tulajdonsagok[2])
#     print(l.eletero_dobas.szorny_szintje)
#
#
#
# # gyoker = tk.Tk()
# gyoker.config(background="#f1f2f6")
#
# # class FelsoKeret(Frame):
# #     def __init__(self):
# #         super().__init__(relief=RAISED, borderwidth=1)
#         self.initUI()

#     def initUI(self):
#         self.master.title = 'Szörny karakterlap-készítő'
#         self.style = Style()
#         self.style.theme_use('default')

# keret_felso = tk.Frame(gyoker, height=200, background="#3498db")
# keret_felso.pack()
# keret_tulajdonsagok = tk.LabelFrame(gyoker, text='Szörny tulajdonságai')
# keret_tulajdonsagok.pack()
# keret_vf = tk.LabelFrame(gyoker, text='Védelmi fokozat', background="#535c68")
# keret_vf.pack()
# tk.Label(keret_felso, text='Szörny neve:').pack(side=tk.LEFT)
# legordulo_szorny_nevek = ttk.Combobox(keret_felso, state='readonly')
# legordulo_szorny_nevek['values'] = csv_szorny_nevek
# legordulo_szorny_nevek.pack(side=tk.LEFT)
# tk.Label(keret_felso, text='Szörny szintje:').pack(side=tk.LEFT)
# szamdoboz_szint = tk.Spinbox(keret_felso, from_ = 1, to = 99, width = 3, textvariable = 1)
# szamdoboz_szint.delete(0, "end")
# szamdoboz_szint.insert(0, 1)
# szamdoboz_szint.pack(side=tk.LEFT)
# # photo=PhotoImage(file="dice-red.png").subsample(20)
# gomb_betolt = tk.Button(keret_felso, text='Betöltöm!', compound='left', relief=tk.FLAT, background='#ff6b81', fg = '#fff', padx = 40, pady = 10)
# gomb_betolt.config()
# gomb_betolt.bind('<Button-1>', toltds_be)
# gomb_betolt.pack(side=tk.LEFT)
# # Label(keret_felso, text='Szörny szintje:').pack()
# class TulajdonsagMezo(ttk.Entry):
#     def __init__(self, id):
#         super().__init__(keret_tulajdonsagok)
#         self.id = id
#
# mezo_vf_teljes = ttk.Entry(keret_vf, state='disabled', width=3)
# mezo_vf_teljes.pack()
# gombok_tulajdonsagokhoz = {}
# for tul in Szabalyok.TULAJDONSAGOK:
#     tk.Label(keret_tulajdonsagok, text=tul[0], state='disabled').pack()
#     mezo_tulajdonsag = ttk.Entry(keret_tulajdonsagok, state='disabled', width=4)
#     mezo_tulajdonsag.pack()
#     gombok_tulajdonsagokhoz.update({tul[0] : mezo_tulajdonsag})
#
# gyoker.mainloop()
