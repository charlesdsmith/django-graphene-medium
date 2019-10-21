# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import rest_framework
import urllib
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import GetAdesaPurchases, CarFax, GetRecalls, GetAdesaRunList, ShoppingList, DamageComparison
from .serializers import DamageComparisonSerializer, PurchasesSerializer, RecallsSerializer, CarFaxSerializer, AdesaRunlistSerializer, ShoppingListSerializer, AdesaRunListBulkUploadSerializer, PurchasesBulkUploadSerializer, CarFaxBulkUploadSerializer, RecallsBulkUploadSerializer
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers, authentication, status
from rest_framework.decorators import action
from rest_framework_bulk import ListBulkCreateAPIView
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from graphene_django.views import GraphQLView

# had to go online and download oauth2_provider manually, package installed oauth2_provider was missing files
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from oauth2_provider.views.generic import ProtectedResourceView


# How django knows which method to use for requests:
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/#django.views.generic.base.View.dispatch
# Create your views here.

class DOTAuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(DOTAuthenticatedGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(DOTAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated, TokenHasReadWriteScope, ))(view)  # add permissions to the view
        view = authentication_classes((OAuth2Authentication,))(view)
        view = api_view(['POST'])(view)
        return view

class getAdesaPurchases(viewsets.ModelViewSet):
    ''' The actions provided by the ModelViewSet class are .list(), .retrieve(),
      .create(), .update(), .partial_update(), and .destroy(). '''

    queryset = GetAdesaPurchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        # accessed at url: ^api/v1/purchases/$
        queryset = GetAdesaPurchases.objects.all()
        serializer = PurchasesSerializer(queryset, many=True)
        print('here')

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # accessed at url: ^api/v1/purchases/{pk}/$

        queryset = GetAdesaPurchases.objects.all()
        # https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/#get-object-or-404
        record = get_list_or_404(queryset, vin__exact=pk)
        # To serialize a queryset or list of objects instead of a single object instance,
        # you should pass the many=True flag when instantiating the serializer
        # https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-multiple-objects
        serializer = PurchasesSerializer(record, many=True)
        print('here')

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = RecallsSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)

    '''def create(self, request, **validated_data):
        serializer = PurchasesSerializer(GetAdesaPurchases.objects.create(**validated_data))
        headers = self.get_success_headers(serializer.data)

        print(headers)
        return Response(serializer.data, headers=headers)'''

class AdesaPurchasesBulkUpload(ListBulkCreateAPIView):
    queryset = GetAdesaRunList.objects.all()
    serializer_class = PurchasesBulkUploadSerializer

class AdesaRunList(viewsets.ModelViewSet):

    queryset = GetAdesaRunList.objects.all()
    serializer_class = AdesaRunlistSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def list(self, request):
        # accessed at url: ^api/v1/purchases/$
        queryset = GetAdesaRunList.objects.all()
        serializer = AdesaRunlistSerializer(queryset, many=True)
        print('here')

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # accessed at url: ^api/v1/purchases/{pk}/$
        print('here')
        queryset = GetAdesaRunList.objects.all()
        # https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/#get-object-or-404
        record = get_list_or_404(queryset, vin__exact=pk)
        # To serialize a queryset or list of objects instead of a single object instance,
        # you should pass the many=True flag when instantiating the serializer
        # https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-multiple-objects
        serializer = AdesaRunlistSerializer(record, many=True)
        print('here')

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = GetAdesaRunList.objects.all()
        record = get_object_or_404(queryset, vin__exact=pk)
        serializer = AdesaRunlistSerializer(record, data=request.data, partial=True)
        print("REQUEST",request.data)
        print("KWARGS", kwargs)
        print("ARGS", args)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = GetAdesaRunList.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = AdesaRunlistSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)



class BulkAdesaRunListUpload(ListBulkCreateAPIView):
    queryset = GetAdesaRunList.objects.all()
    serializer_class = AdesaRunListBulkUploadSerializer


class GetCarFax(viewsets.ModelViewSet):
    ''' This view will be used for GETing new carfax reports to the database '''

    required_scopes = ['write']  # necessary to specify what type of permission the token should have to access this endpoint
    queryset = CarFax.objects.all()
    serializer_class = CarFaxSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


    def list(self, request, **kwargs):

        # accessed at url: ^api/v1/carfax/$
        queryset = CarFax.objects.all()
        serializer = CarFaxSerializer(queryset, many=True)
        print(request.user)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # accessed at url: ^api/v1/retrieve/{pk}/$
        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = CarFaxSerializer(record, many=True)
        print('CARFAX RETRIEVE')

        return Response(serializer.data)

    def retrieve_by_rundate(self, request, rundate=None):
        # accessed at url: ^api/v1/retrieve/{pk}/$
        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, rundate__exact=rundate)
        serializer = CarFaxSerializer(record, many=True)

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = CarFax.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = CarFaxSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)

class CarFaxBulkUpload(ListBulkCreateAPIView):
    queryset = CarFax.objects.all()
    serializer_class = CarFaxBulkUploadSerializer


class Recalls(viewsets.ModelViewSet):
    '''
    This view will be fore retrieving a recall for a car from the database
    '''


    queryset = GetRecalls.objects.all()
    serializer_class = RecallsSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #lookup_field = "vin"


    def list(self, request, **kwargs):

        queryset = GetRecalls.objects.all()
        serializer = RecallsSerializer(queryset, many=True)
        print('LIST')

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = RecallsSerializer(record, many=True)


        print('RETRIEVE')

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        queryset = GetRecalls.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = RecallsSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)

class RecallsBulkUpload(ListBulkCreateAPIView):
    queryset = GetRecalls.objects.all()
    serializer_class = RecallsBulkUploadSerializer

class ShoppingListView(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #lookup_field = "vin"

    def list(self, request, **kwargs):

        queryset = ShoppingList.objects.all()
        serializer = ShoppingListSerializer(queryset, many=True)
        print('LIST')

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = ShoppingList.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        serializer = ShoppingListSerializer(record, many=True)

        print('RETRIEVE ONE')

        return Response(serializer.data)



    @action(methods=['GET'], detail=False, url_path='retrieve_by_rundate/(?P<pk>[^/.]+)')
    def retrieve_by_rundate(self, request, pk=None, *args, **kwargs):

        ''' Shopping List by "Run Date" '''

        queryset = ShoppingList.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, run_date__exact=pk)
        serializer = ShoppingListSerializer(record, many=True)
        print('RETRIEVE RUNDATE')

        return Response(serializer.data)

class DamageComparisonView(viewsets.ModelViewSet):
    ''' The actions provided by the ModelViewSet class are .list(), .retrieve(),
      .create(), .update(), .partial_update(), and .destroy(). '''

    queryset = DamageComparison.objects.all()
    serializer_class = DamageComparisonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        # accessed at url: ^api/v1/purchases/$
        queryset = DamageComparison.objects.all()
        serializer = DamageComparisonSerializer(queryset, many=True)
        print('here damage list')

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # accessed at url: ^api/v1/purchases/{pk}/$
        queryset = DamageComparison.objects.all()
        # https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/#get-object-or-404
        record = get_list_or_404(queryset, vin__exact=pk)
        # To serialize a queryset or list of objects instead of a single object instance,
        # you should pass the many=True flag when instantiating the serializer
        # https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-multiple-objects
        serializer = DamageComparisonSerializer(record, many=True)
        print('here')

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='retrieve_by_vin/(?P<pk>[^/.]+)')
    def retrieve_by_vin(self, request, pk=None, *args, **kwargs):
        queryset = DamageComparison.objects.all()
        #record = get_list_or_404(queryset, self.kwargs)
        record = get_list_or_404(queryset, vin__exact=pk)
        print('RETRIEVE VIN')
        serializer = DamageComparisonSerializer(record, many=True)
        vinData = serializer.data[0]
        print(serializer.data[0]['vin'])
        HTML_TEMPLATE = """<html><head></head><body style="display:flex;flex-direction:column" ><iframe style="display:flex;flex:1" src="https://openauctionca.prod.nw.adesa.com/mfe/vdp?vehicleId=@@ADESAID@@"></iframe>
           <iframe style="display:flex;flex:1" src=data:text/html;charset=utf-8,@@CARFAXHTML@@></iframe>
           
        </body></html>"""
        cleanCarfaxHTML = vinData['carfax']
        # cleanCarfaxHTML = "<div>hello</div>"
        cleanCarfaxHTML = cleanCarfaxHTML.replace(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
        cleanCarfaxHTML = urllib.parse.quote(cleanCarfaxHTML)
        # cleanCarfaxHTML.encode(
        #     encoding='UTF-8')
        HTML_TEMPLATE = HTML_TEMPLATE.replace(
            "@@CARFAXHTML@@", cleanCarfaxHTML)
        HTML_TEMPLATE = HTML_TEMPLATE.replace(
            "@@ADESAID@@", vinData['adesa_id'])

        return HttpResponse(HTML_TEMPLATE)

    '''def create(self, request, **validated_data):
        serializer = PurchasesSerializer(GetAdesaPurchases.objects.create(**validated_data))
        headers = self.get_success_headers(serializer.data)
    ​
        print(headers)
        return Response(serializer.data, headers=headers)'''