

GON_FILES_ARRAY = ['abilities.gon', 'basic_attacks.gon', 'basic_movement.gon', 'butcher_abilities.gon',
'colorless_abilities.gon', 'combined.csv', 'consumable_item_abilities.gon', 'contextual_abilities.gon',
'druid_abilities.gon', 'fighter_abilities.gon', 'hunter_abilities.gon', 'jester_abilities.gon', 'mage_abilities.gon',
'medic_abilities.gon', 'misc_abilities.gon', 'monk_abilities.gon', 'necromancer_abilities.gon', 'psychic_abilities.gon',
'tank_abilities.gon', 'thief_abilities.gon', 'tinkerer_abilities.gon', 'util_abilities.gon']

class Custom_AOE:
    def __init__(self, custom_aoe:str="", custom_aoe_mirror:str="", mirror_custom_aoe:str="False", dont_orient_aoe:str="False",
                 aoe_symmetry:str="none"):
        self.custom_aoe = custom_aoe
        self.custom_aoe_mirror = custom_aoe_mirror
        self.mirror_custom_aoe = mirror_custom_aoe
        self.dont_orient_aoe = dont_orient_aoe
        self.aoe_symmetry = aoe_symmetry

class Ability_target:
    def __init__(self,name:str = "Error", range_mode:str="standard", max_aoe:str=0, min_aoe:str=0,
                 aoe_mode:str= "standard", min_range:str=0, max_range:str=0):

        self.name = name
        #aoe info
        self.target_mode = ""
        self.max_aoe = max_aoe
        self.min_aoe = min_aoe
        self.aoe_mode = aoe_mode
        self.custom_aoe = Custom_AOE()
        #range info
        self.min_range = min_range
        self.max_range = max_range
        self.range_mode = range_mode
        # fields for printing later
        self.has_aoe = 'False'
        self.has_range = 'False'
        self.is_upgrade = 'False'


def parse_ability_target_recu(ability, interest) -> bool:
    found = False

    for file in GON_FILES_ARRAY:
        #field_name = ""
        level = 0
        with open(file, mode='r', encoding='utf-8') as f_in:
            for line in f_in:
                line = line.strip()
                if line == '':
                    continue
                if "}" in line:
                    if "{" in line:
                        continue
                    level -= 1
                    if found and level == 0:
                        return True
                    continue
                split_line = line.split(" ")
                if level == 0:
                    if "{" in line:
                        if interest == split_line[0]:
                            found = True
                if found:
                    if level == 1:
                        if split_line[1] == "{":
                            field_name = split_line[0]
                            if field_name != "target":
                                continue
                        # if fam is variant recursively look for the father info
                        elif split_line[0] == "variant_of":
                            parse_ability_target_recu(ability, split_line[1])
                    elif level == 2:
                        if split_line[0] == "target_mode":
                            ability.target_mode = split_line[1]
                        elif split_line[0] == "max_aoe":
                            ability.max_aoe = int(split_line[1])
                        elif split_line[0] == "min_aoe":
                            ability.min_aoe = int(split_line[1])
                        elif split_line[0] == "aoe_mode":
                            ability.aoe_mode = split_line[1]
                        elif split_line[0] == "min_range":
                            ability.min_range = int(split_line[1])
                        elif split_line[0] == "max_range":
                            ability.max_range = int(split_line[1])
                        elif split_line[0] == "range_mode":
                            ability.range_mode = split_line[1]
                        elif split_line[0] == "aoe_symmetry":
                            ability.aoe_symmetry = split_line[1]
                        elif split_line[0] == "target_mode":
                            ability.target_mode = split_line[1]
                        elif split_line[0] == "custom_aoe":
                            if split_line[1] == "[":
                                aoe = "["
                                while line != "]":
                                    next(f_in, "")
                                    aoe += line
                                aoe += "]"
                                ability.custom_aoe = Custom_AOE(custom_aoe=aoe)
                            else:
                                ability.custom_aoe = Custom_AOE(custom_aoe=split_line[1])
                # After level processing is  done increase level
                if "{" in line:
                    level += 1
    return found


def generate_formatted_item_list()->dict[str,Ability_target]:
    ability_d = {"test": Ability_target(name="test")}

    #build the enemies, call recursion to solve inheritance
    for file in GON_FILES_ARRAY:
        at = Ability_target()
        level = 0
        with open(file, mode='r', encoding='utf-8') as f_in:
            for line in f_in:
                line = line.strip()
                if line == '':
                    continue
                if "}" in line:
                    if "{" in line:  # ignore {} in the same line (I don't care about it, and it makes bugs)
                        continue
                    level -= 1
                split_line = line.split(" ")
                if level == 0:
                    if "{" in line:
                        ability_d[at.name] = at
                        at = Ability_target(name= split_line[0])
                        parse_ability_target_recu(at, at.name)
                if "{" in line:
                    level += 1
    return ability_d

# Run the process
generate_formatted_item_list()