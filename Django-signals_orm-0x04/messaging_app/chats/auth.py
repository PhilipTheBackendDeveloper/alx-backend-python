from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# No need to subclass unless you want custom claims
# But you can extend if you want extra fields in the token
