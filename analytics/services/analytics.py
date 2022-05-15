import pandas as pd

from django.conf import settings
from typing import Dict, List, Tuple


class Analytics:

    def __init__(self):
        self.path = settings.BASE_DIR.parent
        self.coupons = self.get_coupons_df()
        self.types_count = self.get_number_of_coupon_types()
        self.percent_off_min, self.percent_off_mean, self.percent_off_max = \
            self.get_min_mean_and_max_discounts('percent-off')
        self.dollar_off_min, self.dollar_off_mean, self.dollar_off_max = \
            self.get_min_mean_and_max_discounts('dollar-off')
        self.percent_off_min_by_retailer, self.percent_off_mean_by_retailer, self.percent_off_max_by_retailer = \
            self.get_min_mean_and_max_discounts_by_retailer('percent-off')
        self.dollar_off_min_by_retailer, self.dollar_off_mean_by_retailer, self.dollar_off_max_by_retailer = \
            self.get_min_mean_and_max_discounts_by_retailer('dollar-off')
        self.relevant_key_words_from_title, self.relevant_key_words_from_description = \
            self.get_relevant_key_words_from_title_and_description()

    def get_coupons_df(self) -> pd.DataFrame:
        coupons = pd.read_json(f"{self.path}/.data/coupons.json")
        return coupons['coupons'].apply(pd.Series)

    def get_number_of_coupon_types(self) -> pd.Series:
        return self.coupons['promotion_type'].value_counts()

    def get_min_mean_and_max_discounts(self, discount_key: str) -> Tuple[int, int, int]:
        min_value = self.get_values_of_min_discounts(self.coupons, discount_key)
        mean_value = self.get_values_of_mean_discounts(self.coupons, discount_key)
        max_value = self.get_values_of_max_discounts(self.coupons, discount_key)
        min_discounts = self.get_number_of_discounts(self.coupons, min_value)
        mean_discounts = self.get_number_of_discounts(self.coupons, mean_value)
        max_discounts = self.get_number_of_discounts(self.coupons, max_value)
        return min_discounts, mean_discounts, max_discounts

    def get_min_mean_and_max_discounts_by_retailer(self, discount_key: str) -> Tuple[int, int, int]:
        by_retail = self.get_group_by(['coupon_webshop_name', 'promotion_type', 'value'], frame_name='by_retail')
        min_value = self.get_values_of_min_discounts(by_retail, discount_key)
        mean_value = self.get_values_of_mean_discounts(by_retail, discount_key)
        max_value = self.get_values_of_max_discounts(by_retail, discount_key)
        min_discounts = self.get_number_of_discounts(by_retail, min_value)
        mean_discounts = self.get_number_of_discounts(by_retail, mean_value)
        max_discounts = self.get_number_of_discounts(by_retail, max_value)
        return min_discounts, mean_discounts, max_discounts

    def get_relevant_key_words_from_title_and_description(self) -> Tuple[Dict, Dict]:
        title = pd.Series(' '.join(self.coupons['title']).split()).value_counts()[:40]
        description = pd.Series(' '.join(self.coupons['description']).split()).value_counts()[:40]
        return title.to_dict(), description.to_dict()

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
