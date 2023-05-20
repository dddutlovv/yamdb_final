from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from api.views import TitleViewSet, CategoryViewSet, GenreViewSet
from reviews.views import CommentViewSet, ReviewViewSet
from users.views import RegisterViewSet, TokenViewSet

router = DefaultRouter()

router.register(
    'users',
    UserViewSet
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    'auth/signup',
    RegisterViewSet,
    basename='signup'
)
router.register(
    'auth/token',
    TokenViewSet,
    basename='token'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include(router.urls)),
]
