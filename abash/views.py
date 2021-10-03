from django.shortcuts import render
from rest_framework.response import Response
from abash.models import *
from abash.serializers import *
from rest_framework.decorators import api_view,permission_classes
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q
# Create your views here. 
#Login Create
@api_view(['POST'])
def login_create(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            with transaction.atomic():
                user_instance = serializer.save()
                User_Details.objects.create(user= user_instance,first_name = user_instance.username, email=user_instance.email)

                data['response'] = "Registration Successful!"
                data['username'] = user_instance.username
                data['email'] = user_instance.email
                token = Token.objects.get(user=user_instance).key
                data['token'] = token

        else:
            data = serializer.errors
        
        return Response(data)

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("Logged Out")


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def user_settings(request,pk):
    if request.method == 'GET':
        user = User_Details.objects.get(pk=pk)
        serializer = UserSerialzer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        user = User_Details.objects.get(pk=pk)
        serializer = UserSerialzer(instance=user,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        user = User_Details.objects.get(pk=pk)
        user.delete()
        return Response('Deleted')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_property(request):
    if request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_property_image(request):
    if request.method == 'POST':
        serializer = PropertyImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_room(request):
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET'])
def get_room(request,arg):
    if request.method == 'GET':
        room= Room.objects.get(property_id=arg)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_location(request):
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET'])
def get_location(request,arg):
    if request.method == 'GET':
        location = Location.objects.get(property_id=arg)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def app_rating(request):
    if request.method == 'POST':
        serializer = AppRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
@api_view(['GET'])
def get_app_rating(request):   
    if request.method == 'GET':
        review = App_rating.objects.all()
        serializer = AppRatingSerializer(review, many = True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def property_rating(request):
    if request.method == 'POST':
        serializer = PropertyRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
@api_view(['GET'])
def get_property_rating(request):   
    if request.method == 'GET':
        review = Property_rating.objects.all()
        serializer = PropertyRatingSerializer(review, many = True)
        return Response(serializer.data)
def room_check(bed,bath,drawing_dining,balcony):
    room_given = True
    if bed is None or bath is None or drawing_dining is None or balcony is None:
        room_given = False
        return room_given
    else :
        return room_given


@api_view(['POST'])
def filter_property(request):
    if request.method == 'POST':
        serializer = FilterSerializer(data=request.data)
        if serializer.is_valid():
            filter_object = serializer.data
            room_status = room_check(filter_object['bedroom_no'],filter_object['bathroom_no'],filter_object['drawing_dining_no'],filter_object['balcony_no'])
            if room_status is True:
                if filter_object['area_sqft'] is not None and filter_object['rental_type'] is not None and filter_object['home_type'] is not None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['area_sqft'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['rental_type'] is None and filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max']))                  
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)

                elif filter_object['rental_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
            else :
                if filter_object['area_sqft'] is not None and filter_object['rental_type'] is not None and filter_object['home_type'] is not None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['area_sqft'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['rental_type'] is None and filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max']))                  
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)

                elif filter_object['rental_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
        else:
            return Response(serializer.errors)



@api_view(['GET'])
def location_search(request,search_topic):
    if request.method == 'GET':
        area_match = Location.objects.filter(Q(area__iexact = search_topic ) | Q(upazila__iexact = search_topic) | Q(district__iexact = search_topic) )
        properties = Property.objects.filter(pk__in = area_match).filter(rented = False)
        serializer = PropertySerializer(properties,many = True)
        return Response(serializer.data)

