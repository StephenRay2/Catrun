# Compute next_level_exp per level for the provided leveling rule.
# Start next_level_exp at 100, req_multiplier at 0.5. Apply bracketed decrements.

next_level_exp = 100.0
req_multiplier = 0.5
levels = []
for lvl in range(1, 100):
    # exp to go from lvl to lvl+1 is current next_level_exp after applying multiplier at previous level up
    # According to code, when leveling up to new level, next_level_exp increases immediately for next level.
    # We will record the requirement to go from current level to next after performing the increment at this level-up.
    # But to list exp needed per transition, we should compute after applying growth at current level.
    # Initialize for level 1: need next_level_exp after the first growth from starting 100.
    next_level_exp = next_level_exp + next_level_exp * req_multiplier
    levels.append((lvl, next_level_exp))
    # adjust req_multiplier based on new level (lvl) as in code
    if lvl <= 20:
        req_multiplier -= 0.022
    elif lvl <= 40:
        req_multiplier -= 0.0018
    elif lvl <= 60:
        req_multiplier -= 0.0008
    elif lvl <= 80:
        req_multiplier -= 0.00008
    elif lvl < 100:
        req_multiplier -= 0.00003

for lvl, exp in levels[:50]:
    print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
print('...')
for lvl, exp in levels[50:60]:
    print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
print('...')
for lvl, exp in levels[60:90]:
    print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))
print('...')
for lvl, exp in levels[90:99]:
    print(str(lvl) + ' -> ' + str(lvl+1) + ': ' + str(exp))