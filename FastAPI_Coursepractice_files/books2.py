from dataclasses import field
from importlib.resources import contents
from logging import exception 
                        ## field is used to create a limits to create limits for user inputs in payload as user enters 
                        # they might send the empty or larger texts or different datatypes when requested with fields module
                        # we can restrict or raise error when wrong data was sent 
from typing import Optional
from urllib import request
                    ## with the optional method we can pass optional arguments in a class so when user dont have that info
                    # he can leav it as empty

from starlette.responses import JSONResponse

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
                            ## HTTPExecption is used to raise an execption when any error ocoured

from pydantic import BaseModel, Field
                    ##
from uuid import UUID
                ## UUID is used to generate a different UUID's every time

app= FastAPI()

class NegativeNumberExecption(Exception):
    def __init__(self, books_to_return):
        self.books_to_return =books_to_return

class book_no_rating(BaseModel):
    id:UUID
    title:str=Field(min_length=1)
    author: str
    description:Optional[str]=Field(
        None, title="Description of a book ",
        max_length=100,
        min_length=1
    )


##________________________________________________________________##
class book(BaseModel):
    id: UUID
    title: str = Field(min_length=1) # this will check the length of the input that 
                                        #we got from the user and if it is lessthen the prefered lenth it will throughs an error with length
    author: str = Field(min_length=1,max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                            max_length=100,
                            min_length=1)
    rating: int = Field(gt=-1, lt=101) 
    # gt means greaterthen and lt means lessthen 

##________________________________________________________________##
    class Config:
        schema_extra = {
            "example":{
                "id":"be6a235a-2968-11ed-a261-0242ac120002",
                "title":"Config title",
                "author":"Coading ravi",
                "description":"A sample Description of a book",
                "rating":"Rating between 1 to 100"
            }
        }
## The above code will replace a examplecode in the swagarUI with data parameters and detials that w given in classconfig 
##_________________________________________________________________##

# WE created a base Model (AKA: template) for the data that we want to 
# request from the user that request the information through api
# IF the user failed to give the any fields that we mentioned above and
# if we want a field as a optional we need to enclose perameter type in in  a Square brackets
#  given incorrect information it will through an error 422
##_________________________________________________________________##

books = []

##____________Form fils with fast api_______##
@app.post("/books/login")
async def book_login(book_id : int ,username : Optional[str] = Header(None), password : Optional[str] = Header(None)):
    if username=='FastAPIuser' and password == 'test1234':
        return books[book_id]
    else:
        return 'Invalid User'
    # return {"username":username,"password":password}


@app.get("/headers")
async def read_header(random_header : Optional[str] = Header(None)):
    return{"Random_header":random_header}

@app.exception_handler(NegativeNumberExecption)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberExecption):
    return JSONResponse(
        status_code=418,
        content = {"message":f"Hey why do you want {exception.books_to_return} "
                    f"books? you need to read more!"}   
    )

@app.get("/")
async def read_books(books_to_return: Optional[int]=None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberExecption(books_to_return=books_to_return)

    if len(books)<1:
        Create_books_no_api()
    
    if books_to_return and len(books)>=books_to_return>0:
        i=1 
        new_books=[]
        while i<=books_to_return:
            new_books.append(books[i-1])
            i += 1
        return new_books
    return books


## api




##__________________________________________________________##

@app.post("/")
async def create_book(book: book):
    books.append(book)
    return book

# the above API will passes the template with a required fields that 
# we specified in book class and append that information to the books dict 
# it can be empty but key can not be removed(Deleted) from the JSON(AKA: Dictonary)
##__________________________________________________________##

##___________________________________________________##
@app.post("/",status_code=status.HTTP_201_CREATED)
async def create_book(book: book):
    books.append(book)
    return book

##___________________________________________________##

def Create_books_no_api():
    book_1=book(id="ce6a235a-2968-11ed-a261-0242ac120002",
        title="title_1",
        author="author_1",
        description ="Description 1",
        rating= 90)
    book_2=book(id="c6a08966-2968-11ed-a261-0242ac120002",
        title="title_2",
        author="author_2",
        description ="Description 2",
        rating = 50 
        )
    book_3=book(id="b9147032-2968-11ed-a261-0242ac120002",
        title="title_3",
        author="author_3",
        description ="Description 3",
        rating = 60 
        )
    book_4=book(id="d725af96-2968-11ed-a261-0242ac120002",
        title="title_4",
        author="author_4",
        description ="Description 4",
        rating = 70 
        )
    book_5=book(id="a58513a0-2968-11ed-a261-0242ac120002",
        title="title_5",
        author="author_5",
        description ="Description 5",
        rating = 80 
        )
    books.append(book_1)
    books.append(book_2)
    books.append(book_3)
    books.append(book_4)
    books.append(book_5)

# Create_books_no_api()
##________________________________________________##

##____________________________________________________##
@app.get("/book/{bookid}")
async def read_book(book_id:UUID):
    for x in books:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found()

## featching a book by using the UUID that was generated when the book was created
##_____________________________________________________##

@app.get("/book/rating/{bookid}",response_model=book_no_rating)
async def read_book_no_rating(book_id:UUID):
    for x in books:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found()

##____________________________________________________##
@app.put("/{book_id}")
async def  update_book(book_id:UUID,book:book):
    counter = 0
    for x in books:
        counter += 1
        if x.id==book_id:
            books[counter - 1]=book
            return books[counter - 1]
    raise raise_item_cannot_be_found()

## The above function featches the book id and a data from the user as a payload and
#  stores check for UUID matches book and updates the book with the user given detials
##_____________________________________________________##


##________________________________________________##
@app.delete("/{book_id}")
async def delete_book(book_id:UUID):
    counter = 0
    for x in books:
        counter += 1
        if x.id==book_id:
            del books[counter - 1]
            return f'ID:{book_id} deleted'

    raise raise_item_cannot_be_found() # insted of using below aproach we created 
                                       # seperate function to return error that we defined

    # raise HTTPException(status_code=404, detail='book not found'
    #                     , headers={"X-Header-Error":"Nothing to be seen at the UUID"})
                        ## Headers are used to give the information in response headers about the API to a developer

## the above function fetches the uuid from the user as a quary parameter and 
# itterate through the books list and fetches the book with uuid matched and 
# delete that boook and returns the UUID and message as deleted
##________________________________________________##

def raise_item_cannot_be_found():
    return HTTPException(status_code=404,
                        detail="book not found at",
                        headers={"X-header_error":"Nothing to be seen at the uuid"})


