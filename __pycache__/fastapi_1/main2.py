from fastapi import FastAPI, HTTPException
import random
import os
import json


app = FastAPI()



book_database =[
    "harry potter",
    "dune",
    "chronicals of narnia"
]
book_files = "book.json"
if os.path.exists(book_files):
    with open(book_files, "r") as f:
        try:
            book_database = json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON from file. Initializing with empty list.")

@app.get("/")
async def home():
    return {"message": "welcome to my book-store"}

@app.get("/book_list")
async def book_list():
    return{"books":book_database}

@app.get("/book_index/{index}")
async def book_index(index:int):
    if index<0 or index>len(book_database):
        return HTTPException(404, f"index (index) is out of range")
    else:
        return{"book":book_database[index]}
    
@app.get("/get_random")
async def get_random():
    return random.choice(book_database)


@app.post("/add_books")
async def add_book(book:str):
    book_database.append(book)
    with open(book_files,"w") as f:
        json.dump(book_database,f)
    return {"message": f"book {book} was added"}