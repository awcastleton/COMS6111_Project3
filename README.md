# COMS6111_Project3

* Project Group 21
* Alexander Castleton: awc2134
* Justin (Max) Pugliese: jp3571

## Files in Submission

* apriori.py: The Python script in which Apriori exists
* example-run.txt: The output from the detailed run
* README.md: this file
* INTEGRATED-DATASET.csv: Our customized dataset from the NYC Open Data Site
* output.txt: The program's output file

## Project Dependencies
* pandas
* Python 3+

## Package-Installation Commands on Ubuntu 14.04 Google Cloud VM
* apt-get install python-setuptools <br/>
* apt-get install python3-pip <br/>
* pip3 install pandas <br/>

## Connecting to the Virtual Machine

External IP: 104.196.62.59  <br/>
Username: project3 <br/>
password: passw0rd <br/>

ssh project3@104.196.62.59  <br/>
passw0rd

## Running the Code

cd /home/project2/COMS6111_Project3 <br/>
python3 apriori.py INTEGRATED-DATASET.csv \<support\> \<confidence\>

## Integrated Dataset Explanation

Our primary dataset was named [311-Service-Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests/fvrb-kbbt) and contained a listing of all the 311 calls starting in 2010. The 311 dataset is large and multifaceted so we filtered the first 100,000 entries into two distinct groups:

1. Building Requests - Entries where the responding agency was either the Department of Buildings or the Housing Preservation and Development Department.
2. Noise Complaints - Entries where the complaint type is 'Noise' which occurred at a 'Residential' location.

We then inner-joined the data sets together when the incident locations overlapped. Manipulating the data in this way allowed us to see the types of quality of life issues at buildings that also have high noise pollution. Conceptually, the data could show that by fixing specific building issues quickly the city saves additional time and money from the Police department by reducing the number of Noise complaints.

## Compelling Execution Description
The following command was used for the example:
`python3 apriori.py INTEGRATED-DATASET.csv .1 .8`

The example output shows a relation between Noise complaints and problems with the heat & water systems at 89-21 ELMHURST AVENUE, a low-income housing condominium. Multiple city agencies are spending time and effort responding to various issues from this single residence. More investigation should be done, but it is possible that by investing in upgrading the residence's heat/water facilities the city could save time and money by decreasing the amount of attention it is obligated to give this specific building.
