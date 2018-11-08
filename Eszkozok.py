class Fegyver:
    def __init__(self, nev, kategoria, sebzes, kritikus, hatotav, suly, ar):
        self.nev = nev
        self.kategoria = kategoria
        self.sebzes = sebzes
        self.kritikus = kritikus
        self.hatotav = hatotav
        self.suly = suly
        self.ar = ar

class Szakertelem:
    def __init__(self, nev, szak_mod, tul_mod, rank, kieg_mod):
        self.szak_nev = ""
        self.szak_mod = 0
        self.tul_mod = 0
        self.rank = 0
        self.kieg_mod = 0
        self.szak_nev = nev
        self.szak_mod = szak_mod
        self.tul_mod = tul_mod
        self.rank = rank
        self.kieg_mod = kieg_mod

class Kepesseg:
    nev = ""
    def __init__(self, nev):
        self.nev = nev

class Tamadas:
    nev = ""
    sebzes = 0
    szam = 0
    bonusz = 0
    fajta = ""
    def __init__(self):
        pass


'''
class Ero(Tulajdonsag):
    NEV = 'Erő'
    ROVID_NEV = 'Erő'
    def __init__(self):
        super().__init__('Erő', 'Erő')


    def megnovel_kozeli_tamadast(self, tamadas):
        pass

    def megnovel_sebzest(self, sebzes):
        pass

    def segit_probat(self, proba):
        pass
    def segit_eroprobat(self):
        pass

class Intelligencia(Tulajdonsag):
    NEV = 'Intelligencia'
    ROVID_NEV = 'Int'
    def __init__(self):
        super().__init__(self.NEV, self.ROVID_NEV)

class Karizma(Tulajdonsag):
    def __init__(self):
        super().__init__('Karizma', 'Kar')

class Ugyesseg(Tulajdonsag):
    def __init__(self):
        super().__init__('Ügyesség', 'Ügy')
        

class Allokepesseg(Tulajdonsag):

    NEV = 'Állóképesség'
    ROVID_NEV = 'Áll'
    def __init__(self):

        super().__init__(self.NEV, self.ROVID_NEV)

    def noveld_eletero_dobast(self, eletero):
        eletero += self.modosito

    def segits_szivossag_mentoben(self, szivossag_mento):
        szivossag_mento += 1

    def segits_osszpontositas_probaban(self):
        pass

class Bolcsesseg(Tulajdonsag):
    def __init__(self):
        super().__init__('Bölcsesség', 'Böl')
'''