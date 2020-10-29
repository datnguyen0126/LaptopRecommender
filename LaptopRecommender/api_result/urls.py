from rest_framework import routers
from .views import ResultViewSet

app_name = 'api_result'

router = routers.DefaultRouter(trailing_slash=False)
router.register('', ResultViewSet, basename='result')

urlpatterns = router.urls
