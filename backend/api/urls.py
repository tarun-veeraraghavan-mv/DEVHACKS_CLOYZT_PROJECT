from django.urls import path
from .views import hello, image_to_vector, get_initial_cloth_items

urlpatterns = [
    path("hello/", hello),
    path("image-to-vector/", image_to_vector),
    path("get-initial-cloth-items/", get_initial_cloth_items),
]