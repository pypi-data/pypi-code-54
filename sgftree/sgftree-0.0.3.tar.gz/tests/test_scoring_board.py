from helpers import load_sgf


kifu = load_sgf("test_data/game2.sgf")
print(kifu.board)
print(kifu.cursor.game)
print(kifu.get_score())
kifu.mark_stone("dead", (3, 15))
kifu.mark_stone("dead", (8, 6))
print(kifu.get_score())
