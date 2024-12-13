from django.urls import path
from .views import (
    CreateUserView, BorrowRequestListView, ApproveDenyRequestView,
    UserBorrowHistoryView, BookListView, SubmitBorrowRequestView, PersonalBorrowHistoryView
)

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('borrow-requests/', BorrowRequestListView.as_view(), name='borrow_requests'),
    path('approve-deny-request/<int:pk>/', ApproveDenyRequestView.as_view(), name='approve_deny_request'),
    path('user-history/<int:user_id>/', UserBorrowHistoryView.as_view(), name='user_borrow_history'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('borrow-request/', SubmitBorrowRequestView.as_view(), name='submit_borrow_request'),
    path('personal-history/', PersonalBorrowHistoryView.as_view(), name='personal_borrow_history'),
]
