import os
import pandas as pd

from classes.waterfall import Waterfall
from models.viterbi import viterbi_opt
from data.findAllWaterfalls import wrappper

if __name__ == '__main__':

    # initializations
    revenue_r            = []
    num_waterfalls_r     = []
    waterfall_r          = []
    waterfall_r_fillname = []
    waterfall_viterbi_r  = []

    # prepare outpot folder
    if not os.path.exists('outputs'): os.mkdir('outputs')
    for f in os.listdir('outputs'): os.remove('outputs/' + f)

    # create all possible waterfall
    if sum([len(files) for r, d, files in os.walk("data/Waterfalls")]) < 100: wrappper('data/MatrixM.csv','Waterfalls')

    # loop over all possible waterfall for each r and select the best one in terms of revenue
    for r in sorted(os.listdir('data/Waterfalls')):
        max_revenue = 0
        for filename in os.listdir('data/Waterfalls/' + r + '/'):
            if filename != '.ipynb_checkpoints':
                curr_waterfall = Waterfall(csv_path='data/Waterfalls/' + r + '/' + filename)
                revenue = sum(curr_waterfall.get_df()['revenue'])
                if revenue > max_revenue:
                    max_revenue = revenue
                    best_waterfallname = filename
                    curr_waterfall.reorder(sort_by='price', reverse=True)
                    best_waterfall = curr_waterfall.get_df()

        print(r + ' = ' + str(max_revenue))
        revenue_r.append(max_revenue)
        pd.DataFrame(revenue_r).to_csv('outputs/revenue_r.csv')

        print('num_waterfalls = '  + str(len(os.listdir('data/Waterfalls/' + r + '/'))))
        num_waterfalls_r.append(len(os.listdir('data/Waterfalls/' + r + '/')))
        pd.DataFrame(num_waterfalls_r).to_csv('outputs/num_waterfalls_r.csv')

        print(best_waterfall)
        waterfall_r.append(best_waterfall)
        with open('outputs/waterfall_r.txt', 'w') as f:
            for item in waterfall_r:
                f.write("%s\n" % item)

        # start Viterbi optimization
        print('Viterbi:')
        final_waterfall, layers = viterbi_opt('data/MatrixM.csv', 'my_log', 'data/Waterfalls/' + r + '/' + best_waterfallname, 1, 0) #no min impression limit
        waterfall_viterbi_r.append(final_waterfall)
        with open('outputs/waterfall_viterbi_r.txt', 'w') as f:
            for item in waterfall_viterbi_r:
                f.write("%s\n" % item)

        print(final_waterfall)
        print('...')



    #########################################
    # analyze Viterbi by min impression (Y) #
    #########################################

    waterfall_viterbi_m = []
    for m in [50,100,150,200,250,300,350,400]:
        final_waterfall, layers = viterbi_opt('data/MatrixM.csv', '', 'data/Waterfalls/' + r + '/' + best_waterfallname, m, 20)
        waterfall_viterbi_m.append(final_waterfall)
        with open('outputs/waterfall_viterbi_m.txt', 'w') as f:
            for item in waterfall_viterbi_m:
                f.write("%s\n" % item)
        print(final_waterfall)
        print('...')
