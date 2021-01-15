from django.urls import path, include
from rest_framework import routers

from .views import user_views, role_views, organization_views, menu_views, permission_views


router = routers.SimpleRouter()
router.register(r'users', user_views.UserViewSet, basename="users")
router.register(r'roles', role_views.RoleViewSet, basename="roles")
router.register(r'organizations', organization_views.OrganizationViewSet, basename="organizations")
router.register(r'menus', menu_views.MenuViewSet, basename="organizations")
router.register(r"permissions", permission_views.PermissionViewSet, basename="permissions")

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'auth/login/', user_views.UserAuthView.as_view()),
    path(r'auth/info/', user_views.UserInfoView.as_view()),
    path(r"auth/menu/", user_views.UserMenuView.as_view()),
    path(r"auth/change_password/", user_views.UserChangePasswordView.as_view()),
    path(r"auth/upload_avatar/", user_views.UserUploadImage.as_view()),
    path(r'api/organization/tree/', organization_views.OrganizationTreeView.as_view(), name='organizations_tree'),
    path(r'api/organization/user/tree/', organization_views.OrganizationUserTreeView.as_view(),
         name='organization_user_tree'),
    path(r'api/permission/tree/', permission_views.PermissionTreeView.as_view(), name="permission_tree"),

]