import fileinput
from functools import cache


max_score = 1000000

move_scores = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

# Room to amphipod
r2a = ''.join(sorted(move_scores.keys()))

# Amphipod to room
a2r = {a: i for i, a in enumerate(r2a)}

num_rooms = len(r2a)

room_pos = [2 + 2 * i for i in range(num_rooms)]


def room_size(rooms):
    return len(rooms) // num_rooms


def target_rooms(rooms):
    rs = room_size(rooms)
    return ''.join([a for a in r2a for i in range(rs)])


def parse_input(lines):
    hall = '...........'
    rooms = []
    for i in [3 + 2 * i for i in range(num_rooms)]:
        for row in range(2, len(lines) - 1):
            rooms.append(lines[row][i])
    return (hall, ''.join(rooms))


def update(s, i, c):
    """Update char in the given string at the given index."""
    a = list(s)
    a[i] = c
    return ''.join(a)


def print_state(score, hall, rooms):
    print(score)
    print(hall)
    rs = room_size(rooms)
    for i in range(rs):
        print(' ', end='')
        for r in range(num_rooms):
            print('', rooms[rs * r + i], end='')
        print('')


def print_options(ops):
    for score, hall, rooms in ops:
        print()
        print_state(score, hall, rooms)


def path_len(hall, a, b):
    d = 1 if a <= b else -1
    i = a
    count = 0
    while i != b:
        if hall[i] != '.' and i != a:
            return -1
        i += d
        count += 1
    return count


def home_index(rooms, a):
    rs = room_size(rooms)
    for i in range(rs - 1, -1, -1):
        if rooms[rs * a2r[a] + i] == '.':
            return i
        if rooms[rs * a2r[a] + i] != a:
            return -1
    return -1


def hall_to_room_options(ops, hall, rooms):
    rs = room_size(rooms)
    for i, a in enumerate(hall):
        if a == '.':
            continue
        # Try target room
        home_idx = home_index(rooms, a)
        home_path_len = path_len(hall, i, room_pos[a2r[a]])
        if home_idx >= 0 and home_path_len > 0:
            home_path_len += 1 + home_idx
            hall2 = update(hall, i, '.')
            rooms2 = update(rooms, rs * a2r[a] + home_idx, a)
            ops.append((home_path_len * move_scores[a], hall2, rooms2))
    return ops


def room_to_room_options(ops, hall, rooms):
    rs = room_size(rooms)
    for i in range(num_rooms):
        for idx in range(rs):
            a = rooms[rs * i + idx]
            if a == '.':
                continue
            # Amphipod in its target room
            if a == r2a[i]:
                break
            # Try target room
            home_idx = home_index(rooms, a)
            home_path_len = path_len(hall, room_pos[i], room_pos[a2r[a]])
            if home_idx >= 0 and home_path_len > 0:
                home_path_len += 2 + idx + home_idx
                rooms2 = update(rooms, rs * i + idx, '.')
                rooms2 = update(rooms2, rs * a2r[a] + home_idx, a)
                ops.append((home_path_len * move_scores[a], hall, rooms2))
            # Process only one amphipod
            break
    return ops


def room_to_hall_options(ops, hall, rooms):
    rs = room_size(rooms)
    for i in range(num_rooms):
        for idx in range(rs):
            a = rooms[rs * i + idx]
            if a == '.':
                continue
            # Amphipod in its target room
            if a == r2a[i] and all([rooms[rs * i + j] == a
                                    for j in range(idx + 1, rs)]):
                break
            # Check hallway to the left
            for j in range(room_pos[i] - 1, -1, -1):
                if hall[j] != '.':
                    break
                if j in room_pos:
                    continue
                rooms2 = update(rooms, rs * i + idx, '.')
                hall2 = update(hall, j, a)
                hall_path_len = abs(j - room_pos[i]) + 1 + idx
                ops.append((hall_path_len * move_scores[a], hall2, rooms2))
            # Check hallway to the right
            for j in range(room_pos[i] + 1, len(hall)):
                if hall[j] != '.':
                    break
                if j in room_pos:
                    continue
                rooms2 = update(rooms, rs * i + idx, '.')
                hall2 = update(hall, j, a)
                hall_path_len = abs(j - room_pos[i]) + 1 + idx
                ops.append((hall_path_len * move_scores[a], hall2, rooms2))
            # Process only one amphipod
            break
    return ops


def options(hall, rooms):
    ops = []
    hall_to_room_options(ops, hall, rooms)
    if not ops:
        room_to_room_options(ops, hall, rooms)
    if not ops:
        room_to_hall_options(ops, hall, rooms)
    return ops


@cache
def step(hall, rooms):
    if rooms == target_rooms(rooms):
        return 0
    ops = options(hall, rooms)
    if len(ops) == 0:
        return max_score
    m = max_score
    for score, h, rs in ops:
        m = min(m, score + step(h, rs))
    return m


def run(state):
    hall, rooms = state
    # print_state(0, hall, rooms)
    # ops = options(hall, rooms)
    # print_options(ops)
    print(step(hall, rooms))


lines = list(fileinput.input())
state = parse_input(lines)
run(state)

lines.insert(3, '  #D#C#B#A#')
lines.insert(4, '  #D#B#A#C#')
state = parse_input(lines)
run(state)
