
y = "data"
z = "name"


x = 'ab' + str(y) + "cd"

query = '"from(bucket:"data")\
|> range(start: 2024-07-15T09:57:47.288Z, stop: 2024-07-15T10:57:47.288Z)\
|> filter(fn:(r) => r._measurement == "datatest")\
|> filter(fn:(r) => r._field == "value")'

query1 = '"from(bucket:"' + y + '")\
|> range(start: 2024-07-15T09:57:47.288Z, stop: 2024-07-15T10:57:47.288Z)\
|> filter(fn:(r) => r._measurement == "datatest")\
|> filter(fn:(r) => r._field == "'+ z +'")'

query2 = f'"from(bucket:"{y}")\
|> range(start: 2024-07-15T09:57:47.288Z, stop: 2024-07-15T10:57:47.288Z)\
|> filter(fn:(r) => r._measurement == "datatest")\
|> filter(fn:(r) => r._field == "{z}")'




