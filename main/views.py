from django.shortcuts import render
from main.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from collections import defaultdict
from rest_framework import status

import pandas as pd

# Create your views here.
def serve_bank_details(district):
    # BAnk details dataframe district wise
    bank_branch = BankBranch.objects.filter(district=district)
    bank_branch_list = list(bank_branch.values_list('id','district','district__name','bank','bank__bank_name','branch_name','ifsc_code','state__name','taluk','pincode','address','micr_code'))
    bank_branch_column = ['id','district_id','district_name','bank_id','bank_name','branch_name','ifsc_code','state_name','taluk','pincode','address','micr_code']
    bank_branch_df = pd.DataFrame(bank_branch_list, columns=bank_branch_column)
    
    master_dict = defaultdict(dict)
    for index, row in bank_branch_df.iterrows():
        if row['bank_name'] not in master_dict:
            master_dict[row['bank_name']] = defaultdict(dict)
        if row['branch_name'] not in master_dict[row['bank_name']]:
            master_dict[row['bank_name']][row['branch_name']] = defaultdict(dict)
        master_dict[row['bank_name']][row['branch_name']]['ifsc_code'] = row['ifsc_code']
        master_dict[row['bank_name']][row['branch_name']]['micr_code'] = row['micr_code']
    return master_dict


@api_view(['POST'])
@permission_classes((AllowAny,))
def serve_district_wise_bank_details(request):
    print(request.data)
    district = District.objects.get(name=request.data['city'])
    data = serve_bank_details(district)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def store_new_branch_details(request):
    print(request.data)
    district = District.objects.get(name=request.data['district_name'])
    bank = Bank.objects.get(bank_name=request.data['bank_name'])
    if BankBranch.objects.filter(ifsc_code=request.data['ifsc_code']).exists():
        print('already exist')
    else:
        bank_obj = BankBranch(district=district,
                                bank=bank,
                                branch_name=request.data['branch_name'],
                                ifsc_code=request.data['ifsc_code'],
                                state_id=23,
                                micr_code=request.data['micr_code'],
                                created_by=request.data['created_by'])

        bank_obj.save()
    data = serve_bank_details(district)
    return Response(data=data, status=status.HTTP_200_OK)

