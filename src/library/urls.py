from django.urls import path
from .views import (
    CreateUserView, ViewBorrowRequests, ApproveDenyBorrowRequest, ViewUserHistory,
    ListBooksView, SubmitBorrowRequest, UserBorrowHistoryView
)

urlpatterns = [
    # Librarian APIs
    path('librarian/create_user/', CreateUserView.as_view()),
    path('librarian/borrow_requests/', ViewBorrowRequests.as_view()),
    path('librarian/borrow_request/<int:request_id>/', ApproveDenyBorrowRequest.as_view()),
    path('librarian/user_history/<int:user_id>/', ViewUserHistory.as_view()),

    # Library User APIs
    path('books/', ListBooksView.as_view()),
    path('user/borrow_request/', SubmitBorrowRequest.as_view()),
    path('user/history/', UserBorrowHistoryView.as_view()),
]
