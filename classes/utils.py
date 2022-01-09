
from classes.ad_unit import AdUnit

def create_ad_units(ad_units_params_per_adnetwork, add_default=False):
    """Creating ad-units from a dictionary of lists, per ad-network a list of dictionaries containing all information
    to initiallize a new instance, e.g., adnetwork_name, ad_unit_name, order, section, price"""

    ad_units = []
    for adnetwork in ad_units_params_per_adnetwork:
        for params in ad_units_params_per_adnetwork[adnetwork]:
            if 'adnetwork_name' not in params:
                params['adnetwork_name'] = adnetwork
            ad_unit = AdUnit(**params)
            ad_units.append(ad_unit)

    if add_default:
        ad_units.append(AdUnit.get_default_ad_unit())

    return ad_units


if __name__ == "__main__":

    print('hi')
