#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import Dobas
import pymongo
import re
import inflection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["testdb"]
monster_collection = db["monsters"]



camel_pat = re.compile(r'([A-Z])')
def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

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
    
    COLLECTION_IMPROV =  db["improvement"]
    COLLECTION_STATS_BY_SIZE =  db["statschangebysize"]
    COLLECTION_HIDE_MOD = db["hidingmodifiers"]
    COLLECTION_OOZE = db["oozesizes"]

    def __init__(self):
        self.char = None
        self.impr_by_type = None
        self.to_level = 0
        self.plus_hd = 0

    def load_character(self, char):
        self.char = char
        self.impr_by_type = self.COLLECTION_IMPROV.find_one({"type" : self.char.type})
        print(self.impr_by_type)
    

    @property
    def new_skill_points(self):
        if self.char.int_mod == 0 or not self.char.int_mod:
            return 0
            # return self.impr_by_type["extraSkillPoints"]["base"] * self.plus_hd if self.impr_by_type["base"] > 0 else plus_hd
        return self.impr_by_type["extraSkillPoints"]["base"] * self.plus_hd

    @property
    def new_feats(self):

        feats = self.impr_by_type["extraFeats"]
        if feats is None:
            return 0
        if(isinstance(feats, str)):
            self.char.feats.append(feats)
            return 0

        return math.floor(feats * self.plus_hd)

    def advance_character(self, to_level):

        self.plus_hd = to_level - int(self.char.hit_dice["count"])
        self.update_hit_dice()
        self.check_size_changed()

            
    def update_skills():
        pass


    def update_hit_dice(self):
        roll = Dobas.dobj("4d8+44")
        self.char.hit_points = roll

    def check_size_changed(self):
        print(self.char.advancement)
        lookup = next(v for v in self.char.advancement if self.to_level in range(v['rangeMin'],v['rangeMax']))
        # ha a méret megváltozott
        if lookup['version'] is not self.char.size:
            self.char.size = lookup["version"]
            size_stats = self.COLLECTION_STATS_BY_SIZE.find_one({"newSize" : self.char.size})
            if self.char.type == "Ooze":
                hp_bonus = self.COLLECTION_OOZE.find_one({"oozeSize" : self.char.size})["hpBonus"]

            self.char.str += int(size_stats["str"])
            if size_stats["dex"]:
                self.char.dex += int(size_stats["dex"])
            self.char.con += int(size_stats["con"])
            self.char.armor_class["class"] += int(size_stats["acAndAttack"])
            # this.char.abilities[0].score += lookup.str;
            # this.char.abilities[1].score += lookup.dex;
            # this.char.abilities[2].score += lookup.con;
            # this.char.armorClass.class += lookup.acAndAttack;

    def change_stats_by_size():
        pass

        # extra_feats = grant_feats()
        # print(extra_feats)
        # update_hit_dice()
        # check_size_changed()
        

    
def set_attribute_modifier(score):
    return math.floor((score - 10) / 2)

class Character():
    def __init__(self, attributes):

        self.__dict__ = {inflection.underscore(k) : v for k, v in attributes.items()}
        # alphabet =  {k.lower(): v for k, v in alphabet.items()}

    @property
    def str_mod(self):
        print(self.__dict__)
        return set_attribute_modifier(self.str)

    @property
    def dex_mod(self):
        return set_attribute_modifier(self.dex)

    @property
    def con_mod(self):
        return set_attribute_modifier(self.con)

    @property
    def wis_mod(self):
        return set_attribute_modifier(self.wis)

    @property
    def char_mod(self):
        return set_attribute_modifier(self.char)

    @property
    def int_mod(self):
        return set_attribute_modifier(self.int)

    @property
    def base_att_mod(self):
        pass

    @property
    def melee_att_mod(self):
        attack_size_mod = monster_collection.find_one({"size" : self.size})["AttackAndAcMod"]
        return self.base_att_mod + self.str_mod + attack_size_mod

    @property
    def ranged_att_mod(self):
        attack_size_mod = monster_collection.find_one({"size" : self.size})["AttackAndAcMod"]
        return self.base_att_mod + self.dex_mod + attack_size_mod
    # monster.attackModifierMelee = monster.baseAttackModifier() + monster.abilities[0].modifier + sizeModifiers[5].sizeModifier;


def main():
    m = monster_collection.find_one({"name" : "Aboleth"})
    char = Character(m)
    ad = AdvancerSystem()
    ad.load_character(char)
    ad.advance_character(19)
if __name__ == "__main__":
    main()



