from utils.config import config
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError
from sqlalchemy import Integer, String, Date
import pandas as pd
import utils.db as db


def main():
    if config["DEVELOPMENT_DATA_CACHE"]:
        data = pd.read_csv(
            "./pipeline/rental-property-certificate-of-compliance.csv"
        )
    else:
        data = pd.read_csv(config['RENTAL_COC_URL'])
        print("Latest CoC data downloaded")

    db.init_db()

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
                        address_variations.append([
                            str(i) + " " + " ".join(address_parts[1:]),
                            row['Span']
                        ])
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

    with db.get_engine().connect() as con:
        con.execute('ALTER TABLE "properties" ADD PRIMARY KEY ("Span");')
        con.execute('ALTER TABLE "addresses" ADD PRIMARY KEY ("index");')

        con.execute(('ALTER TABLE "addresses" '
                     'DROP CONSTRAINT IF EXISTS fkey_Span;'))

        con.execute(('ALTER TABLE "addresses" '
                     'ADD CONSTRAINT "fkey_Span" '
                     'FOREIGN KEY ("Span") '
                     'REFERENCES "public"."properties" ("Span") '
                     'ON DELETE CASCADE;'))

        con.execute(('CREATE INDEX IF NOT EXISTS "addresses_address_index" '
                     'ON "public"."addresses" '
                     'USING BTREE ("Address");'))

        con.execute(('CREATE INDEX IF NOT EXISTS "addresses_span_index" '
                     'ON "public"."addresses" '
                     'USING BTREE ("Span");'))


main()
