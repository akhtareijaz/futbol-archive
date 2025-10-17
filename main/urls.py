from django.urls import path
from main.views import show_main, show_json, show_json_by_id, show_xml, show_xml_by_id, create_product, show_product, register, login_user, logout_user, edit_product, delete_product, add_product_entry_ajax, edit_product_ajax, delete_product_ajax, login_ajax, register_ajax, get_product_by_id_json, get_products_json

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<int:id>/edit', edit_product, name='edit_product'),
    path('product/<int:id>/delete', delete_product, name='delete_product'),
    path('create-product-ajax', add_product_entry_ajax, name="add_product_entry_ajax"),
    path('edit-product-ajax/<int:id>/', edit_product_ajax, name='edit_product_ajax'),
    path('delete-product-ajax/<int:id>/', delete_product_ajax, name="delete_product_ajax"),
    path("login-ajax/", login_ajax, name="login_ajax"),
    path("register-ajax/", register_ajax, name="register_ajax"),
    path('get-product/<int:id>/', get_product_by_id_json, name='get_product_by_id_json'),
    path("get-products/", get_products_json, name="get_products_json"),
]