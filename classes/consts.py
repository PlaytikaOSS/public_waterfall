# Defining a default instance with price 0 to capture all users that wasn't captured by any other instance.
DEFAULT_AD_NETWORK_NAME = "default_ad_network"
DEFAULT_AD_UNIT_NAME = "default_ad_unit"

# Columns needed in order to initialize a waterfall from a csv file.
DF_COLUMNS = ["adnetwork_name", "ad_unit_name", "order", "section", "price", "rpm", "impressions", "fill_rate", "revenue"]

# For Viterbi
GAP = 1 # number of cutoffs in the prices (2 for 0,0.5,1,1.5,2... 1 for 0,1,2,..., or 3 for 0,0.33,0.66,1,1.33... etc.)
MIN_FRACTION_VITERBI = 15 # maxial price to do breakdown in descrete prices
MOV_AVG_IND_VITERBI = 1 # 0 use regular average. 1 use moving average
