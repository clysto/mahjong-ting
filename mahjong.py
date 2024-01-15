from copy import deepcopy
import pickle
from pathlib import Path
import re


SUITS = "条饼万东西南北中发白"
NUMS = "一二三四五六七八九"
TILES_UNICODE = [
    ["🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"],
    ["🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"],
    ["🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"],
    ["🀀"],
    ["🀂"],
    ["🀁"],
    ["🀃"],
    ["🀄"],
    ["🀅"],
    ["🀆"],
]
TILES_TEXT = [
    ["一条", "二条", "三条", "四条", "五条", "六条", "七条", "八条", "九条"],
    ["一饼", "二饼", "三饼", "四饼", "五饼", "六饼", "七饼", "八饼", "九饼"],
    ["一万", "二万", "三万", "四万", "五万", "六万", "七万", "八万", "九万"],
    ["东"],
    ["西"],
    ["南"],
    ["北"],
    ["中"],
    ["发"],
    ["白"],
]


def hand_count(hand):
    return sum(sum(s) for s in hand)


def print_hand(hand, unicode=False, end="\n"):
    for s in range(10):
        for rank, count in enumerate(hand[s]):
            for _ in range(count):
                if unicode:
                    print(TILES_UNICODE[s][rank], end=" ")
                else:
                    print(TILES_TEXT[s][rank], end=" ")
    print()


def parse_hand(str):
    tiles = re.split(r"\s+", str.strip())
    hand = [[0] * 9 for _ in range(10)]
    for tile in tiles:
        if len(tile) == 1:
            s = SUITS.index(tile)
            hand[s][0] += 1
        else:
            s = SUITS.index(tile[1])
            n = NUMS.index(tile[0])
            hand[s][n] += 1
    return hand


def parse_tile(str):
    if len(str) == 1:
        return SUITS.index(str), 0
    else:
        return SUITS.index(str[1]), NUMS.index(str[0])


def init_tables():
    def gen3n(a, level, table):
        if level > 4:
            return
        # add a triplet
        for i in range(9):
            if a[i] + 3 > 4:
                continue
            b = a.copy()
            b[i] += 3
            table.add(tuple(b))
            gen3n(b, level + 1, table)
        # add a sequence
        for i in range(7):
            if (a[i] + 1 > 4) or (a[i + 1] + 1 > 4) or (a[i + 2] + 1 > 4):
                continue
            b = a.copy()
            b[i] += 1
            b[i + 1] += 1
            b[i + 2] += 1
            table.add(tuple(b))
            gen3n(b, level + 1, table)

    def gen3n2(table):
        for i in range(9):
            a = [0] * 9
            a[i] += 2
            table.add(tuple(a))
            gen3n(a, 1, table)

    global TAB3N, TAB3N2
    path = Path(__file__).parent / "win.pickle"
    if path.exists():
        with open(path, "rb") as f:
            TAB3N, TAB3N2 = pickle.load(f)
    else:
        TAB3N = set()
        TAB3N2 = set()
        TAB3N.add((0,) * 9)
        gen3n([0] * 9, 1, TAB3N)
        gen3n2(TAB3N2)
        with open(path, "wb") as f:
            pickle.dump((TAB3N, TAB3N2), f)


def checkwin(hand):
    if hand_count(hand) != 14:
        return False
    have3n2 = False
    for s in range(10):
        a = tuple(hand[s])
        if a in TAB3N2:
            if have3n2:
                return False
            else:
                have3n2 = True
        elif a not in TAB3N:
            return False
    return True


def wintile(hand):
    if hand_count(hand) != 13:
        return []
    tiles = []
    # 条 饼 万
    for s in range(3):
        for rank in range(9):
            if hand[s][rank] >= 4:
                continue
            hand_copy = deepcopy(hand)
            hand_copy[s][rank] += 1
            if checkwin(hand_copy):
                tiles.append(TILES_TEXT[s][rank])
    # 东 西 南 北 中 发 白
    for s in range(3, 10):
        if hand[s][rank] >= 4:
            continue
        hand_copy = deepcopy(hand)
        hand_copy[s][0] += 1
        if checkwin(hand_copy):
            tiles.append(TILES_TEXT[s][0])
    return tiles


def suggest(hand):
    if hand_count(hand) != 14:
        return []
    tiles = {}
    for s in range(10):
        for rank in range(9):
            if hand[s][rank] < 1:
                continue
            hand_copy = deepcopy(hand)
            hand_copy[s][rank] -= 1
            win_tiles = wintile(hand_copy)
            if len(win_tiles) > 0:
                info = []
                for tile in win_tiles:
                    win_tile_suit, win_tile_rank = parse_tile(tile)
                    info.append((tile, 4 - hand_copy[win_tile_suit][win_tile_rank]))
                tiles[TILES_TEXT[s][rank]] = info
    return tiles


init_tables()
