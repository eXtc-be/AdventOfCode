from collections import deque

def get_points(values):
    ret = []
    for cur in values:
        ret.append([int(x) for x in cur.split(",")])
    return ret


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


def calc(values):
    points = get_points(values)

    ret = 0
    all_used = set()
    constellations = []

    while True:
        used = set()
        to_check = deque()
        for i in range(len(points)):
            if i not in all_used:
                to_check.append(i)
                break

        while len(to_check) > 0:
            cur = to_check.popleft()
            used.add(cur)
            all_used.add(cur)
            for i in range(len(points)):
                if i not in used and i not in all_used:
                    if dist(points[i], points[cur]) <= 3:
                        to_check.append(i)

        if len(used) == 0:
            break
        ret += 1
        constellations.append(used)

    return ret, constellations


test_data = [
'''
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
'''.strip().splitlines(),  # 2
'''
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
'''.strip().splitlines(),  # 2
'''
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
'''.strip().splitlines(),  # 4
'''
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
'''.strip().splitlines(),  # 3
'''
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
'''.strip().splitlines()  # 8
]


# print(calc(test_data[3]))
print(calc(open('./input_2018_25').read().splitlines()))
