# Data dictionary

The analysis uses Aditya Desai’s [100,000 UK Used Car Data Set](https://www.kaggle.com/adityadesai13/used-car-dataset-ford-and-mercedes). Kaggle lists the dataset as **CC0: Public Domain**. Each row represents a used-car listing. The repository includes the [analysis-ready CSV](processed/cars_clean.csv) with 96,255 rows.

## Fields

| Column | Definition |
| --- | --- |
| `brand`, `model` | Vehicle brand and model |
| `year` | Vehicle year as recorded in the source |
| `price` | Listing asking price in GBP |
| `mileage` | Total recorded mileage in miles |
| `transmission`, `fuelType` | Recorded transmission and fuel categories |
| `tax`, `mpg`, `engineSize` | Recorded road tax in GBP, fuel economy in miles per gallon, and engine size in litres |
| `age` | Vehicle age in years, calculated as `2020 − year` |
| `annual_mileage` | Estimated miles per year, calculated as `mileage / max(age, 1)` |
| `mileage_k`, `annual_mileage_k` | Total and estimated annual mileage in thousands of miles |
| `log_price` | Natural logarithm of the asking price |

## Sample construction

The [cleaning notebook](../notebooks/01_cleaning.ipynb) combines the nine brand files. The four additional Focus and C-Class files contain subsets or uncleaned versions of records from the brand files.

| Step | Rows remaining |
| --- | ---: |
| Combine the nine brand files | 99,187 |
| Remove exact duplicates | 97,712 |
| Require observed price, year, mileage, and brand | 97,712 |
| Keep vehicle years from 1990 through 2020 | 97,709 |
| Require positive price and mileage | 97,709 |
| Trim asking prices below the 0.5th and above the 99.5th percentile | 96,739 |
| Trim estimated annual mileage above the 99.5th percentile | 96,255 |

See the [reproduction commands](../README.md#reproduce-the-results) to rebuild the dataset.
