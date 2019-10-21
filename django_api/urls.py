"""django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter
from graphene_django.views import GraphQLView
from api import views

router = routers.DefaultRouter()
router.register(r'purchases', views.getAdesaPurchases)
router.register(r'carfax', views.GetCarFax)
router.register(r'recalls', views.Recalls)
router.register(r'adesa_run_list', views.AdesaRunList)
router.register(r'shopping_list', views.ShoppingListView),
router.register(r'damages', views.DamageComparisonView)

bulk_router = BulkRouter()
bulk_router.register(r'adesa_run_list_bulk_upload', views.BulkAdesaRunListUpload)

admin.autodiscover()


from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    #path('api/v1/adesa_run_list/update-partial/(?P<pk>\d+)/$', views.AdesaRunList.as_view(), name='runlist_partial_update'),
    path('api/v1/adesa_run_list_bulk_upload/', views.BulkAdesaRunListUpload.as_view()),
    path('api/v1/adesa_purchases_bulk_upload/', views.AdesaPurchasesBulkUpload.as_view()),
    path('api/v1/carfax_bulk_upload/', views.CarFaxBulkUpload.as_view()),
    path('api/v1/recalls_bulk_upload/', views.RecallsBulkUpload.as_view()),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('graphqlui', views.GraphQLView.as_view(graphiql=True)),
    path('graphql', views.GraphQLView.as_view(graphiql=True)),

]
