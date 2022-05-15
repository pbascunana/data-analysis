import pandas as pd

from django.conf import settings
from typing import List, Tuple


class Analytics:

    def __init__(self):
        self.path = settings.BASE_DIR.parent
        self.coupons = self.get_coupons_df()
        self.types_count = self.get_number_of_coupon_types()
        self.percent_off_discounts = self.get_percent_off_discounts()
        self.dollar_off_discounts = self.get_dollar_off_discounts()
        self.percent_off_discounts_by_retailer = self.get_percent_off_discounts_by_retailer()
        self.dollar_off_discounts_by_retailer = self.get_dollar_off_discounts_by_retailer()
        print(self.percent_off_discounts)

    def get_coupons_df(self) -> pd.DataFrame:
        coupons = pd.read_json(f"{self.path}/.data/coupons.json")
        return coupons['coupons'].apply(pd.Series)

    def get_number_of_coupon_types(self) -> pd.Series:
        return self.coupons['promotion_type'].value_counts()

    def get_percent_off_discounts(self) -> Tuple[int, int, int, str]:
        min_value = self.get_values_of_min_discounts(self.coupons, 'percent-off')
        mean_value = self.get_values_of_mean_discounts(self.coupons, 'percent-off')
        max_value = self.get_values_of_max_discounts(self.coupons, 'percent-off')
        min_discounts = self.get_number_of_discounts(self.coupons, min_value)
        mean_discounts = self.get_number_of_discounts(self.coupons, mean_value)
        max_discounts = self.get_number_of_discounts(self.coupons, max_value)
        return min_discounts, mean_discounts, max_discounts, '%'

    def get_dollar_off_discounts(self) -> Tuple[int, int, int, str]:
        min_value = self.get_values_of_min_discounts(self.coupons, 'dollar-off')
        mean_value = self.get_values_of_mean_discounts(self.coupons, 'dollar-off')
        max_value = self.get_values_of_max_discounts(self.coupons, 'dollar-off')
        min_discounts = self.get_number_of_discounts(self.coupons, min_value)
        mean_discounts = self.get_number_of_discounts(self.coupons, mean_value)
        max_discounts = self.get_number_of_discounts(self.coupons, max_value)
        return min_discounts, mean_discounts, max_discounts, '$'

    def get_percent_off_discounts_by_retailer(self) -> Tuple[int, int, int, str]:
        by_retail = self.get_group_by(['coupon_webshop_name', 'promotion_type', 'value'], frame_name='by_retail')
        min_value = self.get_values_of_min_discounts(by_retail, 'percent-off')
        mean_value = self.get_values_of_mean_discounts(by_retail, 'percent-off')
        max_value = self.get_values_of_max_discounts(by_retail, 'percent-off')
        min_discounts = self.get_number_of_discounts(by_retail, min_value)
        mean_discounts = self.get_number_of_discounts(by_retail, mean_value)
        max_discounts = self.get_number_of_discounts(by_retail, max_value)
        return min_discounts, mean_discounts, max_discounts, '%'

    def get_dollar_off_discounts_by_retailer(self) -> Tuple[int, int, int, str]:
        by_retail = self.get_group_by(['coupon_webshop_name', 'promotion_type', 'value'], frame_name='by_retail')
        min_value = self.get_values_of_min_discounts(by_retail, 'dollar-off')
        mean_value = self.get_values_of_mean_discounts(by_retail, 'dollar-off')
        max_value = self.get_values_of_max_discounts(by_retail, 'dollar-off')
        min_discounts = self.get_number_of_discounts(by_retail, min_value)
        mean_discounts = self.get_number_of_discounts(by_retail, mean_value)
        max_discounts = self.get_number_of_discounts(by_retail, max_value)
        return min_discounts, mean_discounts, max_discounts, '$'

    @staticmethod
    def get_values_of_min_discounts(dataframe: pd.DataFrame, key: str) -> int:
        return dataframe[(dataframe['promotion_type'] == key)].min()['value']

    @staticmethod
    def get_values_of_mean_discounts(dataframe: pd.DataFrame, key: str) -> int:
        return dataframe[(dataframe['promotion_type'] == key)].mean()['value']

    @staticmethod
    def get_values_of_max_discounts(dataframe: pd.DataFrame, key: str) -> int:
        return dataframe[(dataframe['promotion_type'] == key)].max()['value']

    @staticmethod
    def get_number_of_discounts(dataframe: pd.DataFrame, value: int) -> int:
        return dataframe[dataframe['value'] == value].value_counts().size

    def get_group_by(self, keys: List, frame_name: str) -> pd.DataFrame:
        return self.coupons.groupby(keys).size().to_frame(name=frame_name).reset_index()
