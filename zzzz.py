# -*- coding: utf-8 -*-
import hsdata

# 获取卡组数据
decks = hsdata.HSBoxDeck()
# 若未找到本地数据，会自动从网络获取
# print('从炉石盒子获取到', len(decks), '个卡组数据！')


print(decks.wins)

