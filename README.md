# custom_api_project

Group Member Contributions:

Matt - Main/README

Bret - SQL Database

Troy - Flask API



This API was created to view relevant data for any top 1000 baby name since 1880.


To run: first download the names.zip file from https://www.ssa.gov/oact/babynames/limits.html


Create a folder in custom_api_project called ssa_data and drag the .txt files from names.zip into that folder.


Run main.py and then run flask_api.py.


Example usage: "http://127.0.0.1:5000/nameinfo?name=John"

Example output: 
{
  "first_year": 1880,
  "most_popular_year": 1947,
  "name": "John",
  "top_years": [1947, 1952, 1948, 1964, 1951, 1949, 1954, 1956, 1953, 1955]
}