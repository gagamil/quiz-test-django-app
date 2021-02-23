# from django.shortcuts import render
from rest_framework.permissions import BasePermission

from .models import User


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_ADMINISTRATOR