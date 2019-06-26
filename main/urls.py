from django.conf.urls import url
from main import views


urlpatterns = [
    url(r'^serve/district/wise/bank/details/$', views.serve_district_wise_bank_details),
    url(r'^store/new/branch/details/$', views.store_new_branch_details),
] 