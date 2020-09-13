from random import randint
import re
from itertools import repeat
import json

class RollMultiple:
    def __init__(self, roll_string, number_rolls, drop_type=None, number_drops=1):
        if roll_string:
            if number_rolls and int(number_rolls) > 1:
                self.roll_results = [Roll(roll_string) for _ in repeat(None, int(number_rolls))]
                if drop_type:
                    drop_func = max if drop_type == 'H' else min
                    self.droppedResults = []
                    for _ in repeat(None, int(number_drops)):
                        drop_value = drop_func(map(lambda x: x.result, self.roll_results))
                        drop_roll = next((x for x in self.roll_results if x.result == drop_value))
                        self.droppedResults.append(drop_roll)
                        self.roll_results.remove(drop_roll)
                self.result = list(map(lambda x: x.result, self.roll_results))
    
    def to_json(self):
        return json.dumps(self, default=serialize)

class Roll:
    def __init__(self, roll_string):
        self.roll_string = roll_string.strip().replace(' ','')
        self.rolls = []
        self.breakdown=''
        self.result = self.__parse_roll(roll_string)

    def __repr__(self):
        return f"=========================\nRolled {self.roll_string} for a result of {self.result}\nRolls: {self.rolls}\nFinal: {self.breakdown}\n========================="

    def __parse_roll(self, roll_string):
        self.breakdown = re.sub(r'((\d*)d(\d+))?((H|L)(.))?', self.__roll_section, self.roll_string)
        return eval(self.breakdown)
    
    def __roll_section(self, section):
        if (section.groups()[1] is None):
            return ''
        roll_section = RollSection(*section.groups())
        self.rolls.append(roll_section)
        return str(roll_section.value)

    def to_json(self):
        return json.dumps(self, default=serialize)



class RollSection:
    def __init__(self, roll_string_section, number_rolls, dice_type, drop_rule, drop_type="H", drop_num=0):
        self.roll_string_section = roll_string_section
        self.number_rolls = int(number_rolls or 1)
        self.dice_type = int(dice_type or 0)
        self.drop_rule = drop_rule
        self.drop_num = int(drop_num or 0)
        self.drop_type_func = max if drop_type == "H" else min
        self.rolls = []
        self.dropped = []
        self.value = self.__roll()
    
    def __repr__(self):
        if(self.roll_string_section is not None):
            return f"\n\t{self.roll_string_section} => {self.rolls} (dropped:{self.dropped})"
        return ''

    def __roll(self):
        if(self.roll_string_section):
            for _ in repeat(None, self.number_rolls):
                roll = randint(1,int(self.dice_type))
                self.rolls.append(roll)
            if (self.drop_rule is not None):
                for _ in repeat(None, self.drop_num):
                    dropped_roll = self.drop_type_func(self.rolls)
                    self.dropped.append(dropped_roll)
                    self.rolls.remove(dropped_roll)
            return sum(self.rolls)
        return ''


def serialize(obj):
    if (not callable(obj)):
        return obj.__dict__