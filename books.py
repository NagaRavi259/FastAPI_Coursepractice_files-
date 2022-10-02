from multiprocessing import current_process
from fastapi import FastAPI
from enum import Enum

## Assigning the class that we imported from the fastapi module to class instence variable
app = FastAPI()

books ={'book_1' : {"tittle" : 'tittle one'  ,"author" : 'author one'  },
        'book_2' : {"tittle" : "tittle two"  ,"author" : 'author two'  },
        'book_3' : {"tittle" : "title three" ,"author" : 'author three'},
        'book_4' : {"tittle" : "title four"  ,"author" : 'author Four' },
        'book_5' : {"tittle" : "tittle five" ,"author" : 'author five' }}


# returning the dictonary when the user call the api
@app.get("/")
async def read_All_books():
    return books
    

# This was using Path parameter as it was using the staic path in the path of the app.get function
@app.get("/books/mybook")
async def read_favorite_books():
    return {"book_title": books["book_3"]}


## This was using Quary Parameter as it has curly bracess in the path of the app.get function
@app.get("/books/{book_Id}")
async def read_book(book_id:int):
    return {"book_title": book_id}

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

@app.get("/direction/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction":direction_name, "sub":"Up"}
    if direction_name == DirectionName.south:
        return {"Direction":direction_name, "sub":"Down"}
    if direction_name == DirectionName.east:
        return {"Direction":direction_name, "sub":"Right"}
    if direction_name == DirectionName.west:
        return {"Direction":direction_name, "sub":"Left"}



## Taking ta input from the user using the key that we taken from the user using the quary parameters
@app.get("/{nbook_name}")
async def read_book(book_name:str):
    return books[book_name]



## _________________________________________________________##
# POST method
    # In here we are taking a input from a user by using the api and storing the 
    # data that we are fetching from the user and storing it into the dict
    # in similar we can also store the data into the database using the other modules to write a data into the data base
@app.post("/")
async def creat_book(book_title, book_author):
    currentbook_ID=0

    if len(books)>0:
        for book in books:
            x=int(book.split("_")[-1])
            if x > currentbook_ID:
                currentbook_ID=x
    books[f'book_{currentbook_ID+1}'] = {'title':book_title,'author':book_author}
    return books[f'book_{currentbook_ID+1}']
## _________________________________________________________##

##___________________________________________________________##
# With PUT method we updated the data that we fetch from the API user and
# UPdated our Dictonary with the detials that fetch from the user

@app.put("/book_name")
async def update_book(book_name:str,book_title:str ,book_author:str):
    book_info = {"tittle":book_title,'author':book_author}
    books[book_name] = book_info
    return book_info
##____________________________________________________________##

@app.delete("/book_name")
async def delete_book(book_name):  
    del books[book_name]
    return f'book {book_name} deleted.'

## PATH Paramaeter
    ## the path parameter is a fixed patch that takes inputs from the user that append to the link of that path

## query perameter
    ## Query parameter is a dynamically changing parameter this will change accourding to the inputs
    #  that user passed to the API when requesting the data


## To run this File we need to used command that
    # uvicorn books:app --reload
        # uvicorn was a import that need to build and register our server
        # books was a python file that we have created
        # we are registering the python file books to the app which was created in the puython file app=FastAPI()
        # --reload means to reaload the development server as we changing code very often in producion serverwe dont do reloads
