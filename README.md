# BTV Rentals Backend


## Overview

This project provides a backend for BTV Rentals, a Burlington, VT property search application to identify code-compliant rental properties.

## Get Started
This app has been tested and developed on Python version `3.8.1`. This is available for download from [python.org](https://www.python.org/).

1. [Clone](https://help.github.com/articles/cloning-a-repository/) the repository to your local device, `cd` to its location
2. Install the dependencies: `pip install -r requirements.txt`, and configure the project as editable by running `pip install -e .`
3. Install [PostgreSQL](https://www.postgresql.org/download/) to your machine.
4. Install [Redis](https://redis.io/download) to your machine.
5. Create a database by running `createdb <database name>`
6. Copy `.env.sample` to `.env`, and configure your environment variables, paying attention to the `DATABASE_URL` and `REDIS_URL` variables. See the section on [environment variables](#environment-variables) for more information on each one.
7. Run the data pipeline, which can be found in the `pipeline/` directory and can be run by typing `python pipeline/data.py`
8. Run the API by typing in your console: `python -m flask run`

## Linting
This repo has [flake8](http://flake8.pycqa.org/en/latest/) style guide enforcement configured. Flake8 can be run from the command line by typing `flake8` in the root directory, or can be configured to use in your editor of choice (this is automatically configured if you use **Visual Studio Code**)

## Environment Variables
* `DATABASE_URL`: Your PostgreSQL connection string, a [JDBC complaint url](https://jdbc.postgresql.org/documentation). Tables will be initialized upon run of the data pipeline
* `FLASK_APP`: This should not be changed, as the `app.py` file resides in the `./src` directory.
* `FLASK_DEBUG`: Allows you to turn on and off Flask debug mode. `1` for on, `0` for off.
* `FLASK_ENV`: Which environment should Flask be run in. This accepts two arguments, `development` or `production`.
* `REDIS_URL`: Your Redis connection string, whose format can be found [here](https://metacpan.org/pod/URI::redis)
* `RENTAL_COC_URL`: The Burlington rental properties URL. This link needs to be in CSV format, with `,` as the seoarator (`%2C` when URL encoded).

## API Documentation
* [/search/[query]](docs/api-search.md)

## Team Members
* Clasby Chope <Katherine.Chope@uvm.edu>
* Christian DeLuca <Christian.Deluca@uvm.edu>
* Samuel Frederick <Samuel.Frederick@uvm.edu>
* Harry Makovsky <Harrison.Makovsky@uvm.edu>


