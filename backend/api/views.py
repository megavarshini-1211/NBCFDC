# api/views.py

from rest_framework import generics, viewsets
from .models import (
    Beneficiary, Loan, EmiDetail, AccountTransaction, 
    MobileRecharge, ElectricityBill, RationCard, PDSTransaction, UtilityBill
)
from .serializers import (
    BeneficiarySerializer, LoanSerializer, EmiDetailSerializer,
    AccountTransactionSerializer, MobileRechargeSerializer, ElectricityBillSerializer,
    RationCardSerializer, PDSTransactionSerializer, UtilityBillSerializer
)

import os
import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import * # Import your existing models
from .serializers import * # Import your existing serializers

# --- CSV Data Loading ---
# This code runs only ONCE when the Django server starts.
try:
    scores_csv_path = os.path.join(settings.BASE_DIR, 'beneficiary_scores.csv')
    # Load the scores and set 'beneficiary_id' as the index for fast lookups
    df_scores = pd.read_csv(scores_csv_path).set_index('beneficiary_id')
    print("Beneficiary scores CSV loaded successfully into memory.")
except FileNotFoundError:
    print(f"CRITICAL ERROR: 'beneficiary_scores.csv' not found in the project root directory.")
    df_scores = None

# --- API View for fetching scores ---
class GetBeneficiaryScore(APIView):
    """
    An API endpoint to retrieve a pre-calculated score for a beneficiary
    by looking it up in the loaded scores CSV file.
    """
    def get(self, request, beneficiary_id, format=None):
        if df_scores is None:
            return Response(
                {"error": "Server configuration error: Score data not loaded."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Look up the beneficiary ID in the dataframe's index
            score_data = df_scores.loc[beneficiary_id.upper()] # Convert to uppercase to be safe

            # Create the response object
            response_data = {
                'beneficiary_id': beneficiary_id.upper(),
                'score': int(score_data['score']),
                'risk_band_class': score_data['risk_band_class']
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except KeyError:
            # This error occurs if the beneficiary_id is not in the index
            return Response(
                {"error": f"Beneficiary with ID '{beneficiary_id}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

# --- ADD NEW VIEWSETS FOR ALL OTHER MODELS ---

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class EmiDetailViewSet(viewsets.ModelViewSet):
    queryset = EmiDetail.objects.all()
    serializer_class = EmiDetailSerializer

class AccountTransactionViewSet(viewsets.ModelViewSet):
    queryset = AccountTransaction.objects.all()
    serializer_class = AccountTransactionSerializer

class MobileRechargeViewSet(viewsets.ModelViewSet):
    queryset = MobileRecharge.objects.all()
    serializer_class = MobileRechargeSerializer

class ElectricityBillViewSet(viewsets.ModelViewSet):
    queryset = ElectricityBill.objects.all()
    serializer_class = ElectricityBillSerializer

class RationCardViewSet(viewsets.ModelViewSet):
    queryset = RationCard.objects.all()
    serializer_class = RationCardSerializer

class PDSTransactionViewSet(viewsets.ModelViewSet):
    queryset = PDSTransaction.objects.all()
    serializer_class = PDSTransactionSerializer

class UtilityBillViewSet(viewsets.ModelViewSet):
    queryset = UtilityBill.objects.all()
    serializer_class = UtilityBillSerializer