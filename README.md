# syab-bigquery-geoport

Result dataset has been shared with data_members@foodpanda.com

To run this in your environment:
### Prerquisites
1. Python 3 and latest version of pip installed
2. Google application credentials configured for BigQuery API. See Annex below.
3. python virtualenv installed

## Usage
1. Start python virtual environment.
```
virtualenv <your-virtualenv>
source <your-virtualenv>/bin/activate
```

2. Install dependencies
```
<your-env>/bin/pip install -r requirement.txt
```

3. In file ```geo_intl_ports.py``` line 6, change the name of the variable below with an existing project you may have on GCP. Othwerwise, you can also create a proect (in the GCP console) with the name below and uncomment the line.
```
# gcp_project = 'syab-gbq-ports-result'
```

4. Run the file.
```
python geo_intl_ports.py
```

## Outputs
Final Results :


- There are 7 outputs from running the file
    1. Output 1 : Prints the dataset created in the project

    2. Output 2 : Prints the query to run that answers Q1.
        - `five_nearest_ports` : output table created that identifies the 5 nearest ports from jurong island port
        - params : defines center point (JURONG ISLAND port), maximum distance from the centerpoint, and maximum number of ports around the center point.
        - distance_from_center : creates a virtual table from the query on the public dataset, geo_international_ports.world_port_index 

    3. Output 3 : Prints the query to run that answers Q2.
        - `largest_num_ports`: table created that identifies the country with the most cargo_wharf
        - counts the number of cargo_wharf=true and groups by country
        - first record identifies the country with the most cargo_wharf

    4. Output 4 : Prints the query to run that answers Q3.
        - `lost_sailor` : output table created that identifies the nearest port from given coordinates
        - params : defines center point (middle of atlantic ocean), maximum distance from the centerpoint.
        - distance_from_center : creates a virtual table from the query on the public dataset, geo_international_ports.world_port_index 
    5. Outputs data from `five_nearest_ports` table
    6. Outputs data from `largest_num_ports` table
    7. Outputs data from `lost_sailor` table

    ### Annex

    To configure google credentials on your local machine:
    1. In your GCP account console, go to IAM > Service Accounts > Create Service Account
    2. Type in a name for your service role
   
    3. 

     ![create_key](image/create_key.png)