from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Umbrella, Reservation
from .serializers import ReservationSerializer, UserSerializer
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
# 예약 후 Kafka 메시지 전송 예시

# Create your views here.
@api_view(['GET'])
def helloAPI(request):
    return Response("Test Project")

# 삽입 요청 처리 함수 
@api_view(['POST'])
def userAPI(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 삽입 요청 처리 함수 
@api_view(['POST'])
def umbrellaAPI(request):
    umbrella_code = request.data.get('umbrella_code')
    if not umbrella_code:
        return Response({'error': 'Umbrella code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    umbrella, created = Umbrella.objects.get_or_create(umbrella_code=umbrella_code, defaults={'is_available': True})
    if created:
        return Response({'message': 'Umbrella created successfully.', 'umbrella_code': umbrella.umbrella_code}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Umbrella already exists.', 'umbrella_code': umbrella.umbrella_code}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reservationsAPI(request):
    user_id = request.data.get('user_id')
    umbrella_code = request.data.get('umbrella_code')

    # Validate inputs
    if not user_id or not umbrella_code:
        return Response({'error': 'User ID and Umbrella Code are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if User exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if Umbrella exists
    try:
        umbrella = Umbrella.objects.get(umbrella_code=umbrella_code)
    except Umbrella.DoesNotExist:
        return Response({'error': 'Umbrella not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the umbrella is available
    if not umbrella.is_available:
        return Response({'error': 'Umbrella is not available.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a Reservation
    reservation = Reservation.objects.create(
        user=user,
        umbrella=umbrella,
        status='success'  # Assume reservation is successful at this point
    )

    # Mark the umbrella as unavailable
    umbrella.is_available = False
    umbrella.save()

@api_view(['GET', 'PUT'])
def reservationStatusAPI(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'reservation_id': reservation.id, 'status': reservation.status})

    if request.method == 'PUT':
        new_status = request.data.get('status')
        if new_status not in ['pending', 'success', 'failed']:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = new_status
        reservation.save()
        return Response({'message': 'Reservation status updated.', 'new_status': reservation.status})

@api_view(['POST'])
def cancelReservationAPI(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)

    if reservation.status == 'failed':
        return Response({'error': 'Cannot cancel a failed reservation.'}, status=status.HTTP_400_BAD_REQUEST)

    # Mark the reservation as 'failed' and make the umbrella available
    reservation.status = 'failed'
    reservation.umbrella.is_available = True
    reservation.umbrella.save()
    reservation.save()

    return Response({'message': 'Reservation cancelled and umbrella is now available.'})
