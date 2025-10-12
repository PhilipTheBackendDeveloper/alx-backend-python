#!/usr/bin/env python3
"""Project-level URL routing for messaging_app."""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),                # API routes for chats app
    path("api-auth/", include("rest_framework.urls")),  # Browsable API login/logout (optional)

    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
