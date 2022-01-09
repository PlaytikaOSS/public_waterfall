import pandas as pd
import math
import os

def capacity_check(adNetwork_list):
    """check that adding node will not violate the MAX_CAPACITY property and that two consecutive instances do
    not belong to the same adNetwotks"""

    r = len(adNetwork_list) # r is the waterfall length/depth

    if r == 2:
        MAX_CAPACITY = {"AdNetwork1": 0,
                      "AdNetwork2": 1,
                      "AdNetwork3": 1}
    elif r == 3:
        MAX_CAPACITY = {"AdNetwork1": 1,
                      "AdNetwork2": 1,
                      "AdNetwork3": 1}
    elif r == 4:
        MAX_CAPACITY = {"AdNetwork1": 1,
                        "AdNetwork2": 2,
                        "AdNetwork3": 1}
    elif r == 5:
        MAX_CAPACITY = {"AdNetwork1": 2,
                        "AdNetwork2": 2,
                        "AdNetwork3": 1}
    elif r == 6:
        MAX_CAPACITY = {"AdNetwork1": 2,
                        "AdNetwork2": 2,
                        "AdNetwork3": 2}
    elif r == 7:
        MAX_CAPACITY = {"AdNetwork1": 3,
                        "AdNetwork2": 2,
                        "AdNetwork3": 2}
    elif r == 8:
        MAX_CAPACITY = {"AdNetwork1": 3,
                        "AdNetwork2": 3,
                        "AdNetwork3": 2}
    elif r == 9:
        MAX_CAPACITY = {"AdNetwork1": 4,
                        "AdNetwork2": 3,
                        "AdNetwork3": 2}

    CURR_CAPACITY = {"AdNetwork1": 0,
                  "AdNetwork2": 0,
                  "AdNetwork3": 0}

    for i in range(r):
        if i < len(adNetwork_list)-1 and adNetwork_list[i] == adNetwork_list[i+1]:
            return False
        CURR_CAPACITY[adNetwork_list[i]] += 1
        if CURR_CAPACITY[adNetwork_list[i]] > MAX_CAPACITY[adNetwork_list[i]]:
            return False
    return True


def same_price_check(keys, prices):
    """check that the same adNetwotk don't have two equal prices"""

    for i in range(len(keys)):
        for j in range(i, len(keys)):
            if i != j and keys[i] == keys[j] and prices[i] == prices[j]:
                return False
    return True


def get_next_price(keys, prices, adNetwork, price):
    """find the next adNetwotk price if exists"""

    for i in range(len(keys)):
        if keys[i] == adNetwork and prices[i] == price:
            for j in range(i, len(keys)):
                if i != j and keys[j] == adNetwork:
                    return prices[j] - 1
    return maxPrice


def wrappper(MatrixM_path, output_dir):
    '''Here we generate all possible waterfall accordint to thier length (r)'''

    global maxPrice
    M = pd.read_csv(MatrixM_path, sep=',')
    maxPrice = M.iloc[0, 0]  # 12
    numAdnetwork = M.shape[1] - 1  # 3
    adNetworks = list(M.columns[1:])

    # r = 1
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r1'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1/maxPrice))]

        waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
        allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                     columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions', 'Network fill rate', 'Revenue','Network RFM', 'Ad unit id']))
        if not os.path.exists(Opath): os.mkdir(Opath)
        allWaterfalls[-1].to_csv(Opath + '/waterfall_r1_' + str(i) + '.csv', index=False)
        i += 1

    # r = 2
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r2'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1/maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2/maxPrice))]

            if price1 <= price2 and capacity_check([adNetwork1,adNetwork2]):
                waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                             columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions', 'Network fill rate', 'Revenue','Network RFM', 'Ad unit id']))
                if not os.path.exists(Opath): os.mkdir(Opath)
                allWaterfalls[-1].to_csv(Opath + '/waterfall_r2_' + str(i) + '.csv', index=False)
                i += 1

    # r = 3
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r3'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1/maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2/maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3/maxPrice))]

                    if price2 <= price3 and adNetwork2 != adNetwork3 and capacity_check([adNetwork1,adNetwork2,adNetwork3]):
                        waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                        waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                        waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                        allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                     columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions', 'Network fill rate', 'Revenue','Network RFM', 'Ad unit id']))
                        if not os.path.exists(Opath): os.mkdir(Opath)
                        allWaterfalls[-1].to_csv(Opath + '/waterfall_r3_' + str(i) + '.csv', index=False)
                        i += 1

    # r = 4
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r4'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1/maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2/maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3/maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]

                            keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4]
                            prices = [price1, price2, price3, price4]

                            if price3 <= price4 and adNetwork3 != adNetwork4 and capacity_check(keys) and same_price_check(keys, prices):
                                waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                             columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions', 'Network fill rate', 'Revenue','Network RFM', 'Ad unit id']))
                                if not os.path.exists(Opath): os.mkdir(Opath)
                                allWaterfalls[-1].to_csv(Opath + '/waterfall_r4_' + str(i) + '.csv', index=False)
                                i += 1

    # r = 5
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r5'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1 / maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2 / maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3 / maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]
                            if price3 <= price4 and adNetwork3 != adNetwork4:
                                for instance5 in range(maxPrice * numAdnetwork):
                                    price5 = instance5 % maxPrice + 1
                                    adNetwork5 = adNetworks[int(math.floor(instance5 / maxPrice))]

                                    keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4, adNetwork5]
                                    prices = [price1, price2, price3, price4, price5]

                                    if price4 <= price5 and adNetwork4 != adNetwork5 and capacity_check(keys) and same_price_check(keys, prices):
                                        waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                        waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                        waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                        waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                        waterfall_list.append('High, 1,' + adNetwork5 + ' Oct $' + str(price5) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)]) * price5 / 1000) + ', 0, 5')
                                        allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                                                          columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions','Network fill rate', 'Revenue', 'Network RFM','Ad unit id']))
                                        if not os.path.exists(Opath): os.mkdir(Opath)
                                        allWaterfalls[-1].to_csv(Opath + '/waterfall_r5_' + str(i) + '.csv', index=False)
                                        i += 1

    # r = 6
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r6'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1 / maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2 / maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3 / maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]
                            if price3 <= price4 and adNetwork3 != adNetwork4:
                                for instance5 in range(maxPrice * numAdnetwork):
                                    price5 = instance5 % maxPrice + 1
                                    adNetwork5 = adNetworks[int(math.floor(instance5 / maxPrice))]
                                    if price4 <= price5 and adNetwork4 != adNetwork5:
                                        for instance6 in range(maxPrice * numAdnetwork):
                                            price6 = instance6 % maxPrice + 1
                                            adNetwork6 = adNetworks[int(math.floor(instance6 / maxPrice))]

                                            keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4, adNetwork5, adNetwork6]
                                            prices = [price1, price2, price3, price4, price5, price6]

                                            if price5 <= price6 and adNetwork5 != adNetwork6 and capacity_check(keys) and same_price_check(keys, prices):
                                                waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                                waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                                waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                                waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                                waterfall_list.append('High, 1,' + adNetwork5 + ' Oct $' + str(price5) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)]) * price5 / 1000) + ', 0, 5')
                                                waterfall_list.append('High, 1,' + adNetwork6 + ' Oct $' + str(price6) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)]) * price6 / 1000) + ', 0, 6')
                                                allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                                                                  columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions','Network fill rate', 'Revenue', 'Network RFM','Ad unit id']))
                                                if not os.path.exists(Opath): os.mkdir(Opath)
                                                allWaterfalls[-1].to_csv(Opath + '/waterfall_r6_' + str(i) + '.csv', index=False)
                                                i += 1

    # r = 7
    '''i = 0
    allWaterfalls = []
    Opath = output_dir + '/r7'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1 / maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2 / maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3 / maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]
                            if price3 <= price4 and adNetwork3 != adNetwork4:
                                for instance5 in range(maxPrice * numAdnetwork):
                                    price5 = instance5 % maxPrice + 1
                                    adNetwork5 = adNetworks[int(math.floor(instance5 / maxPrice))]
                                    if price4 <= price5 and adNetwork4 != adNetwork5:
                                        for instance6 in range(maxPrice * numAdnetwork):
                                            price6 = instance6 % maxPrice + 1
                                            adNetwork6 = adNetworks[int(math.floor(instance6 / maxPrice))]
                                            if price5 <= price6 and adNetwork5 != adNetwork6:
                                                for instance7 in range(maxPrice * numAdnetwork):
                                                    price7 = instance7 % maxPrice + 1
                                                    adNetwork7 = adNetworks[int(math.floor(instance7 / maxPrice))]

                                                    keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4, adNetwork5, adNetwork6, adNetwork7]
                                                    prices = [price1, price2, price3, price4, price5, price6, price7]

                                                    if price6 <= price7 and adNetwork6 != adNetwork7 and capacity_check(keys) and same_price_check(keys, prices):
                                                        waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                                        waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                                        waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                                        waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                                        waterfall_list.append('High, 1,' + adNetwork5 + ' Oct $' + str(price5) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)]) * price5 / 1000) + ', 0, 5')
                                                        waterfall_list.append('High, 1,' + adNetwork6 + ' Oct $' + str(price6) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)]) * price6 / 1000) + ', 0, 6')
                                                        waterfall_list.append('High, 1,' + adNetwork7 + ' Oct $' + str(price7) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)]) * price7 / 1000) + ', 0, 7')
                                                        allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                                                                          columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions','Network fill rate', 'Revenue', 'Network RFM','Ad unit id']))
                                                        if not os.path.exists(Opath): os.mkdir(Opath)
                                                        allWaterfalls[-1].to_csv(Opath + '/waterfall_r7_' + str(i) + '.csv', index=False)
                                                        i += 1

    # r = 8
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r8'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1 / maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2 / maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3 / maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]
                            if price3 <= price4 and adNetwork3 != adNetwork4:
                                for instance5 in range(maxPrice * numAdnetwork):
                                    price5 = instance5 % maxPrice + 1
                                    adNetwork5 = adNetworks[int(math.floor(instance5 / maxPrice))]
                                    if price4 <= price5 and adNetwork4 != adNetwork5:
                                        for instance6 in range(maxPrice * numAdnetwork):
                                            price6 = instance6 % maxPrice + 1
                                            adNetwork6 = adNetworks[int(math.floor(instance6 / maxPrice))]
                                            if price5 <= price6 and adNetwork5 != adNetwork6:
                                                for instance7 in range(maxPrice * numAdnetwork):
                                                    price7 = instance7 % maxPrice + 1
                                                    adNetwork7 = adNetworks[int(math.floor(instance7 / maxPrice))]
                                                    if price6 <= price7 and adNetwork6 != adNetwork7:
                                                        for instance8 in range(maxPrice * numAdnetwork):
                                                            price8 = instance8 % maxPrice + 1
                                                            adNetwork8 = adNetworks[int(math.floor(instance8 / maxPrice))]

                                                            keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4, adNetwork5, adNetwork6, adNetwork7, adNetwork8]
                                                            prices = [price1, price2, price3, price4, price5, price6, price7, price8]

                                                            if price7 <= price8 and adNetwork7 != adNetwork8 and capacity_check(keys) and same_price_check(keys, prices):
                                                                waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                                                waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                                                waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                                                waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                                                waterfall_list.append('High, 1,' + adNetwork5 + ' Oct $' + str(price5) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)]) * price5 / 1000) + ', 0, 5')
                                                                waterfall_list.append('High, 1,' + adNetwork6 + ' Oct $' + str(price6) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)]) * price6 / 1000) + ', 0, 6')
                                                                waterfall_list.append('High, 1,' + adNetwork7 + ' Oct $' + str(price7) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)]) * price7 / 1000) + ', 0, 7')
                                                                waterfall_list.append('High, 1,' + adNetwork8 + ' Oct $' + str(price8) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork8, price8)].tolist()[0]:M.index[M['price'] == price8].tolist()[0] + 1,M.columns.get_loc(adNetwork8)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork8, price8)].tolist()[0]:M.index[M['price'] == price8].tolist()[0] + 1,M.columns.get_loc(adNetwork8)]) * price8 / 1000) + ', 0, 8')
                                                                allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                                                                                  columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions','Network fill rate', 'Revenue', 'Network RFM','Ad unit id']))
                                                                if not os.path.exists(Opath): os.mkdir(Opath)
                                                                allWaterfalls[-1].to_csv(Opath + '/waterfall_r8_' + str(i) + '.csv', index=False)
                                                                i += 1

    # r = 9
    i = 0
    allWaterfalls = []
    Opath = output_dir + '/r9'
    for instance1 in range(maxPrice * numAdnetwork):
        price1 = instance1 % maxPrice + 1
        adNetwork1 = adNetworks[int(math.floor(instance1 / maxPrice))]
        for instance2 in range(maxPrice * numAdnetwork):
            price2 = instance2 % maxPrice + 1
            adNetwork2 = adNetworks[int(math.floor(instance2 / maxPrice))]
            if price1 <= price2 and adNetwork1 != adNetwork2:
                for instance3 in range(maxPrice * numAdnetwork):
                    price3 = instance3 % maxPrice + 1
                    adNetwork3 = adNetworks[int(math.floor(instance3 / maxPrice))]
                    if price2 <= price3 and adNetwork2 != adNetwork3:
                        for instance4 in range(maxPrice * numAdnetwork):
                            price4 = instance4 % maxPrice + 1
                            adNetwork4 = adNetworks[int(math.floor(instance4 / maxPrice))]
                            if price3 <= price4 and adNetwork3 != adNetwork4:
                                for instance5 in range(maxPrice * numAdnetwork):
                                    price5 = instance5 % maxPrice + 1
                                    adNetwork5 = adNetworks[int(math.floor(instance5 / maxPrice))]
                                    if price4 <= price5 and adNetwork4 != adNetwork5:
                                        for instance6 in range(maxPrice * numAdnetwork):
                                            price6 = instance6 % maxPrice + 1
                                            adNetwork6 = adNetworks[int(math.floor(instance6 / maxPrice))]
                                            if price5 <= price6 and adNetwork5 != adNetwork6:
                                                for instance7 in range(maxPrice * numAdnetwork):
                                                    price7 = instance7 % maxPrice + 1
                                                    adNetwork7 = adNetworks[int(math.floor(instance7 / maxPrice))]
                                                    if price6 <= price7 and adNetwork6 != adNetwork7:
                                                        for instance8 in range(maxPrice * numAdnetwork):
                                                            price8 = instance8 % maxPrice + 1
                                                            adNetwork8 = adNetworks[int(math.floor(instance8 / maxPrice))]
                                                            if price7 <= price8 and adNetwork7 != adNetwork8:
                                                                for instance9 in range(maxPrice * numAdnetwork):
                                                                    price9 = instance9 % maxPrice + 1
                                                                    adNetwork9 = adNetworks[
                                                                        int(math.floor(instance9 / maxPrice))]

                                                                    keys = [adNetwork1, adNetwork2, adNetwork3, adNetwork4, adNetwork5, adNetwork6, adNetwork7, adNetwork8, adNetwork9]
                                                                    prices = [price1, price2, price3, price4, price5, price6, price7, price8, price9]

                                                                    if price8 <= price9 and adNetwork8 != adNetwork9 and capacity_check(keys) and same_price_check(keys, prices):
                                                                        waterfall_list = ['High, 1,' + adNetwork1 + ' Oct $' + str(price1) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork1, price1)].tolist()[0]:M.index[M['price'] == price1].tolist()[0] + 1,M.columns.get_loc(adNetwork1)]) * price1 / 1000) + ', 0, 1']
                                                                        waterfall_list.append('High, 1,' + adNetwork2 + ' Oct $' + str(price2) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork2, price2)].tolist()[0]:M.index[M['price'] == price2].tolist()[0] + 1,M.columns.get_loc(adNetwork2)]) * price2 / 1000) + ', 0, 2')
                                                                        waterfall_list.append('High, 1,' + adNetwork3 + ' Oct $' + str(price3) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork3, price3)].tolist()[0]:M.index[M['price'] == price3].tolist()[0] + 1,M.columns.get_loc(adNetwork3)]) * price3 / 1000) + ', 0, 3')
                                                                        waterfall_list.append('High, 1,' + adNetwork4 + ' Oct $' + str(price4) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork4, price4)].tolist()[0]:M.index[M['price'] == price4].tolist()[0] + 1,M.columns.get_loc(adNetwork4)]) * price4 / 1000) + ', 0, 4')
                                                                        waterfall_list.append('High, 1,' + adNetwork5 + ' Oct $' + str(price5) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork5, price5)].tolist()[0]:M.index[M['price'] == price5].tolist()[0] + 1,M.columns.get_loc(adNetwork5)]) * price5 / 1000) + ', 0, 5')
                                                                        waterfall_list.append('High, 1,' + adNetwork6 + ' Oct $' + str(price6) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork6, price6)].tolist()[0]:M.index[M['price'] == price6].tolist()[0] + 1,M.columns.get_loc(adNetwork6)]) * price6 / 1000) + ', 0, 6')
                                                                        waterfall_list.append('High, 1,' + adNetwork7 + ' Oct $' + str(price7) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork7, price7)].tolist()[0]:M.index[M['price'] == price7].tolist()[0] + 1,M.columns.get_loc(adNetwork7)]) * price7 / 1000) + ', 0, 7')
                                                                        waterfall_list.append('High, 1,' + adNetwork8 + ' Oct $' + str(price8) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork8, price8)].tolist()[0]:M.index[M['price'] == price8].tolist()[0] + 1,M.columns.get_loc(adNetwork8)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork8, price8)].tolist()[0]:M.index[M['price'] == price8].tolist()[0] + 1,M.columns.get_loc(adNetwork8)]) * price8 / 1000) + ', 0, 8')
                                                                        waterfall_list.append('High, 1,' + adNetwork9 + ' Oct $' + str(price9) + ',0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork9, price9)].tolist()[0]:M.index[M['price'] == price9].tolist()[0] + 1,M.columns.get_loc(adNetwork9)])) + ', 0,' + str(sum(M.iloc[M.index[M['price'] == get_next_price(keys, prices, adNetwork9, price9)].tolist()[0]:M.index[M['price'] == price9].tolist()[0] + 1,M.columns.get_loc(adNetwork9)]) * price9 / 1000) + ', 0, 9')
                                                                        allWaterfalls.append(pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]],
                                                                                                          columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions','Network fill rate', 'Revenue', 'Network RFM','Ad unit id']))
                                                                        if not os.path.exists(Opath): os.mkdir(Opath)
                                                                        allWaterfalls[-1].to_csv(Opath + '/waterfall_r9_' + str(i) + '.csv', index=False)
                                                                        i += 1'''


if __name__ == '__main__':

    wrappper('MatrixM.csv','Waterfalls')