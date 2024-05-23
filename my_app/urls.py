from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sing_up'),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('item/', views.Home.as_view(), name='index'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('inventories/', views.InventoriesViwe.as_view(), name='inventories'),
    path('desbord/', views.DashboardView.as_view(), name='desbord'),
    path('add/', views.AddItemViwe.as_view(), name='add_invantoris'),
    path('update/<pk>', views.EditViwe.as_view(), name='update'),
    path('delete/<pk>', views.InventoriesDeleteView.as_view(), name='delete'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    # path('search/', views.SearchView.as_view(), name='search'),
]
