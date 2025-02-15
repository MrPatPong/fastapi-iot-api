from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from typing import Optional, List
from bson.json_util import dumps, loads
import json
import uvicorn
from test import influxdb_query, influxdb_write

app = FastAPI()

# .\env\Scripts\activate
# uvicorn main:app --reload --host 192.168.1.135 --port 8080

Client = MongoClient("mongodb://localhost:27017/")
db = Client["esphttp"]
collection = db["data"]
collection0 = db["dataStore"]
collection1 = db["data1"]

Client0 = MongoClient("mongodb://localhost:27023/")
db0 = Client0["test"]
collec = db0["mongo_dock"]

class Data(BaseModel):
    name: str
    value: int
    datastore: list = []


class Data1(BaseModel):
    name: str
    value: int
    time: str

class Influx(BaseModel):
    bucket: str
    field: str

class Influx1(BaseModel):
    bucket: str
    field: str
    value: float

# for x in collection.find({}, {"_id":0, "name": 1, "count": 1 }): 
#         print(x)

# v1....................................................................................................

@app.get("/")
async def root():
    return {"message" : "Test5"}

@app.post("/mongo-docker/")
async def create(data: Data):
    # exis_data = collection.find_one({"name":data.name})
    # if exis_data :
    #     raise HTTPException(status_code=404,detail="data already exists")
    result = collec.insert_one(data.dict())
    return {
        "id" : str(result.inserted_id),
        "name" : data.name,
        "value" :data.value,
        }

@app.get("/mogo-docker/{data_id}")
async def read(data_id: str):
    data = collec.find_one({"_id": ObjectId(data_id)})
    if data:
        return {"id" : str(data["_id"]),"name" : data["name"],"value" : data["value"]}
    else:
        raise HTTPException(status_code=404,detail="data not found")

@app.post("/data/")
async def create(data: Data):
    # exis_data = collection.find_one({"name":data.name})
    # if exis_data :
    #     raise HTTPException(status_code=404,detail="data already exists")
    result = collection.insert_one(data.dict())
    return {
        "id" : str(result.inserted_id),
        "name" : data.name,
        "value" :data.value,
        }



@app.get("/data/{data_id}")
async def read(data_id: str):
    data = collection.find_one({"_id": ObjectId(data_id)})
    if data:
        return {"id" : str(data["_id"]),"name" : data["name"],"value" : data["value"]}
    else:
        raise HTTPException(status_code=404,detail="data not found")
    
 

        
@app.put("/data/{data_id}")
async def updete(data_id: str, data : Data ):
    result = collection.update_one({"_id": ObjectId(data_id)},{"$set" : data.dict(exclude_unset=True)})
    if result.modified_count == 1 :
        return {"id" : data_id, "name" : data.name ,"value" : data.value}
    else:
        raise HTTPException(status_code=404,detail="data not found")
    
@app.post("/datastore/")
async def create(data1: Data1):
    result = collection0.insert_one(data1.dict())
    return {
        "name" : data1.name,
        "value" :data1.value,
        "time" :data1.time
        }

# x = collection0.find({},{ "_id": 0})
# alldata = list(x)

# @app.get("/readall/")
# async def readAll():
#      alldataJson = dumps(alldata)
#      return alldataJson

@app.get("/readall/")
async def readall():
    x = collection1.find({}, {"_id":0})
    alldata = list(x)
    alldataJson = dumps(alldata)
    if x:
        return alldataJson

    


# v2.........................................................................................   
    
# @app.post("/data1/")
# async def create1( data: Data):
   
#     exis_data = collection1.find({"name": data.name})
#     alldata1 = list(exis_data)
#     alldataJson1 = dumps(alldata1)
#     if exis_data :
#         raise HTTPException(status_code=404,detail= str(alldataJson1))
        
#     result = collection1.insert_one(data.dict())
#     return {
#             "id" : str(result.inserted_id),
#             "name" : data.name,
#             "value" :data.value,
#             "datastore": data.datastore
#             }

@app.post("/data1/")
async def create1(data: Data):
    exis_data = collection1.find_one({"name":data.name})

    if exis_data :
        exis_data1 = collection1.find({"name":data.name},{"name": 0, "value": 0})
        alldata1 = list(exis_data1)
        alldataJson1 = dumps(alldata1)
        y = alldataJson1.strip("[]")
        y1 = json.loads(y)
        y2 = y1["_id"]
        # print(y2)
        raise HTTPException(status_code=404,detail=str(y2))
    result = collection1.insert_one(data.dict())
    return {
        "id" : str(result.inserted_id),
        "name" : data.name,
        "value" :data.value,
        "datastore": data.datastore
        
        }

@app.put("/data1/{data_id}")
async def updete1(data_id: str,data: Data):
    result = collection1.update_one({"_id": ObjectId(data_id)},{ "$push" : { "datastore" : { "$each" : data.datastore }}})
    result1 = collection1.update_one({"_id": ObjectId(data_id)},{"$set" : data.dict(exclude_unset=True)})
    if result and result1:
        return {       
        "id" :data_id ,
        "name" : data.name,
        "value" :data.value,
        "datastore" : data.datastore
        
        }
    else:
        raise HTTPException(status_code=404,detail="data not found")
    

@app.get("/data1/{data_id}")
async def read1(data_id: str):
    data = collection1.find_one({"_id": ObjectId(data_id)})
    if data:
        return {"id" : str(data["_id"]),"name" : data["name"],"value" : data["value"],"datastore" : data["datastore"]}
    else:
        raise HTTPException(status_code=404,detail="data not found")
    
# @app.get("/datastore/{data_id}")
# async def read1(data_id: str):
#     data = collection1.find_one({"_id": ObjectId(data_id)})
#     if data:
#         return {"id" : str(data["_id"]),"datastore" : data["datastore"]}
#     else:
#         raise HTTPException(status_code=404,detail="data not found")

    

# --------------------------------------------------------------------------------------------------------------------------------------

@app.post("/influx/query")
async def create(data: Influx):
    q = influxdb_query(data.field,data.bucket)
    return q

@app.post("/influx/write")
async def create(data: Influx1):
    p = influxdb_write(data.field,data.bucket,data.value)
    return p


# if __name__ == "__main__":
#     uvicorn.run(app, host="192.168.1.135", port =8080, reload=True)
