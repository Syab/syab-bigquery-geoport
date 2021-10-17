import pandas as pd
from google.api_core.exceptions import NotFound
from google.cloud import bigquery

# TODO For user to change to your account project, or create a project in your account with the name below
# gcp_project ='gbq-ports-project'

client = bigquery.Client(project=gcp_project)

dataset_id = "{}.syab_geo_port_results".format(client.project)
table_id_1,table_id_2,table_id_3 = "five_nearest_ports", "largest_num_ports", "lost_sailor"

dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

# Creates new dataset in your project
client.create_dataset(dataset, timeout=30)
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

def run_query(sql):
    exc_query = client.query(sql)
    results = exc_query.result()
    return results.to_dataframe()

# Creates a table that identifies the 5 nearest ports to JURONG ISLAND
q1 = '''
CREATE TABLE IF NOT EXISTS `{}.{}`
AS
WITH params AS (
  SELECT ST_GeogPoint(103.733333333333, 1.28333333333333) AS center,
         10 AS maxn_ports,
         100 AS maxdist_km
),
distance_from_center AS (
  SELECT
    index_number,
    region_number,
    port_name,
    country,
    ST_GeogPoint(port_longitude, port_latitude) AS loc,
    ST_Distance(ST_GeogPoint(port_longitude, port_latitude), params.center) AS dist_meters
  FROM
    `bigquery-public-data.geo_international_ports.world_port_index`,
    params
  WHERE ST_DWithin(ST_GeogPoint(port_longitude, port_latitude), params.center, params.maxdist_km*1000)
)
SELECT port_name, dist_meters AS distance_in_meters from distance_from_center
WHERE dist_meters > 1
ORDER BY dist_meters 
LIMIT 5;
'''.format(dataset_id,table_id_1)

# Creates a table that identifies the lagest port where cargo_wharf is TRUE
q2 = '''
CREATE TABLE IF NOT EXISTS `{}.{}`
AS
SELECT country, COUNT(cargo_wharf=true) as port_count
FROM `bigquery-public-data.geo_international_ports.world_port_index`
GROUP BY country
ORDER BY port_count desc
LIMIT 1
'''.format(dataset_id,table_id_2)

# Creates a table that idenifies the nearest port to given coordinates (lat: 32.610982, long: -38.706256)
q3 = '''
CREATE TABLE IF NOT EXISTS `{}.{}`
AS
WITH params AS (
  SELECT ST_GeogPoint(-38.706256, 32.610982) AS center,
         1500 AS maxdist_km
),
distance_from_center AS (
  SELECT
    index_number,
    region_number,
    port_name,
    country,
    provisions,
    water,
    fuel_oil,
    diesel,
    port_longitude, port_latitude,
    ST_GeogPoint(port_longitude, port_latitude) AS loc,
    ST_Distance(ST_GeogPoint(port_longitude, port_latitude), params.center) AS dist_meters
  FROM
    `bigquery-public-data.geo_international_ports.world_port_index`,
    params
  WHERE ST_DWithin(ST_GeogPoint(port_longitude, port_latitude), params.center, params.maxdist_km*1000)
  AND (provisions=true AND water=true AND fuel_oil=true AND diesel=true)
)
SELECT country,port_name,port_longitude, port_latitude
FROM distance_from_center
WHERE dist_meters > 1
ORDER BY dist_meters
LIMIT 1;
'''.format(dataset_id,table_id_3)

q4 = '''
select * from `{}.{}`
'''.format(dataset_id,table_id_1)

q5 = '''
select * from `{}.{}`
'''.format(dataset_id,table_id_2)

q6 = '''
select * from `{}.{}`
'''.format(dataset_id,table_id_3)

for i in ([q1,q2,q3]):
    print("Running Query :", i)
    run_query(i)

for j in ([q4, q5, q6]):
    results = run_query(j)
    print(results)
