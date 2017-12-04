# COMS6111_Project3

* Project Group 21
* Alexander Castleton: awc2134
* Justin (Max) Pugliese: jp3571

## Files in Submission

## Project Dependencies
* pandas
* Python 3+

## Integrated Dataset Explanation

Our primary dataset was named [311-Service-Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests/fvrb-kbbt) and contained a listing of all the 311 calls starting in 2010. The 311 dataset is large and multifaceted so we filtered the first 100,000 entries into two distinct groups:

1. Building Requests - Entries where the responding agency was either the Department of Buildings or the Housing Preservation and Development Department.
2. Noise Complaints - Entries where the complaint type is 'Noise' which occurred at a 'Residential' location.

We then joined the data sets together when the incident locations overlapped. Manipulating the data in this way allowed us to see the types of quality of life issues at buildings that also have high noise pollution. Conceptually, the data could show that by fixing specific building issues quickly the city saves additional time and money from the Police department by reducing the number of Noise complaints.
