from django.urls import path
from . import views
from .views import (HomePageView, AboutPageView, BlogListView,
                    BlogDetailView, BlogCreateView, BlogUpdateView,
                    BlogDeleteView)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/edit', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name='blog_delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-budget/', views.create_budget, name='create_budget'),
    path('add-expense/<int:budget_id>/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('edit-budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('delete-budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
]