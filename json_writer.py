import json
temp = 'cooking time + 45 minutes'
solution = [int(s) for s in temp.split() if s.isdigit()]

print(solution)