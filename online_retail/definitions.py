from dagster import Definitions, load_assets_from_modules
from online_retail.assets import clean_dataset, raw_dataset

assets = load_assets_from_modules([raw_dataset, clean_dataset])

defs = Definitions(assets=assets)
