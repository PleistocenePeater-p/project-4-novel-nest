from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Genre, CreditCard
from .forms import CreditCardForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Log a user in
            login(request, user)
            return redirect('login')
        else:
            error_message = 'Invalid sign up'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def addpayment(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    credit_card_form = CreditCardForm()
    return render(request, 'main_app/creditcard_form.html', {'genre': genre, 'credit_card_form': credit_card_form})


class GenreList(ListView):
    model = Genre


class GenreDetail(DetailView):
    model = Genre


def create_creditcard(request):
    form = CreditCardForm(request.POST)
    if form.is_valid():
        print(request.user.id)
        new_creditcard = form.save(commit=False)
        new_creditcard.user_id = request.user.id
        new_creditcard.save()
    else:
        return redirect("/")
    return redirect("genres_index")
