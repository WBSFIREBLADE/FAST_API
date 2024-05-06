from fastapi import FastAPI, HTTPException
import random
import os
import json

app = FastAPI()
book_file = "book.json"

book_database = [
    "game of thrones",
    "kin kong"
]

# This block of code overwrites book_database if the file exists
if os.path.exists(book_file):
    with open(book_file, "r") as f:
        try:
            book_database = json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON from file. Initializing with empty list.")


@app.get("/")
async def home():
    return {"message": "Welcome to my book-store"}

@app.get("/book_list")
async def book_list():
    return {"books": book_database}

@app.get("/book_index/{index}")
async def book_index(index: int):
    if index < 0 or index >= len(book_database):
        raise HTTPException(status_code=404, detail=f"Book with index {index} not found")
    else:
        return {"book": book_database[index]}

@app.get("/get_random")
async def get_random():
    if not book_database:
        raise HTTPException(status_code=404, detail="No books available")
    return random.choice(book_database)

@app.post("/add_book")
async def add_book(book: str):
    book_database.append(book)
    with open(book_file, "w") as f:
        json.dump(book_database, f)  # Save the updated list to the file
    return {"message": f"Book '{book}' was added"}
