from django.urls import path
from .views import hello, image_to_vector, get_initial_cloth_items, create_user, swipe, add_to_waitlist, remove_from_waitlist, get_waitlist_items

urlpatterns = [
    path("hello/", hello),
    path("image-to-vector/", image_to_vector),
    path("get-initial-cloth-items/", get_initial_cloth_items),
    path("create-user/", create_user),
    path("swipe/", swipe),
    path("waitlist/", add_to_waitlist),
    path("waitlist/user/<int:user_id>/", get_waitlist_items),
    path("waitlist/<int:waitlist_id>/", remove_from_waitlist),
]
