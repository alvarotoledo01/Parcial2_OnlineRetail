from dagster import Definitions, load_assets_from_modules
from online_retail.assets import clean_dataset, load_dataset, create_features

assets = load_assets_from_modules([load_dataset, clean_dataset, create_features])

defs = Definitions(assets=assets)
