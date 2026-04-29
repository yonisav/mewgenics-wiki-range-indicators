

GON_FILES_ARRAY = ['gons/necromancer_abilities.gon', 'gons/basic_attacks.gon', 'gons/basic_movement.gon', 'gons/butcher_abilities.gon',
'gons/colorless_abilities.gon', 'gons/combined.csv', 'gons/contextual_abilities.gon',
'gons/druid_abilities.gon', 'gons/fighter_abilities.gon', 'gons/hunter_abilities.gon', 'gons/jester_abilities.gon', 'gons/mage_abilities.gon',
'gons/medic_abilities.gon', 'gons/misc_abilities.gon', 'gons/monk_abilities.gon', 'gons/psychic_abilities.gon',
'gons/tank_abilities.gon', 'gons/thief_abilities.gon', 'gons/tinkerer_abilities.gon']

TEMPLATES_FILE = 'gons/ability_templates.gon'

class Custom_AOE:
    def __init__(self, custom_aoe:str="", custom_aoe_mirror:str="", mirror_custom_aoe:str="False", dont_orient_aoe:str="False",
                 aoe_symmetry:str="none"):
        self.custom_aoe = custom_aoe
        self.custom_aoe_mirror = custom_aoe_mirror
        self.mirror_custom_aoe = mirror_custom_aoe
        self.dont_orient_aoe = dont_orient_aoe
        self.aoe_symmetry = aoe_symmetry

    def __str__(self):
        return f"{self.custom_aoe=}, {self.aoe_symmetry=}"

    def __repr__(self):
        return str(self)





class Ability_target:
    def __init__(self,name:str="Error", range_mode:str="standard", max_aoe:int=0, min_aoe:int=0,
                 aoe_mode:str="standard", min_range:int=0, max_range:int=0, target_mode:str="tile",
                 orign_file:str=""):

        self.name = name
        #aoe info
        self.target_mode = target_mode
        self.max_aoe = max_aoe
        self.min_aoe = min_aoe
        self.aoe_mode = aoe_mode
        self.aoe_excludes_self = False
        self.custom_aoe:Custom_AOE = None
        #range info
        self.min_range = min_range
        self.max_range = max_range
        self.range_mode = range_mode
        self.custom_range:Custom_AOE = None
        # fields for printing later
        self.has_aoe = False
        self.has_range = False
        self.is_upgrade = False
        self.upgrade:Ability_target = None
        self. origin_file = orign_file
        self.errors = ""

        if self.name[-1] == "2":
            self.is_upgrade = True

    def __str__(self):
        return f"""name={self.name}, target_mode={self.target_mode}, max_aoe={self.max_aoe}, min_aoe={self.min_aoe}, aoe_mode={self.aoe_mode}, 
custom_aoe={self.custom_aoe}, min_range={self.min_range}, max_range={self.max_range}, range_mode={self.range_mode}, self.custom_range={self.custom_range}, 
has_aoe={self.has_aoe}, has_range={self.has_range}, is_upgrade={self.is_upgrade}\n{self.errors=}\nupgrade={self.upgrade}"""

    def __repr__(self):
        return str(self)

#Create a library of only the interesting abilities to avoid extra parsing later
#Interesting is anything with an actual indicator. This mostly filters upgrades.
def create_interesting_dictionary(file, ab_dict):
    ability_name = ""
    field_name = ""
    level = 0
    with open(file, mode='r', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            if "/*" in line and "*/" not in line:
                while "*/" not in line:
                    line = next(f_in)
            split_line = line.split(" ")
            if "}" in line:
                if "{" in line:
                    continue
                level -= 1
            if level == 0:
                if "{" in line:
                    ability_name = split_line[0]
            elif level == 1:
                if "{" in line:
                    field_name = split_line[0]
                if field_name == "target" or field_name == "template":
                    at = Ability_target(name=ability_name, orign_file=file)
                    if "2" in ability_name:
                        low_name = ability_name.split("2")[0]
                        if low_name in ab_dict:
                            ab_dict[low_name].upgrade = at
                    ab_dict[ability_name] = at
            if "{" in line:
                level += 1


def parse_ability_target_recu(ability, interest, file) -> bool:
    found = False
    level = 0
    if not file in GON_FILES_ARRAY and not file == TEMPLATES_FILE:
        print("File not found")
        return False
    with open(file, mode='r', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            if "/*" in line and "*/" not in line:
                while "*/" not in line:
                    line = next(f_in)
                line = next(f_in)
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
                    # if ability is variant recursively look for the father info
                    elif split_line[0] == "variant_of":
                        #look in the s ame file first (reduce searching for the common case of upgrades)
                        if not parse_ability_target_recu(ability, split_line[1], file):
                            for file1 in GON_FILES_ARRAY:
                                parse_ability_target_recu(ability, split_line[1], file1)
                    elif split_line[0] == "template":
                        parse_ability_target_recu(ability, "template_"+split_line[1], TEMPLATES_FILE)
                elif level == 2:
                    if field_name == "target":
                        if split_line[0] == "target_mode":
                            ability.target_mode = split_line[1]
                        elif split_line[0] == "min_aoe":
                            mina = split_line[1].split('+')[0]
                            try:
                                ability.min_aoe = int(mina)
                            except ValueError:
                                ability.min_aoe = 0
                                ability.errors += f"min aoe = {mina}, "
                        elif split_line[0] == "max_aoe":
                            maxa = split_line[1].split('+')[0]
                            try:
                                ability.max_aoe = int(maxa)
                            except ValueError:
                                if maxa == "level":
                                    ability.max_aoe = 1
                                    if ability.upgrade:
                                        ability.upgrade.max_aoe = 2
                                    else:
                                        ability.upgrade = Ability_target(max_aoe=2)
                                else:
                                    ability.max_aoe = 0
                                ability.errors += f"max aoe = {maxa}, "
                            if ability.max_aoe > 0:
                                ability.has_aoe = True
                            else:
                                ability.has_aoe = False #this needs to be done for if the ability overloads inheritance
                        elif split_line[0] == "aoe_mode":
                            ability.aoe_mode = split_line[1]
                        elif split_line[0] == "min_range":
                            minr = split_line[1].split('+')[0]
                            try:
                                ability.min_range = int(minr)
                            except ValueError:
                                ability.min_range = 0
                                ability.errors += f"min range = {minr}, "
                        elif split_line[0] == "max_range":
                            maxr = split_line[1].split('+')[0]
                            try:
                                ability.max_range = int(maxr)
                            except ValueError:
                                if maxr == "level":
                                    ability.max_range = 1
                                    if ability.upgrade:
                                        ability.upgrade.max_range = 2
                                    else:
                                        ability.upgrade = Ability_target(max_range=2)
                                else:
                                    ability.max_range = 0
                                ability.errors += f"max range = {maxr}, "
                            if ability.max_range > 0:
                                ability.has_range = True
                            else:
                                ability.has_range = False #this needs to be done for if the ability overloads inheritance
                        elif split_line[0] == "range_mode":
                            ability.range_mode = split_line[1]
                        elif split_line[0] == "aoe_symmetry":
                            if ability.custom_aoe:
                                ability.custom_aoe.aoe_symmetry = split_line[1]
                            else:
                                ability.custom_aoe = Custom_AOE(aoe_symmetry=split_line[1])
                        elif split_line[0] == "target_mode":
                            ability.target_mode = split_line[1]
                        elif split_line[0] == "custom_aoe":
                            ability.has_aoe = True
                            if not "]" in line:
                                aoe = ""
                                while line != "]":
                                    line = next(f_in).strip()
                                    if line == "]":
                                        aoe = aoe[:-2]
                                    else:
                                        aoe += line + ", "
                                if ability.custom_aoe:
                                    ability.custom_aoe.custom_aoe = aoe
                                else:
                                    ability.custom_aoe = Custom_AOE(custom_aoe=aoe)
                            else:
                                ca_index = line.find("[")+1
                                aoe = line[ca_index:-1]
                                if ability.custom_aoe:
                                    ability.custom_aoe.custom_aoe = aoe
                                else:
                                    ability.custom_aoe = Custom_AOE(custom_aoe=aoe)
                        elif split_line[0] == "custom_range":
                            ability.has_range = True
                            if not "]" in line:
                                r_aoe = ""
                                while line != "]":
                                    line = next(f_in).strip()
                                    if line == "]":
                                        r_aoe = r_aoe[:-2]
                                    else:
                                        r_aoe += line + ", "
                                if ability.custom_range:
                                    ability.custom_range.custom_aoe = aoe
                                else:
                                    ability.custom_range = Custom_AOE(custom_aoe=aoe)
                            else:
                                ca_index = line.find("[") + 1
                                aoe = line[ca_index:-1]
                                if ability.custom_range:
                                    ability.custom_range.custom_aoe = aoe
                                else:
                                    ability.custom_range = Custom_AOE(custom_aoe=aoe)


            # After level processing is  done increase level
            if "{" in line:
                level += 1

    return found


def generate_formatted_item_list()->dict[str,Ability_target]:
    ability_d:dict[str,Ability_target] = {}
    ability_dp: dict[str, Ability_target] = {}
    i = 0 #for testing
    #build the enemies, call recursion to solve inheritance
    with (open("abilities.txt", mode='w', encoding='utf-8') as f_out):
        for file in GON_FILES_ARRAY:
            # i = i + 1
            if i > 3:
                break
            create_interesting_dictionary(file, ability_d)

        #Fill the values
        for ability in ability_d.keys():
            if not parse_ability_target_recu(ability_d[ability], ability, ability_d[ability].origin_file):
                print("this shouldn't happen")

        #filter out uninteresting values
        for ability in ability_d.keys():

            # Direction overrides the range
            if ability_d[ability].target_mode == "direction":
                ability_d[ability].has_range = True
                ability_d[ability].range_mode = "cross"
                ability_d[ability].min_range = ability_d[ability].min_aoe
                ability_d[ability].max_range = ability_d[ability].max_aoe

            # All overrides the range
            if ability_d[ability].target_mode == "direction":
                ability_d[ability].has_range = False

            # if upgrade is identical, remove it
            if ability_d[ability].upgrade:
                if (ability_d[ability].max_range == ability_d[ability].upgrade.max_range
                    and ability_d[ability].min_range == ability_d[ability].upgrade.min_range
                    and ability_d[ability].max_aoe == ability_d[ability].upgrade.max_aoe
                    and ability_d[ability].min_aoe == ability_d[ability].upgrade.min_aoe
                    and ability_d[ability].custom_aoe == ability_d[ability].upgrade.custom_aoe
                    and ability_d[ability].custom_range == ability_d[ability].upgrade.custom_range):
                    ability_d[ability].upgrade = None

            #Don't copy upgrades
            if ability_d[ability].is_upgrade:
                continue

            # copy the interesting values to a new dict
            if (ability_d[ability].has_range or ability_d[ability].has_aoe or ability_d[ability].custom_aoe
                or ability_d[ability].custom_range):
                ability_dp[ability] = ability_d[ability]
            elif ability_d[ability].upgrade:
                if (ability_d[ability].upgrade.has_range or ability_d[ability].upgrade.has_aoe
                        or ability_d[ability].upgrade.custom_aoe or ability_d[ability].custom_range):
                    ability_dp[ability] = ability_d[ability]

        # Print to file for debugging
        for ability in ability_dp.keys():
            f_out.write(f"{ability_dp[ability]}\n")
            if ability_dp[ability].custom_aoe:
                f_out.write(f"{ability_dp[ability].name} custom_aoe={ability_dp[ability].custom_aoe}\n")
            if ability_dp[ability].custom_range:
                f_out.write(f"{ability_dp[ability].name} custom_range={ability_dp[ability].custom_range}\n")


    return ability_dp

# Run the process
generate_formatted_item_list()
