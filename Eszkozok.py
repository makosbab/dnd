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
