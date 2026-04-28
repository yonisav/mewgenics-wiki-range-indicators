<includeonly><!--
-->[<span style="color: var(--wiki-content-link-color) "><span role="button" class="mw-customtoggle-{{{name|sectionName}}}><u>View Range</u></span></span>]
<div class="mw-collapsible mw-collapsed" id="mw-customcollapsible-{{{name|sectionName}}}">
{{{1|"Your Content Here"}}}
</div><!--
--></includeonly><noinclude>
This template is meant to be used with [[Template:RangeIndicator]], used to hide away range where it could be too intrusive. It should be used in line with the text.
<syntaxhighlight lang=wikitext>
{{RangeIndicator
| name = <!-- Section name, needs to be different or the same button will open multiple sections -->
| <!-- unnamed, the cotent --> 
}}
</syntaxhighlight>
== Example ==
empty {{RangeIndicatorWrapper}}
Puke Shot {{RangeIndicatorWrapper|name=puke|{{RangeIndicator
| target_mode = none
| aoe_mode = custom
| aoe_symmetry = eight_way
| custom_aoe = [1 1] [2 2] [3 3] [4 4] [5 5] [6 6] [7 7] [8 8] [9 9] [1 2] [2 3] [3 4] [4 5] [5 6] [6 7] [7 8] [8 9] 
| is_aoe = true
| is_warn = true
}}}}

see: [[Crater Maker]]
