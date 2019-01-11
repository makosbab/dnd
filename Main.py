#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import Dobas
import pymongo
import json
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["testdb"]
monster_collection = db["monsters"]

m = monster_collection.find_one({"name" : "Aboleth"})

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

class AdvancerSystem():
    pass


class Ability():
    pass
    
class Attributes():

    def __init__(self, entries):

        for key, value in entries.items():
            setattr(self, key, self._wrap_value(value))
        
    def _wrap_value(self, value):
        if isinstance(value, list):
            return list(self._wrap_value(v) for v in value)
        else:
            return Attributes(value) if isinstance(value, dict) else value   

    @property
    def modifier(self):
        return 2

def abmod(score):
    return math.floor(score - 10 / 2)

class Character():
    def __init__(self, attributes):
        self.__dict__ = attributes
        self.name.x 

    @property
    def ability(self):
        return self.abilities

char = Character(m)
def advance_creature(new_level, **monster):

    plus_hit_dice = new_level - int(monster["hitDice"]["numOfHitDice"])
    impr_coll =  db["improvement"]
    size_stats_coll =  db["statschangebysize"]
    hide_mod_coll = db["hidingmodifiers"]
    ooze_sizes_coll = db["oozesizes"]
    impr = impr_coll.find_one({"type" : monster["type"]})

    def count_skill_points():

        intelligence_score = int(monster["abilities"][3]["score"])
        if intelligence_score == 0 or not intelligence_score:
            return 0
           
        skill_point = impr["extraSkillPoints"]
        points_per_hd = skill_point["base"]
        
        if skill_point["modifier"]:
            points_per_hd += int(monster["abilities"][3]["modifier"])
 
        return points_per_hd * plus_hit_dice if points_per_hd > 0 else plus_hit_dice

    def update_skills():
        pass

    def grant_feats():
        feats = impr["extraFeats"]
        if feats is None:
            return 0
        if(isinstance(feats, str)):
            monster["feats"].append(feats)
            return 0

        return math.floor(feats * plus_hit_dice)

    def update_hit_dice():
        roll = Dobas.dobj("4d8+44")
        monster["hitPoints"] = roll

    def check_size_changed():
        print(monster)
        lookup = next(v for v in monster['advancement'] if new_level in range(v['hitDiceMin'],v['hitDiceMax']))
        # ha a méret megváltozott
        if lookup['version'] is not monster["size"]:
            monster["size"] = lookup["version"]
            size_stats = size_stats_coll.find_one({"newSize" : monster["size"]})
            if monster["type"] == "Ooze":
                hp_bonus = ooze_sizes_coll.find_one({"oozeSize" : monster["size"]})["hpBonus"]

            monster["abilities"][0]["score"] += int(size_stats["str"])
            if size_stats["dex"]:
                monster["abilities"][1]["score"] += int(size_stats["dex"])
            monster["abilities"][2]["score"] += int(size_stats["con"])
            monster["armorClass"]["class"] += int(size_stats["acAndAttack"])
            # this.monster.abilities[0].score += lookup.str;
            # this.monster.abilities[1].score += lookup.dex;
            # this.monster.abilities[2].score += lookup.con;
            # this.monster.armorClass.class += lookup.acAndAttack;

    def change_stats_by_size():
        pass


    #extra_skill_points = count_skill_points()
    extra_feats = grant_feats()
    #print(extra_skill_points)
    print(extra_feats)
    update_hit_dice()
    check_size_changed()
    # print(monster)
    return monster


monster = monster_collection.find_one({"name" : "Aboleth"})

for ability in monster["abilities"]:
    ability.update({"modifier" : math.floor((ability["score"] - 10) / 2)})

monster.update({"hitPoints" : monster["hitDice"]["avgHitPoints"]})
advance_creature(19, **monster)