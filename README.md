A Library Management System backend built with Django and Django REST Framework (DRF), which allows librarians to manage users, books, and borrowing requests. Library users can browse books, request books for borrowing, and view their borrowing history.

Features
Librarian APIs:
Create Library User: Add a new library user with an email and password.
View Borrow Requests: See all book borrowing requests.
Approve/Deny Borrow Requests: Manage borrowing requests (approve or deny them).
View User's Borrow History: Access borrowing history for specific users.

Library User APIs:
List Books: View all available books in the library.
Borrow Books: Submit requests to borrow books for specific dates.
Borrow History: View personal borrowing history.


API Endpoints
Authentication
Login: Basic Authentication (username and password).

Librarian APIs
Method	Endpoint	Description
POST	/api/library/create-user/	Create a new library user.
GET	/api/library/borrow-requests/	View all borrow requests.
POST	/api/library/approve-request/<pk>/	Approve or deny a borrow request.
GET	/api/library/user-history/<user_id>/	View a user's borrowing history.

Library User APIs
Method	Endpoint	Description
GET	/api/library/books/	List all available books.
POST	/api/library/borrow-request/	Submit a borrow request for a book.
GET	/api/library/my-history/	View the user's borrowing history.
