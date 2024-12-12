import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# INFLUXDB_TOKEN = "J1Q1g0a4Bvnq8iFacMSVpyCBqdleqsOHB7szSrcUbXG1vyFxNZGMxLaPdMUxF84DsvcGktPiiSkC-nFy_Sh6rQ=="
INFLUXDB_TOKEN = "01V8vtfyM2HJf8t63tBWO4Bs9lw7VZ46HlIcS-nm1cBzvECT27YB86xLyhgnFJsbqaiStSXkCLtwGZ9HnfDJlA=="
# 01V8vtfyM2HJf8t63tBWO4Bs9lw7VZ46HlIcS-nm1cBzvECT27YB86xLyhgnFJsbqaiStSXkCLtwGZ9HnfDJlA==   token

token = INFLUXDB_TOKEN
org = "influxdb"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def influxdb_write(field:str,bucket:str,value):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = influxdb_client.Point("datatest").field(field,value)
    write_api.write(bucket=bucket, org=org, record=p)
    return p


def influxdb_query(field:str,bucket:str):

    query_api = client.query_api()

    q = '''from(bucket:_bucket)
    |> range(start: 2024-07-15T09:57:47.288Z)
    |> filter(fn:(r) => r._measurement == "datatest")
    |> filter(fn:(r) => r._field == _field)'''

    p = {
        "_field": field,
        "_bucket": bucket
        }

    result = query_api.query(query=q,org=org,params=p)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    return results

value, data = "value","data"


# y = influxdb_write(value,data,33.7)
# print(y)
# x = influxdb_query(value,data)
# print(x)