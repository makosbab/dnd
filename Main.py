#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import math
import Kocka
import sys
import csv
import io
import Szabalyok
import tkinter as tk
from tkinter import ttk
from collections import namedtuple
import re
#from tkinter import Tk, RIGHT, BOTH, RAISED
#from tkinter.ttk import Frame, Button, Style

REGKIF_KTAM = r'(\w+)'
REG_TAMADAS = r'(\w+) ([\+|\-]\d+) kh.'
REGKIF_DOBAS = r'(\d)?d(\d{3|4|6|8|10|20|100})(x(\d)+)?((\+|\-)\d+)'

REGKIF_SEBZES = r'(\w+)+ ' + REGKIF_DOBAS
REGKIF_JARTASSAGOK = r'(?P<nev>\w+)+ (?P<pont>[\+|\-]\d+)'
REGKIF_MENTOK = r'(?P<rovid_nev>\w+)+ (?P<pont>[\+|\-]\d+)'
REGKIF_TULAJDONSAGOK = r'(?P<rovid_nev>\w+)+ (?P<ertek>\d+|\-)'
REGKIF_VF = r'(\d+) \((\+|\-\d+) termet, (\+\d+) Ügy, (\+\d+) természetes\)'
REGKIF_ELETERO = REGKIF_DOBAS + r" \((\d+) ép\)"
REGKIF_KEZDEMENYEZES = r'(?P<modosito>\+\d+) \((?P<eredet>\w+)\)'
REGKIF_TAMADAS = r'(?P<szam>\d+) (?P<nev>[\w\s]+) (?P<bonusz>\+\d+) (?P<forma>\w+.)'
REGKIF_OLDAL_ELERES = r'(\d+) x (\d+) \/ (.+)'
MENTO_NEVEK = {
    'Szív' : 'Szívósság',
    'Gyors' : 'Gyorsaság',
    'Akarat' : 'Akaraterő',
}



csv_szorny_nevek = list()
with open("szornyek.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        csv_szorny_nevek.append(row['nev'])


# with open('szornyek.csv', 'r', encoding='utf-8') as g:
#     uj = {sor['név']}
def olvass(reg_kif, szoveg):
    print(reg_kif)
    olvasas = re.compile(reg_kif)
    talalatok = olvasas.findall(szoveg)
    return talalatok

def keress(csv_fajl, kulcs, ertek):
    with open(csv_fajl, 'r', encoding='utf-8') as csv_szornyek:
        csv_olvaso = csv.DictReader(csv_szornyek)
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

        # self.nev = Szabalyok.TULAJDONSAGOK[self.rovid_nev]
        self.ideiglenes_ertek = ideig_ertek or 0
        self.ideiglenes_modosito = ideig_mod or 0
        # self.ertek = Kocka.TulajdonsagDobas().eredmeny

        #print(self.ertek)
        #self.modosito = math.floor((self.ertek - 10 ) / 2)
    @property
    def modosito(self):
        try:
            return math.floor((self.ertek - 10 ) / 2)
        except TypeError:
            return 0

    def __str__(self):
        return '{} értéke {}, módosító: {}'.format(self.rovid_nev, self.ertek, self.modosito)


class Eletero:
    def __init__(self, e):
        r = re.match(REGKIF_ELETERO, e)
        self.teljes_eletero = int(r.group(7)) if r else 0
        self.ideig_mod = 0

class Vf:
    def __init__(self, v):
        r = re.match(REGKIF_VF, v)
        self.meret_mod = int(r.group(2)) if r else 0
        self.tul_mod = int(r.group(3)) if r else 0
        self.term_mod = int(r.group(4)) if r else 0

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

    def __str__(self):
        return '{} mentő értéke: {}'.format(self.nev, self.pont)

class Fejlesztes:
    def __init__(self, tipus):
        fejlesztes = keress('fejlesztes.csv', 'tipus', tipus)
        self.elet_kocka = fejlesztes['eletero_dobas']
        self.tamadas_bonusz = fejlesztes['tamadas_bonusz']
        self.jo_mentodobas = fejlesztes['jo_mentodobas']
        self.jartassag_pontok = fejlesztes['jartassagpontok']
        self.kepessegek = fejlesztes['kepessegek']

    def __str__(self):
        return 'életkocka: {}, tám. bón.: {}, jó mentő: {}, járt. pontok: {}, kép.: {}'.format(
            self.elet_kocka, self.tamadas_bonusz, self.jo_mentodobas, self.jartassag_pontok, self.kepessegek)

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
        return '{} {} + {} {}'.format(self.szam, self.nev, self.bonusz, self.forma)

class Sebzes:
    def __init__(self, s):
        r = re.match(REGKIF_SEBZES, s)
        self.tamadas_nev = r.group(1)
        self.dobas = r.group(2)
        self.kulonleges = r.group(3) if r.group(3) else ''

class Kepesseg(object):
    def __init__(self, nev):
        self.nev = nev
class KulonlegesKepesseg(Kepesseg):
    pass

class Jartassag(object):
    def __init__(self, nev, pont):

        self.nev = nev
        self.pont = pont

class Leny:
    def __init__(self, **kwargs):
        self.hord_fegyvert = False
        self.van_pajzsa = False
        self.van_vertezete = False
        self.nev = kwargs['nev']
        self.meret = kwargs['meret']
        self.tipus = kwargs['tipus']
        self.tipus_modosito = kwargs['tipus_modosito'] if kwargs['tipus_modosito'] else ''
        #kulcs = rövid név, érték = új tulajdonság(rövid név, hosszú név, pont)
        self.tulajdonsagok = [Tulajdonsag(**t.groupdict()) for t in re.finditer(REGKIF_TULAJDONSAGOK, kwargs['tulajdonsagok'])]

        self.eletero_dobas =  Eletero(kwargs['eletero_dobas'])
        self.kezdemenyezes = Kezdemenyezes(**re.search(REGKIF_KEZDEMENYEZES,kwargs['kezdemenyezes']).groupdict())
        self.vf = Vf(kwargs['vf'])
        self.fejlesztes = Fejlesztes(self.tipus)
        self.mentok = [Mento(**m.groupdict()) for m in re.finditer(REGKIF_MENTOK, kwargs['mentok'])]
        self.jartassagok = [Jartassag(*j.groups()) for j in re.finditer(REGKIF_JARTASSAGOK, kwargs['jartassagok'])]
        for j in self.jartassagok:
            print(j)
        self.kepessegek = kwargs['kepessegek'].split(', ')
        self.szint = re.match(REGKIF_ELETERO, kwargs['eletero_dobas']).group(1)
        self.kihivasi_ertek = int(kwargs['kihivasi_ertek'])
        self.kulonleges_tamadasok = (str.capitalize(kt) for kt in kwargs['kulonleges_tamadasok'].split(', '))
        self.kulonleges_kepessegek = (str.capitalize(kk) for kk in kwargs['kulonleges_kepessegek'].split(', '))

        OldalElteres = namedtuple('OldalElteres', 'szelesseg hosszusag tav')
        self.oldal_eleres = OldalElteres(*re.match(REGKIF_OLDAL_ELERES, kwargs['oldal_eleres']).groups())

        self.tamadasok = [Tamadas(**t.groupdict()) for t in re.finditer(REGKIF_TAMADAS, kwargs['tamadasok'])]
        self.sebzes = Sebzes(kwargs['sebzes'])

talalat = keress('szornyek.csv', 'nev', 'Aboleth')
l = Leny(**talalat)

def toltds_be(esemeny):
    # mezo_tul.config(state = 'enabled')
    for gomb in keret_tulajdonsagok.winfo_children():
        gomb.config(state='normal')


    for t in l.tulajdonsagok:
        gombok_tulajdonsagokhoz[t.rovid_nev].delete(0, "end")
        gombok_tulajdonsagokhoz[t.rovid_nev].insert(0, t.ertek)
    print('VF: {}'.format(str(l.vf.osszes)))
    for t in l.tamadasok:
        print(t)
    print(l.oldal_eleres.tav)
    mezo_vf_teljes.config(state='normal')
    mezo_vf_teljes.delete(0, "end")
    mezo_vf_teljes.insert(0, l.vf.osszes)
    print(l.tulajdonsagok[2])



gyoker = tk.Tk()
gyoker.config(background="#f1f2f6")

# class FelsoKeret(Frame):
#     def __init__(self):
#         super().__init__(relief=RAISED, borderwidth=1)
#         self.initUI()

#     def initUI(self):
#         self.master.title = 'Szörny karakterlap-készítő'
#         self.style = Style()
#         self.style.theme_use('default')

keret_felso = tk.Frame(gyoker, height=200, background="#3498db")
keret_felso.pack()
keret_tulajdonsagok = tk.LabelFrame(gyoker, text='Szörny tulajdonságai')
keret_tulajdonsagok.pack()
keret_vf = tk.LabelFrame(gyoker, text='Védelmi fokozat', background="#535c68")
keret_vf.pack()
tk.Label(keret_felso, text='Szörny neve:').pack(side=tk.LEFT)
legordulo_szorny_nevek = ttk.Combobox(keret_felso, state='readonly')
legordulo_szorny_nevek['values'] = csv_szorny_nevek
legordulo_szorny_nevek.pack(side=tk.LEFT)
tk.Label(keret_felso, text='Szörny szintje:').pack(side=tk.LEFT)
szamdoboz_szint = tk.Spinbox(keret_felso, from_ = 1, to = 99, width = 3, textvariable = 1)
szamdoboz_szint.delete(0, "end")
szamdoboz_szint.insert(0, 1)
szamdoboz_szint.pack(side=tk.LEFT)
# photo=PhotoImage(file="dice-red.png").subsample(20)
gomb_betolt = tk.Button(keret_felso, text='Betöltöm!', compound='left', relief=tk.FLAT, background='#ff6b81', fg = '#fff', padx = 40, pady = 10)
gomb_betolt.config()
gomb_betolt.bind('<Button-1>', toltds_be)
gomb_betolt.pack(side=tk.LEFT)
# Label(keret_felso, text='Szörny szintje:').pack()
class TulajdonsagMezo(ttk.Entry):
    def __init__(self, id):
        super().__init__(keret_tulajdonsagok)
        self.id = id

mezo_vf_teljes = ttk.Entry(keret_vf, state='disabled', width=3)
mezo_vf_teljes.pack()
gombok_tulajdonsagokhoz = {}
for tul in Szabalyok.TULAJDONSAGOK:
    tk.Label(keret_tulajdonsagok, text=tul[0], state='disabled').pack()
    mezo_tulajdonsag = ttk.Entry(keret_tulajdonsagok, state='disabled', width=4)
    mezo_tulajdonsag.pack()
    gombok_tulajdonsagokhoz.update({tul[0] : mezo_tulajdonsag})

gyoker.mainloop()
# C:\Selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox('geckodriver.exe')
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
