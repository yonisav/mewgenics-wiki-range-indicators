<includeonly><!-- Var declare
-->{{#vardefine:is_aoe|{{{is_aoe|false}}} }}<!--
-->{{#vardefine:target_mode|{{{target_mode|Tile}}} }}<!-- tile, direction, none
-->{{#vardefine:aoe_mode| {{{aoe_mode|standard}}} }}<!-- standard, line, cross, 8cross, cone, all, occupied_tiles, square, circle, perpline, narrow_cone, diagcross, custom
-->{{#vardefine:min_range|{{{min_range|0}}} }}<!--
-->{{#vardefine:max_range|{{{max_range|0}}} }}<!--
-->{{#vardefine:aoe_excludes_self|{{{aoe_excludes_self|false}}} }}<!--
-->{{#vardefine:custom_aoe|{{{custom_aoe|none}}} }}<!--
-->{{#vardefine:aoe_symmetry|{{{aoe_symmetry|none}}} }}<!--


--><templatestyles src="RangeIndicator/styles.css"/>{{#invoke:RangeIndicator
| render
| is_aoe={{#var:is_aoe}}
| target_mode={{#var:target_mode}}
| aoe_mode={{#var:aoe_mode}}
| min_range={{#var:min_range}}
| max_range={{#var:max_range}}
| aoe_excludes_self={{#var:aoe_excludes_self}}
| custom_aoe = {{#var:custom_aoe}}
| aoe_symmetry = {{#var:aoe_symmetry}}
}}<!--
--></includeonly><noinclude>
== Usage ==
<syntaxhighlight lang=wikitext>
{{RangeIndicator
| is_aoe = <!-- for range or aoe indicator  Default: False (Range) -->
| target_mode =  <!-- who this targets  Default: None -->
| aoe_mode = <!-- one of several preprogrammed shapes or custom Default: Standard--> 
| min_range = <!-- default: 0 -->
| max_range = <!-- default: 0 -->
| aoe_excludes_self = <!-- default: False (include self)-->
| aoe_symmetry = <!-- for custom aoe, multiply by 4 or 8 ways -->
}}
</syntaxhighlight>

<!-- TODO: Supports the following target_modes: <code>tile, direction, none</code> -->

Supports the following aoe_modes: <code>standard, line, cone, cross, perpline, diagcross, <!-- TODO:8cross, all, occupied_tiles, square, circle,  custom --></code>

== Example ==
Mage spell: {{a|Mega Blast}}

<syntaxhighlight lang=wikitext>{{RangeIndicator
| is_aoe = true
| target_mode = direction
| aoe_mode = cone
| min_range = 1
| max_range = 3
| aoe_excludes_self = true
}}</syntaxhighlight>
{{RangeIndicator
| is_aoe = true
| target_mode = direction
| aoe_mode = cone
| min_range = 1
| max_range = 3
| aoe_excludes_self = true
}}

Hunter spell: {{a|Scatter Shot}} (range indicator)

<syntaxhighlight lang=wikitext>{{RangeIndicator
| is_aoe = false
| min_range = 3
| max_range = 6
}}</syntaxhighlight>
{{RangeIndicator
| is_aoe = false
| min_range = 3
| max_range = 6
}}[[Category:Templates]][[Category: Templates using GridShape]]</noinclude>
