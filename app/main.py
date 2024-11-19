#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import mysql
import mysql.connector
from mysql.connector import Error


app = FastAPI()

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "eju2pk"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

@app.get("/")  # zone apex
def zone_apex():
    return {"Good Day": "Sunshine!"}

@app.get("/sum/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

from fastapi.middleware. cors import CORSMiddleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    
@app.get('/songs')
def get_songs():
    query = "Select * From songs ORDER BY id;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        print("MySQL Error: ", str(e))
        return {"Error": "MySQL Error: " + str(e)}  