from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'

class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/about.html'

class BlogListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/blog_list.html'

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/blog_detail.html'

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name = 'app/blog_create.html'

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name = 'app/blog_update.html'

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'app/blog_delete.html'
    success_url = reverse_lazy('blog')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserCreationForm()

    return render(request, 'app/signup.html', {'form': form})

@login_required()
def profile_view(request):
    return render(request, 'app/profile.html')

@login_required
def dashboard(request):
    budgets = Budget.objects.filter(user=request.user)

    category_filter = request.GET.get('category')
    date_filter = request.GET.get('start_date')

    if category_filter:
        budgets = budgets.filter(expenses__category__name=category_filter)

    if date_filter:
        budgets = budgets.filter(start_date__gte=date_filter)

    return render(request, 'app/dashboard.html', {'budgets': budgets})

# Create a new budget
@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'app/create_budget.html', {'form': form})

# Add an expense to a specific budget
@login_required
def add_expense(request, budget_id):
    budget = Budget.objects.get(id=budget_id)
    if budget.user != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.budget = budget
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'app/add_expense.html', {'form': form, 'budget': budget})


