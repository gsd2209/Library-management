from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import BasicAuthentication
from .models import User, Book, BorrowRequest
from .serializers import UserSerializer, BookSerializer, BorrowRequestSerializer
from django.db.models import Q

# Librarian APIs
class CreateUserView(APIView):
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        data = request.data
        if not request.user.is_librarian:
            return Response({"error": "Unauthorized"}, status=403)
        
        password = make_password(data['password'])
        user = User.objects.create(username=data['username'], email=data['email'], password=password, is_librarian=False)
        return Response({"message": "User created successfully!"})

class ViewBorrowRequests(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        if not request.user.is_librarian:
            return Response({"error": "Unauthorized"}, status=403)
        
        requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(requests, many=True)
        return Response(serializer.data)

class ApproveDenyBorrowRequest(APIView):
    authentication_classes = [BasicAuthentication]

    def put(self, request, request_id):
        if not request.user.is_librarian:
            return Response({"error": "Unauthorized"}, status=403)

        borrow_request = BorrowRequest.objects.get(id=request_id)
        borrow_request.status = request.data['status']
        borrow_request.save()
        return Response({"message": f"Borrow request {borrow_request.status}!"})

class ViewUserHistory(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, user_id):
        if not request.user.is_librarian:
            return Response({"error": "Unauthorized"}, status=403)
        
        history = BorrowRequest.objects.filter(user_id=user_id)
        serializer = BorrowRequestSerializer(history, many=True)
        return Response(serializer.data)

# Library User APIs
class ListBooksView(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        books = Book.objects.filter(available=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class SubmitBorrowRequest(APIView):
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        data = request.data
        book = Book.objects.get(id=data['book_id'])

        # Check for overlapping borrow dates
        overlapping = BorrowRequest.objects.filter(
            book=book,
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date'],
            status='approved'
        )
        if overlapping.exists():
            return Response({"error": "Book is already borrowed during the requested dates."}, status=400)
        
        borrow_request = BorrowRequest.objects.create(
            user=request.user,
            book=book,
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        return Response({"message": "Borrow request submitted successfully!"})

class UserBorrowHistoryView(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        history = BorrowRequest.objects.filter(user=request.user)
        serializer = BorrowRequestSerializer(history, many=True)
        return Response(serializer.data)

