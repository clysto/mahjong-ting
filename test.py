from mahjong import parse_hand, print_hand, wintile, checkwin, suggest

my_hand = "一条 一条 一条 二条 三条 四条 五条 六条 七条 八条 九条 九条 九条 中"
hand = parse_hand(my_hand)
print("我的手牌:")
print_hand(hand)

print("建议出牌:")
options = suggest(hand)
for tile, info in options.items():
    print(tile + ":")
    for tile, count in info:
        print("    听" + tile + ":", count, "张")
