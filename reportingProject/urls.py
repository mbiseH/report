from django.contrib import admin
from django.urls import path
from django.urls import path
# from CRUD_BACKEND import schema as views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("report", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # path('export/download', views.export_write_xls, name='export'),
    # path('export/excel-styling', views.export_styling_xls, name='export_styling_excel'),
]

