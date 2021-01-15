from django.urls import path, include
from rest_framework import routers

from cmdb.views import business_views, group_views, cabinet_views, host_views, label_views
from rbac.views import menu_views

router = routers.SimpleRouter()
router.register(r'businesses', business_views.BusinessViewSet, basename="businesses")
router.register(r'groups', group_views.DeviceGroupViewSet, basename="devicegroups")
router.register(r'labels', label_views.LableViewSet, basename='labels')
router.register(r'cabinets', cabinet_views.CabinetViewSet, basename='cabinets')
router.register(r'hosts', host_views.HostViewSet, basename='hosts')

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/host_ip/list', host_views.HostListView.as_view(), name="host_ip_list"),
    path(r'api/import_excel', host_views.ImportExcelView.as_view(), name="import_excel"),
    path(r'api/menu/tree/',  menu_views.MenuTreeView.as_view(), name='menus_tree'),

]