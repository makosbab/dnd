# -*- coding: utf-8 -*-

import Kocka

SZORNYEK = {
	'Alakváltó' : (
		'Aranea', 
		'Fazma',
		'Likantrópok',
		'Utánzó'
		),
	'Bestia' : (
		'Ankheg', 'Bagolymedve', 'Bulette', 'Dinoszauruszok', 'Girallon', 'Couatl'
		)
}

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
OOZE_ELETPONT_BONUSZ = dict(zip(MERETEK, (0, 0, 0, 5, 10, 15, 20, 30, 40)))
VF_TAMADAS_MODOSITO = dict(zip(MERETEK, range(8, -10, -2)))

MERETNOVEKEDES_BONUSZOK = (
    (0, -2, 0, 0, -4),
    (2, -2, 0, 0, -2),
    (4, -2, 0, 0, -1),
    (4, -2, 2, 0, -1),
    (8, -2, 4, 2, -1),
    (8, -2, 4, 3, -1),
    (8, 0, 4, 4, -2),
    (8, 0, 4, 5, -4)
    )
MERETNOVEKEDES = dict(zip(MERETEK[1:], MERETNOVEKEDES_BONUSZOK))

FEREG_NF_BONUSZ = dict(zip(MERETEK[4:], range(2, 12, 2)))

FEJLESZTES = {
    'Alakváltó' : (
        Kocka.Kocka(8),
        0.75,
        ('Szívósság', 'Gyorsaság', 'Akarat'),
        1,
        0.25
    ),
    'Állat' : (
        Kocka.Kocka(8),
        0.75,
        'Akarat',
        (10, 15),
        0
    ),
    'Bestia' : (
        Kocka.Kocka(10),
        0.75,
        ('Szívósság', 'Gyorsaság'),
        1,
        0
    ),
    'Elementál' : (
        Kocka.Kocka(8),
        0.75,
        ({
            'Föld' : 'Szívósság',
            'Víz' : 'Szívósság',
            'Levegő' : 'Gyorsaság',
            'Tűz' : 'Gyorsaság'
        }),
        2,
        0.25
    ), 
    'Élőhalott' : (
        Kocka.Kocka(8),
        0.5,
        'Szívósság',
        2,
        0.25
    ),
    'Fey' : (
        Kocka.Kocka(6),
        0.5,
        ('Gyorsaság','Akarat'),
        2,
        0
    ),
    'Féreg' : (
        Kocka.Kocka(8),
        0.5,
        'Szívósság',
        list(range(10, 13)),
        0
    ),
    'Humanoid' : (
        Kocka.Kocka(8),
        0.5,
        'random',
        1,
        0.25
    ),
    'Humanoid szörny' : (
        Kocka.Kocka(8),
        1,
        ('Gyorsaság','Akarat'),
        2,
        0.25
    ),
    'Külvilági' : (
        Kocka.Kocka(8),
        1,
        ('Szívósság', 'Gyorsaság','Akarat'),
        8,
        0.25
    ),
    'Mágikus Bestia' : (
        Kocka.Kocka(10),
        1,
        ('Szívósság', 'Gyorsaság','Akarat'),
        8,
        0.25
    ),
    'Növény' : (
        Kocka.Kocka(8),
        1,
        'Szívósság',
        0,
        0
    ),
    'Ooze' : (
        Kocka.Kocka(10),
        0.75,
        '',
        0,
        'Vaklátás'
    ),
    'Óriás' : (
        Kocka.Kocka(8),
        0.75,
        'Szívósság',
        1,
        0.25
    ),
    'Rendellenesség' : (
        Kocka.Kocka(8),
        0.75,
        'Akarat',
        2,
        0.25
    ),
    'Sárkány' : (
        Kocka.Kocka(12),
        1,
        ('Szívósság', 'Gyorsaság','Akarat'),
        6,
        0.25
    ),
    'Szerkezet' : (
        Kocka.Kocka(10),
        0.75,
        '',
        0,
        0
    )   #,'Rendellenesség' : (Kocka(8), 0.75, 'Akarat', 2, 0.25)
}
