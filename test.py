import random
# hearts = {
# 	2: [12,6, -5]
# }

# hearts[1] = -5

# print(hearts)

# hearts.update({1: [13, 14, 5]})

hearts = [[[12, 13], 5],[[14, 15], -5]]
vels = [5, -5]

for h in hearts:
	print(h[0][1])