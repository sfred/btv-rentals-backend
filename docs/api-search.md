**/search/[query]**
----
  > The search API returns a property for the given search term. As address can be represented by multiple city parcels, the API will return more than one property if this is the case.

* **URL**

  `/search/[query]`

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `query (String)`: A search query to look for

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    [
      {
        "index": <string>,
        "CoCYears": <integer>,
        "CoCIssueDate": <date>,
        "CoCExpireDate": <date>,
        "Span": <string>,
        "StreetAddress": <string>,
        "UnitNumber": <string>,
        "LandUseCode": <string>,
        "ResidentialUnits": <integer>,
        "RentalUnits": <integer>,
        "LastMhInDate": <date>,
        "LastMhInspectionDate": <date>,
        "UpdateDate": <date>,
        "geopoint": <string>
      }
    ]
    ```
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{'error': 'Address not parseable'}` <br />
    **Meaning:** The address entered cannot be parsed by the API. Check your formatting and try again.

  * **Code:** 404 <br />
    **Content:** `{'error': 'No results found'}` <br />
    **Meaning:** The address was parsed successfully, but no results were found. This could mean that the data does not exist, or that the property is not a rental.

  * **Code:** 503 <br />
    **Content:** n/a <br />
    **Meaning:** You have exceeded the rate limit. The maximum amount of requests is `1 req/s`.

* **Sample Call:**

  `https://btv-rentals-backend.herokuapp.com/search/8 Saint Francis Park`

  Sample Result:
  ```
  [
    {
      "index": 976,
      "CoCYears": 5,
      "CoCIssueDate": "2016-02-09",
      "CoCExpireDate": "2021-02-09",
      "Span": "114-035-10695",
      "StreetAddress": "6-8 SAINT FRANCIS PARK",
      "UnitNumber": null,
      "LandUseCode": "RC",
      "ResidentialUnits": 2,
      "RentalUnits": 2,
      "LastMhInDate": "2016-01-07",
      "LastMhInspectionDate": "2016-02-09",
      "UpdateDate": "2020-03-03",
      "geopoint": "44.51948,-73.2564"
    }
  ]
  ```