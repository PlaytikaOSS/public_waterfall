import numpy as np
import pandas as pd

from classes.consts import DF_COLUMNS
from classes.utils import create_ad_units

class Waterfall:

    def __init__(self, ad_units=None, df=None, csv_path=None):

        self.ad_units = ad_units
        # Probability of accepting a user even if user valuation >= ad-unit floor price.

        self.df = self.set_df(df) if df is not None else None
        self.csv_path = csv_path

        if self.ad_units is None:
            assert df is not None or csv_path is not None, "If adnetworks is None " \
                                                           "then both df and csv_path cannot be None!"
            if csv_path is not None:
                self.df = self.set_df(pd.read_csv(self.csv_path))

            self.init_from_df()

        self.adnetworks = self.get_adnetworks()

        self.ad_units_by_id = {}  # Mapping of ad_unit_id to the actual ad_unit

        self.adnetworks_capacities = self.get_adnetworks_capacities()
        self.num_of_defaults = self.get_num_of_defaults()  # Number of ad-units with section "Auto"

        # for Viterbi
        self.best_child = []
        self.best_grandchild = []

    def get_num_of_defaults(self):
        """Returning the number of ad-units in the automatic section."""

        return sum([1 for ad_unit in self.ad_units if ad_unit.section == "Auto"])

    def reorder(self, sort_by='order', reverse=False):
        """Ordering the waterfall based on the sort_by column.
        For example, 'sort_by' can by 'order' or 'price'."""

        sign = 2 * int(reverse) - 1

        def sort_by_func(ad_unit):
            value = float(getattr(ad_unit, sort_by))
            if str(value) == 'nan':
                return -sign * np.inf
            else:
                return value

        if sort_by != 'order': # i.e., by price
            default_start = len(self.ad_units)
            for ad_unit in self.ad_units:
                if ad_unit.section == 'Auto': # Do not change the order of 'default' instances
                    default_start = ad_unit.order
                    break
            self.ad_units[0:default_start] = sorted(self.ad_units[0:default_start], key=sort_by_func, reverse=reverse) # sort without default
        else:
            self.ad_units = sorted(self.ad_units, key=sort_by_func, reverse=reverse)

        if self.ad_units[0].adnetwork_name == 'Cross':
            self.ad_units = [self.ad_units[1]] + [self.ad_units[0]] + self.ad_units[2:]

        for i, ad_unit in enumerate(self.ad_units):
            ad_unit.order = i + 1

    def get_adnetworks(self):
        return {ad_unit.adnetwork_name for ad_unit in self.ad_units}

    def set_df(self, df):
        """Setting, after cleaning and adding few columns (adnetwork_name and price),
        the DataFrame from which the waterfall is initialized."""

        def clean_ad_unit_name(x):
            ad_unit_name_tuple = x.split(" ")
            if len(ad_unit_name_tuple) == 1: return x
            i = 1 if ad_unit_name_tuple[1] != '(ironSource)' else 2
            return '_'.join(x.split(" ")[i:])

        def get_price(row):
            ad_unit_name = row["ad_unit_name"].replace("_", "")
            price_ind = ad_unit_name.rfind("$")
            # if price_ind != -1 and row["adnetwork_name"] not in self.brand_networks:
            if price_ind != -1:
                return int(float(ad_unit_name[price_ind + 1:]))
            else:
                return round(row["rpm"]) if row["rpm"] > 0 else 0

        df.rename(str.lower, axis='columns', inplace=True)
        df.rename({"ad unit": "ad_unit_name", "network fill rate": "fill_rate"}, axis='columns', inplace=True)

        df["adnetwork_name"] = df["ad_unit_name"].apply(lambda x: x.split(" ")[0])
        df["ad_unit_name"] = df["ad_unit_name"].apply(clean_ad_unit_name)
        df["price"] = df.apply(get_price, axis=1)

        return df[DF_COLUMNS].fillna(0)

    def init_from_df(self):
        """Initialized the waterfall using a DataFrame (assuming the DataFrame is set by the set_df method)."""

        ad_unit_groups = self.df.groupby("adnetwork_name").groups
        ad_units_params_per_adnetwork = {}
        for adnetwork in ad_unit_groups:
            ad_units_params_per_adnetwork[adnetwork] = [dict(self.df.iloc[i]) for i in ad_unit_groups[adnetwork]]
        self.ad_units = create_ad_units(ad_units_params_per_adnetwork)
        self.reorder()

    def set_ad_unit_order(self, ad_unit, order=True, order_sign=-1):
        """Calculating ad-unit order in the waterfall, according to its floor price, and placing it in the right place.
        In case of an ambiguity (same price as some other ad-unit) order_sign determines where to place it:
        if order_sign=-1 then the ad-unit will be place above all other ad-units with the same price;
        if order_sign=+1 then the ad-unit will be place below all other ad-units with the same price."""

        ad_unit_order = np.inf
        for other_ad_unit in self.ad_units:
            if other_ad_unit.ad_unit_id != ad_unit.ad_unit_id:
                if other_ad_unit.price < ad_unit.price:
                    ad_unit_order = other_ad_unit.order - 0.5
                    break
                elif other_ad_unit.price == ad_unit.price:
                    ad_unit_order = other_ad_unit.order + order_sign * 0.5
                    break
        ad_unit.order = ad_unit_order
        ad_unit.order = ad_unit_order
        if order:
            self.reorder()

    def set_price_and_order(self, ad_unit, price, order):
        """Set the price of the ad|_unit and reorder"""

        ad_unit.set_price(price)
        ad_unit.order = order
        self.reorder()

    def get_revenue(self):
        return sum([ad_unit.revenue for ad_unit in self.ad_units])

    def get_impressions(self):
        return sum([ad_unit.impressions for ad_unit in self.ad_units])

    def get_df(self):
        return pd.DataFrame([ad_unit.get_tuple() for ad_unit in self.ad_units], columns=DF_COLUMNS)

    def __repr__(self):
        return f"Total revenue = {self.get_revenue()}\n" + str(self.get_df())

    def get_adnetworks_capacities(self):
        """Calculated initial ad-networks capacities"""

        adnetworks_capacities = {adnetwork: 0 for adnetwork in self.adnetworks}
        for ad_unit in self.ad_units:
            adnetworks_capacities[ad_unit.adnetwork_name] += 1
        return adnetworks_capacities

    def set_best_child(self, child):
        self.best_child = child

    def set_best_grandchild(self, grandchild):
        self.best_grandchild = grandchild

if __name__ == "__main__":

    print("hi")