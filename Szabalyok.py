# -*- coding: utf-8 -*-

import Dobas

TULAJDONSAGOK = (
	('Erő', 'Erő'),
	('Áll','Állóképesség'),
	('Ügy','Ügyesség'),
	('Int', 'Intelligencia'),
	('Kar', 'Karizma'),
	('Böl','Bölcsesség')

	)
TIPUSOK = ('Alakváltó', 'Állat', 'Bestia', 'Elementál', 'Élőholt', 'Féreg', 'Fey', 'Humanoid', 'Humanoid szörny', 'Külvilági', 'Mágikus bestia', 'Növény', 'Ooze', 'Óriás', 'Rendellenesség', 'Sárkány', 'Szerkezet')
ALTIPUSOK = ('Fagy', 'Testetlen', 'Tűz')
MERETEK = ('Apró','Pöttöm','Pici','Kicsi','Közepes','Nagy','Óriási','Hatalmas','Gigászi')
# OOZE_ELETPONT_BONUSZ = dict(zip(MERETEK, (0, 0, 0, 5, 10, 15, 20, 30, 40)))
# VF_TAMADAS_MODOSITO = dict(zip(MERETEK, range(8, -10, -2)))
#
# MERETNOVEKEDES_BONUSZOK = (
#     (0, -2, 0, 0, -4),
#     (2, -2, 0, 0, -2),
#     (4, -2, 0, 0, -1),
#     (4, -2, 2, 0, -1),
#     (8, -2, 4, 2, -1),
#     (8, -2, 4, 3, -1),
#     (8, 0, 4, 4, -2),
#     (8, 0, 4, 5, -4)
#     )
# MERETNOVEKEDES = dict(zip(MERETEK[1:], MERETNOVEKEDES_BONUSZOK))

FEREG_NF_BONUSZ = dict(zip(MERETEK[4:], range(2, 12, 2)))
