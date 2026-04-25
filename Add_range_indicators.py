import pywikibot
from pywikibot import pagegenerators
import re
import csv
import os

from pywikibot.date import pattern
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
    cat = pywikibot.Category(site, "Yosa test")
    gen = pagegenerators.CategorizedPageGenerator(category=cat)
    #exclude_cat = pywikibot.Category(site, "Category:Bonus Birds")

    misc_text = ""

    with open('errors.csv', 'w') as f2:
        writer = csv.writer(f2)
        writer.writerow(["Page name", "Error"])
        i=0
        for page in gen:

            #break after i repeats for testing
            if i > 1:
                break
            i += 1 # increment before making changes

            title = page.title()
            clean_title = remove_brackets(title)
            pywikibot.output(title)
            # if exclude_cat in page.categories():
            #     pywikibot.output(f"{title} is in excluded category")
            #     continue

            # Skip all non-info pages
            if page.isRedirectPage() or page.isDisambig() or ("MediaWiki:" in title) or (
                    "Template:" in title or "File:" in title or "/" in title):
                pywikibot.output(f"skipped {title}, a non-content page")
                continue

            # --- Declarations ---
            new_text = page.text
            p_text = "".join(new_text.split()).lower()
            #pywikibot.output(f"lower text:\n {p_text}")

            # --- Test conditions ---
            if "== Range indicator ==" in new_text:
                pywikibot.output(f"{title}, already has range indicator")
                writer.writerow([title, "already has range indicator"])
                continue
            id_pattern = "\|\s*ID\s*=\s*(.*)"
            id_match = re.search(id_pattern, new_text, flags=re.IGNORECASE)
            if not id_match:
                pywikibot.output(f"{title}, no ID found")
                writer.writerow([title, "no ID found"])
                continue
            ability:parser.Ability_target = parsed_lib[id_match.group()]


            # --- Build the new section ---
            section = "\n== Range indicators ==\n"
            if ability.upgrade:
                section += "<tabber>\nNormal=\n"
            if ability.has_range:
                section += f"""=== Range ===
'''Range''' indicator for distance of {ability.min_range}" to {ability.max_range}.
{{{{RangeIndicator
| is_aoe = false
| target_mode= {ability.target_mode}
| min_range = {ability.min_range}
| max_range = {ability.max_range}
| custom_aoe = {ability.custom_range}
"""
            if ability.has_aoe:
                    section += f"""=== Area Of Effect ===
{ability.aoe_mode} shaped '''AOE''' indicator for distance of {ability.min_aoe}" to {ability.max_aoe}.
{{{{RangeIndicator
| is_aoe = true
| target_mode = {ability.target_mode}
| aoe_mode = {ability.aoe_mode}
| min_range = {ability.min_aoe}
| max_range = {ability.max_aoe}
| aoe_excludes_self = {ability.aoe_excludes_self}
| custom_aoe = {ability.custom_aoe}
"""
            if ability.upgrade:
                section += "|-|\n(+)Upgraded=\n"
                if ability.upgrade.has_range:
                    section += f"""=== Range ===
'''Range''' indicator for distance of {ability.upgrade.min_range}" to {ability.upgrade.max_range}.
{{{{RangeIndicator
| is_aoe = false
| target_mode={ability.upgrade.target_mode}
| min_range ={ability.upgrade.min_range}
| max_range ={ability.upgrade.max_range}
| custom_aoe = {ability.upgrade.custom_range}
"""
                if ability.upgrade.has_aoe:
                    section += f"""=== Area Of Effect ===
{ability.upgrade.aoe_mode} shaped '''AOE''' indicator for distance of {ability.upgrade.min_aoe}" to {ability.upgrade.max_aoe}.
{{{{RangeIndicator
| is_aoe = true
| target_mode = {ability.upgrade.target_mode}
| aoe_mode = {ability.upgrade.aoe_mode}
| min_range = {ability.upgrade.min_aoe}
| max_range = {ability.upgrade.max_aoe}
| aoe_excludes_self = {ability.upgrade.aoe_excludes_self}
| custom_aoe = {ability.upgrade.custom_aoe}
"""

            if ability.upgrade:
                section += "<\\tabber>\n"

            # --- insert after the Interactions section ---
            in_pattern = "== ?(Interactions)?(Synergies)? ?=="
            in_match = re.search(in_pattern, new_text, flags=re.IGNORECASE)
            if not in_match:
                pywikibot.output(f"{title}, no interaction/synergy section found")
                writer.writerow([title, "no interaction/synergy section found"])
                continue
            new_text = new_text[:in_match.end()] + section + new_text[in_match.end():]

            if page.text == new_text:
                pywikibot.output(f"Skipping {title}, unchanged")
                writer.writerow([title, "no changed made"])
                continue

            page.text = new_text
            page.save(summary="Adding range and aoe indicators.")
            #i += 1 #increment after making changes


if __name__ == "__main__":
    main()
