<includeonly><!-- Var declare
-->{{#vardefine:is_aoe|{{{is_aoe|false}}} }}<!--
-->{{#vardefine:target_mode|{{{target_mode|Tile}}} }}<!-- tile, direction, none
-->{{#vardefine:aoe_mode| {{{aoe_mode|standard}}} }}<!-- standard, line, cross, 8cross, cone, all, occupied_tiles, square, circle, perpline, narrow_cone, diagcross, custom
-->{{#vardefine:min_range|{{{min_range|0}}} }}<!--
-->{{#vardefine:max_range|{{{max_range|0}}} }}<!--
-->{{#vardefine:aoe_excludes_self|{{{aoe_excludes_self|false}}} }}<!--
-->{{#vardefine:custom_aoe|{{{custom_aoe|none}}} }}<!--
-->{{#vardefine:aoe_symmetry|{{{aoe_symmetry|none}}} }}<!--
-->{{#vardefine:is_warn|{{{is_warn|false}}} }}<!-- for ! indicator

--><templatestyles src="RangeIndicator/styles.css" /><div class="{{{class|}}}" {{#if:{{{cell_size|}}}|style="--shape-cell-size-override: {{{cell_size|16px}}}|}};">{{#invoke:RangeIndicator
| render
| is_aoe={{#var:is_aoe}}
| target_mode={{#var:target_mode}}
| aoe_mode={{#var:aoe_mode}}
| min_range={{#var:min_range}}
| max_range={{#var:max_range}}
| aoe_excludes_self={{#var:aoe_excludes_self}}
| custom_aoe = {{#var:custom_aoe}}
| aoe_symmetry = {{#var:aoe_symmetry}}
| is_warn = {{#var:is_warn}}
}}</div><!--
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
| is_warn = <!-- For warning indicator (!) -->

| cell_size = <!-- Adjust the default cell size. Default: 16px -->
| class = <!-- Add a custom css class. Presumably using [[Template:RangeIndicator/styles.css]]. -->
}}
</syntaxhighlight>

Supports the following target_modes: <code>tile, none</code><!-- TODO: direction,  -->

Supports the following aoe_modes: <code>standard, line, cone, cross,  diagcross, 8cross, perpline, all, square, circle, custom  <!-- TODO:  occupied_tiles, --></code>

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
| cell_size = 12px
}}</syntaxhighlight>
{{RangeIndicator
| is_aoe = false
| min_range = 3
| max_range = 6
| cell_size = 12px
}}[[Category:Templates]][[Category: Templates using GridShape]]</noinclude>
