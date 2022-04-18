from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.predicting.predictioner import Predictioner
from .predicting.modelcreators.charactermodel import create_model as create_character


@api_view(['POST'])
def predict_breed(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    prediction = Predictioner(request.POST, request.FILES.getlist('images')).get_prediction()
    print(prediction)

    return Response(prediction)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def character_model_create(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    response = create_character()
    return Response({'Test Loss': response[0], 'Test Accuracy': response[1], 'Time': response[2]})
