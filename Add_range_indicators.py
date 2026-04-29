import pywikibot
from pywikibot import pagegenerators
import re
import csv
import os

from range_indicators import ability_target_gon_parser as parser


def remove_brackets(text):
    cutoff = text.find(" (")
    if cutoff != -1:
        text = text[:cutoff]
    return text

def main():
    site = pywikibot.Site()

    parsed_lib = parser.generate_formatted_item_list()

    # Define which pages to look at (e.g., all pages in Category:Example)
    cat = pywikibot.Category(site, "Spells")
    gen = pagegenerators.CategorizedPageGenerator(category=cat)
    #exclude_cat = pywikibot.Category(site, "Category:Bonus Birds")

    misc_text = ""

    with open('errors.csv', 'w') as f2:
        writer = csv.writer(f2)
        writer.writerow(["Page name", "Error"])
        i=0
        for page in gen:

            #break after i repeats for testing
            if i > 10:
                break
            #i += 1 # increment before making changes

            title = page.title()
            clean_title = remove_brackets(title)
            pywikibot.output(title)
            # if exclude_cat in page.categories():
            #     pywikibot.output(f"{title} is in excluded category")
            #     continue

            # Skip all non-info pages
            if page.isRedirectPage() or page.isDisambig() or ("MediaWiki:" in title) or (
                    "Template:" in title or "File:" in title or "/draft" in title):
                pywikibot.output(f"skipped {title}, a non-content page")
                continue

            # --- Declarations ---
            new_text = page.text
            p_text = "".join(new_text.split()).lower()
            #pywikibot.output(f"lower text:\n {p_text}")

            # --- Test conditions ---
            if "== Range ==" in new_text:
                pywikibot.output(f"{title}, already has range indicator")
                writer.writerow([title, "already has range indicator"])
                continue
            id_pattern = r"ID\s*=\s*([^}\s]+)"
            id_match = re.search(id_pattern, new_text, flags=re.IGNORECASE)
            if not id_match:
                pywikibot.output(f"{title}, no ID found")
                writer.writerow([title, "no ID found"])
                continue
            try:
                ability:parser.Ability_target = parsed_lib[id_match.group(1)]
            except KeyError:
                pywikibot.output(f"{title}, not interesting")
                writer.writerow([title, "not interesting"])
                continue

            # --- Build the new section ---
            section = "\n== Range ==\n"
            if ability.upgrade:
                if ability.upgrade.has_range:
                    section += "<tabber>\nNormal=\n"
            if ability.has_range:
                custom_range_a = ability.custom_range.custom_aoe if ability.custom_range else "none"
                custom_range_symmetry = ability.custom_range.aoe_symmetry if ability.custom_range else "none"
                if ability.has_aoe:
                    section += f"=== Range ===\n"
                section += f"<code>{ability.range_mode}</code> shape; "
                if not ability.aoe_mode == "all":
                    section += f"distance of {ability.min_range} "
                s = "" if ability.min_range == 1 else "s"
                section += f"tile{s}:" if ability.min_range == ability.max_range else f"to {ability.max_range} tiles:"
                section += f"""
{{{{RangeIndicator
| is_aoe = false
| aoe_mode = {ability.range_mode}
| target_mode = {ability.target_mode}
| min_range = {ability.min_range}
| max_range = {ability.max_range}"""
                if ability.custom_range:
                    section += f"""
| custom_aoe = {custom_range_a}
| aoe_symmetry = {custom_range_symmetry}"""
                section += f"""
}}}}
"""
            if ability.has_aoe:
                if ability.upgrade:
                    if ability.upgrade.has_aoe and not ability.upgrade.has_range:
                       section += "<tabber>\nNormal=\n"
                custom_aoe_a = ability.custom_aoe.custom_aoe if ability.custom_aoe else "none"
                aoe_symmetry_a = ability.custom_aoe.aoe_symmetry if ability.custom_aoe else "none"
                s = "" if ability.min_aoe == 1 else "s"
                section += f"=== Area Of Effect ===\n<code>{ability.aoe_mode}</code> shape; distance of {ability.min_aoe} "
                section += f"tile{s}:" if ability.min_aoe == ability.max_aoe else f"to {ability.max_aoe} tiles:"
                section += f"""
{{{{RangeIndicator
| is_aoe = true
| target_mode = {ability.target_mode}
| aoe_mode = {ability.aoe_mode}
| min_range = {ability.min_aoe}
| max_range = {ability.max_aoe}
| aoe_excludes_self = {ability.aoe_excludes_self}"""
                if ability.custom_aoe:
                    section += f"""
| custom_aoe = {custom_aoe_a}
| aoe_symmetry = {aoe_symmetry_a}"""
                section += f"""
}}}}
"""

            if ability.upgrade:
                if ability.upgrade.has_range:
                    section += "|-|\nUpgraded (+)=\n"
                    custom_range_b = ability.upgrade.custom_aoe if ability.upgrade.custom_range else "none"
                    range_symmetry_b = ability.upgrade.custom_aoe.aoe_symmetry if ability.upgrade.custom_range else "none"
                    if ability.upgrade.has_aoe:
                        section += f"=== Range ===\n"
                    section += f"<code>{ability.upgrade.range_mode}</code> shape; "
                    if not ability.aoe_mode == "all":
                        section += f"distance of {ability.upgrade.min_range} "
                    s = "" if ability.upgrade.min_range == 1 else "s"
                    section += f"tile{s}:" if ability.upgrade.min_range == ability.upgrade.max_range else f"to {ability.upgrade.max_range} tiles:"
                    section += f"""
{{{{RangeIndicator
| is_aoe = false
| target_mode = {ability.upgrade.target_mode}
| min_range = {ability.upgrade.min_range}
| max_range = {ability.upgrade.max_range}"""
                    if ability.upgrade.custom_range:
                        section += f"""
| custom_aoe = {custom_range_b}
| aoe_symmetry = {range_symmetry_b}"""
                    section += f"""
}}}}
"""
                if ability.upgrade.has_aoe:
                    if not ability.upgrade.has_range:
                        section += "|-|\nUpgraded (+)=\n"
                    custom_aoe_b = ability.upgrade.custom_aoe.custom_aoe if ability.upgrade.custom_aoe else "none"
                    aoe_symmetry_b = ability.upgrade.custom_aoe.aoe_symmetry if ability.upgrade.custom_aoe else "none"
                    s = "" if ability.upgrade.min_aoe == 1 else "s"
                    section += f"=== Area Of Effect ===\n<code>{ability.upgrade.aoe_mode}</code> shape; distance of {ability.upgrade.min_aoe} "
                    section += f"tile{s}:" if ability.upgrade.min_aoe == ability.upgrade.max_aoe else f"to {ability.upgrade.max_aoe} tiles:"
                    section += f"""
{{{{RangeIndicator
| is_aoe = true
| target_mode = {ability.upgrade.target_mode}
| aoe_mode = {ability.upgrade.aoe_mode}
| min_range = {ability.upgrade.min_aoe}
| max_range = {ability.upgrade.max_aoe}
| aoe_excludes_self = {ability.upgrade.aoe_excludes_self}"""
                    if ability.upgrade.custom_aoe:
                        section += f"""
| custom_aoe = {custom_aoe_b}
| aoe_symmetry = {aoe_symmetry_b}"""
                    section += f"""
}}}}
"""

            if ability.upgrade:
                if ability.upgrade.has_range or ability.upgrade.has_aoe:
                    section += "</tabber>\n"

            # --- insert after the Interactions section ---
            in_pattern = r"==\s*(Luck|Synergies|Interactions|Trivia)\s*=="
            in_match = re.search(in_pattern, new_text, flags=re.IGNORECASE)
            if not in_match:
                pywikibot.output(f"{title}, no Luck|Synergies|Interactions|Trivia section found")
                writer.writerow([title, "no Luck|Synergies|Interactions|Trivia section found"])
                continue
            new_text = new_text[:in_match.start()] + section + "\n" + new_text[in_match.start():]

            if page.text == new_text:
                pywikibot.output(f"Skipping {title}, unchanged")
                writer.writerow([title, "no changed made"])
                continue

            page.text = new_text
            page.save(summary="Adding range and aoe indicators.")
            i += 1 #increment after making changes


if __name__ == "__main__":
    main()
