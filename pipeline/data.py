from sqlalchemy import Integer, String, Date
from utils.config import config
import utils.db as db
import pandas as pd
import usaddress
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError

# Configuration
RENTAL_COC_URL = "https://data.burlingtonvt.gov/explore/dataset/rental-property-certificate-of-compliance/download/?format=csv&timezone=US/Eastern&lang=en&use_labels_for_header=true&csv_separator=%2C"


def main():
    if config["DEVELOPMENT_DATA_CACHE"]:
        data = pd.read_csv(
            "./pipeline/rental-property-certificate-of-compliance.csv"
        )
    else:
        data = pd.read_csv(RENTAL_COC_URL)

    db.load_schema()

    # Drop unneeded columns
    try:
        data = data.drop(columns=[
            'AmandaPropertyRSN',
            'TaxParcelId',
            'GISPIN',
            'UniqueId'
        ])
    except KeyError as e:
        print("Attempted to drop non-existent column: " + str(e))

    # Drop rows with duplicate Span IDs
    droplog = pd.DataFrame()
    null_mask = data.duplicated(subset=['Span'], keep='first')
    clean_data = data.loc[~null_mask]
    droplog = droplog.append(data.loc[null_mask])

    for index, row in droplog.iterrows():
        print("Row Dropped (duplicate span): " + row['Span']
              + " " + row['StreetAddress']
              )

    # Drop rows with null Span IDs
    droplog = pd.DataFrame()
    droplog = clean_data.loc[clean_data.Span.isnull()]
    clean_data = clean_data.dropna(subset=['Span'])

    for index, row in droplog.iterrows():
        print("Row Dropped (null span): " + row['StreetAddress'])

    # Parse addresses
    address_variations = []

    def parse_address(row):
        try:
            address = normalize_address_record(row['StreetAddress'])
            address_parts = address['address_line_1'].split(" ")

            if "-" in address_parts[0]:
                numbers = address_parts[0].split("-")
                try:
                    range_low = int(numbers[0])
                    range_high = int(numbers[1])

                    for i in range(range_low, range_high + 1):
                        address_variations.append(
                            [str(i) + " " + " ".join(address_parts[1:]), row['Span']])
                except ValueError:
                    print("Could not parse address number: " +
                          row['StreetAddress'])
            else:
                address_variations.append(
                    [address['address_line_1'], row['Span']])
        except UnParseableAddressError:
            print("Address not normalized due to usaddress parser failing: " +
                  row['StreetAddress'])
            return ""
        return address['address_line_1']

    clean_data['StreetAddress'] = clean_data.apply(
        parse_address, axis=1)

    clean_data.to_sql(
        "properties",
        con=db.get_engine(),
        if_exists="replace",
        method="multi",
        dtype={
            'CoCYears': Integer,
            'Span': String,
            'StreetAddress': String,
            'UnitNumber': String,
            'LandUseCode': String,
            'ResidentialUnits': Integer,
            'RentalUnits': Integer,
            'geopoint': String,
            'CoCIssueDate': Date,
            'CoCExpireDate': Date,
            'LastMhInDate': Date,
            'LastMhInspectionDate': Date,
            'UpdateDate': Date
        }
    )

    address_df = pd.DataFrame(address_variations, columns=["Address", "Span"])
    address_df.to_sql(
        "addresses",
        con=db.get_engine(),
        if_exists="replace",
        method="multi",
        dtype={
            'address': String,
            'span': String
        }
    )

    with db.get_engine().connect() as con:
        con.execute('ALTER TABLE "properties" ADD PRIMARY KEY ("Span");')
        con.execute('ALTER TABLE "addresses" ADD PRIMARY KEY ("index");')
        con.execute('CREATE INDEX IF NOT EXISTS "addresses_index" ON "public"."addresses" USING BTREE ("Address");')


main()
