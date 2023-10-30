# Python
from typing import Optional
# DRF
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models.functions import Lower
from django.db.models import Q
# LOCAL
# from .models import ()
# from .serializers import()