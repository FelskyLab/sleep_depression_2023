# Data

Contains Any data that is relevant to your project.

As you acquire and process your data with the goal of improving its structure and quality it will generally go through the below states.

> **Note**
> All files within the data directory are ignored and will not be committed to your repo

## Bronze

Contains raw data (data in its original state) that you've simply moved from any external system to where you need it with little to no manipulation. The underlying data storage format may be converted for efficient storage (i.e. .csv --> .parquet) and data may be timestamped to indicate versions.

Data the is located physically elsewhere on the SCC can be symbolically linked with `ln -s <original-path-to-raw-data> <new-path>` so that it is available in your project directory.

## Silver

Contains raw data that has been enriched, filtered, cleaned, and joined together appropriately to minimize data duplication and is provided a well defined structure and enforced schema (columns have declared types, i.e. `integer`).

This is the data that your analyses will be performed on.

## Gold

Contains the outputs of any analyses you have performed.
