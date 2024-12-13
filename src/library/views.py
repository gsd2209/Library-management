from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Book, BorrowRequest
from .serializer import UserSerializer, BookSerializer, BorrowRequestSerializer


# Create a new library user
class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get all borrow requests (Librarian only)
class BorrowRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_librarian:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        borrow_requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(borrow_requests, many=True)
        return Response(serializer.data)

# Approve or deny a borrow request
class ApproveDenyRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_librarian:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        try:
            borrow_request = BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            return Response({'error': 'Borrow request not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_choice = request.data.get('status')
        if status_choice not in ['approved', 'denied']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        borrow_request.status = status_choice
        borrow_request.save()
        return Response({'message': f'Request {status_choice} successfully'}, status=status.HTTP_200_OK)

# View a user's borrow history
class UserBorrowHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if not request.user.is_librarian:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        borrow_history = BorrowRequest.objects.filter(user_id=user_id)
        serializer = BorrowRequestSerializer(borrow_history, many=True)
        return Response(serializer.data)

# Get list of books
class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# Submit a borrow request
class SubmitBorrowRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # Attach the logged-in user
        serializer = BorrowRequestSerializer(data=data)
        if serializer.is_valid():
            # Check for overlapping borrow dates
            book_id = serializer.validated_data['book'].id
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            overlapping_requests = BorrowRequest.objects.filter(
                book_id=book_id,
                status='approved',
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            if overlapping_requests.exists():
                return Response({'error': 'Book is already borrowed for the selected dates'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View personal borrow history
class PersonalBorrowHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        borrow_history = BorrowRequest.objects.filter(user=request.user)
        serializer = BorrowRequestSerializer(borrow_history, many=True)
        return Response(serializer.data)
