
from django.urls import path
from . views import HomeView,Initial,DetailTripView,AddTripView,DeleteTripView,UpdateTripView,EditSitsView,BookView,CreateSitView,ListOfSits,DeleteSitView,ThanksView,CreateABookView,ShowAllOrdersView,DeleteBookView

urlpatterns = [
    path('',Initial,name='initial'),
    path('home/', HomeView,name='home'),
    path("trip/<int:pk>",DetailTripView.as_view(),name='trip_details'),
    path("create_trip",AddTripView.as_view(),name="create_trip"),
    path('delete_trip/<int:pk>',DeleteTripView.as_view(),name='delete_trip'),
    path('edit_trip/<int:pk>',UpdateTripView.as_view(),name='edit_trip'),
    path('edit_sits/<int:pk>',EditSitsView,name='edit_sits'),
    path('booking/<int:pk>',BookView,name='book'),
    path('create_sit/<int:pk>',CreateSitView.as_view(),name="create_sits"),
    path('list_of_sits/<int:pk>',ListOfSits.as_view(),name='list_of_sits'),
    path('delete_sit/<int:pk>',DeleteSitView.as_view(),name='delete_sit'),
    path('thanks/',ThanksView,name='thanks'),
    path('book/<int:pk>',CreateABookView,name='create_a_book'),
    path('orders',ShowAllOrdersView,name='showorders'),
    path('delete_an_order/<int:pk>',DeleteBookView.as_view(),name='delete_book')




]