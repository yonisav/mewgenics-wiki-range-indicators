{{RangeIndicator
| aoe_mode = test
| custom_aoe = 0 1 2 3 4 5 6 7 8 9;10 11 12 13 14 15 16 17 18 19
}}


cross
{{RangeIndicator
| is_aoe = false
| target_mode = direction
| aoe_mode = cross
| min_range = 1
| max_range = 3
}}


diagcross
{{RangeIndicator
| aoe_mode = diagcross
| min_range = 0
| max_range = 3
}}


8cross
{{RangeIndicator
| is_aoe = false
| target_mode = direction
| aoe_mode = 8cross
| min_range = 0
| max_range = 4
}}


perpline
{{RangeIndicator
| is_aoe = true
| aoe_mode = perpline
| min_range = -10
| max_range = 10
}}


line
{{RangeIndicator
| is_aoe = true
| aoe_mode = line
| min_range = 1
| max_range = 3
}}


circle
{{RangeIndicator
| is_aoe = true
| aoe_mode = circle
| min_range = 0
| max_range = 2
}}

{{RangeIndicator
| is_aoe = true
| aoe_mode = circle
| min_range = 3
| max_range = 5
}}


square
{{RangeIndicator
| is_aoe = true
| aoe_mode = square
| min_range = 0
| max_range = 1
}}

{{RangeIndicator
| is_aoe = false
| aoe_mode = square
| min_range = 2
| max_range = 5
}}


standard
{{RangeIndicator
| min_range = 0
| max_range = 15
}}

{{RangeIndicator
| min_range = 0
| max_range = 10
}}

{{RangeIndicator
| min_range = 0
| max_range = 8
}}


custom
{{RangeIndicator
| is_aoe = false
| aoe_mode = custom
| custom_aoe = [-2 0] [-2 -1] [-1 -2] [0 -2] [-1 1] [0 1] [1 0] [1 -1]
}}

{{RangeIndicator
| is_aoe = true
| aoe_mode = custom
| custom_aoe = [[0 0] [1 0] [0 1] [1 1]]
}}


{{RangeIndicator
| target_mode = none
| aoe_mode =  custom
| custom_aoe = [1, 1]
| aoe_symmetry = four_way
}}

{{RangeIndicator
| target_mode = none
| aoe_mode =  custom
| custom_aoe = [1, 1] [1, 0]
| aoe_symmetry = four_way
}}

{{RangeIndicator
| target_mode = none
| aoe_mode = custom
| aoe_symmetry = eight_way
| custom_aoe = [1 1] [2 2] [3 3] [4 4] [5 5] [6 6] [7 7] [8 8] [9 9] [1 2] [2 3] [3 4] [4 5] [5 6] [6 7] [7 8] [8 9] 
}}


test
{{RangeIndicator
| aoe_mode = test
| custom_aoe = 16 16 16 16 16 16 16 16 16 13 13 13 16 16 16 16 16 16 16 16 16;16 16 16 16 16 16 16 16 16 13 13 13 16 16 16 16 16 16 16 16 16;16 16 16 16 16 16 16 16 16 13 13 13 16 16 16 16 16 16 16 16 16
}}
