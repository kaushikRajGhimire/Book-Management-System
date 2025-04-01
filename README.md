CLONE THIS REPO AND use "uv sync" to setup all dependencies and make virtual environment. Now use "uvicorn app.main:app --reload" to run the project.


First the user registers in the application using the “/register” endpoint.
Here, he would enter his username,email and password. His credentials would be stored in the MongoDB database “user_collection” if he was not registered earlier along with his hashed password.

After that the “/token” endpoint is used to login to the application by taking the data like username,email from the the Form submitted and the data is taken directly using Depends(). If he is authenticated user from the JWT token then it returns the access_token and token_type:”bearer” as response.

This JWT token was created from the auth.py file in the core. It has mainly 3 functions that is used to create_password using hashing, verify_password to verify the plain and hashed password and finally create_token using the SECRET KEY and ALGORITHM like HS256 from the .env file.

The database connection is made in the database.py file where the connection is made with the MongoDB so that it can store both the users data and the books data using the users_collection and books_collection.

The user.py and book.py is used to define the Data Validation using the pydantic model with the Field class so that we can impose constraints on the input of the user and EmailStr for the email validation.

So now when the user is logged in we can allow him to do the CRUD operations on the books. However, we must test only the logged in user is allowed to do the CRUD. Also updating and deleting can only be done by the registered user who is currently logged.

Moreover, the routes is made for the APIs for the user registry and authentication using auth.py and the books CRUD operations using book.py in api.

At the end, in the main.py app instance is made from the FastAPI and the routes are included i.e. 2 of them auth.router and book.router with the tags “Authentication” and “Books”. 

These are the API Endpoints and the HTTP methods for the CRUD Operations:
            CRUD operations:
Create a Book (POST /books/)
Adds a new book to the database (only accessible to authenticated users).
Retrieve Books (GET /books/)
Returns a list of all books stored in the database.
Retrieve a Single Book (GET /books/{book_id})
Fetches a book by its unique ID.
Update a Book (PUT /books/{book_id})
Updates book details (only by the logged-in user who created the book).
Delete a Book (DELETE /books/{book_id})
Removes a book from the database (only by the logged-in user who created the book).
API Routing (api/auth.py and api/book.py)
Authentication Routes (auth.py)
Handles user registration (/register)
Handles login and JWT token issuance (/token)
Book Routes (book.py)
Manages all CRUD operations on books.
Ensures authentication is required for modification operations
