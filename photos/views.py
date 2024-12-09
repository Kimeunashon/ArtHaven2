from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to 'next' parameter or default to 'gallery'
            next_url = request.GET.get('next', 'gallery')
            return redirect(next_url)
        else:
            context = {'error': 'Invalid username or password', 'page': page}
            return render(request, 'photos/login_register.html', context)

    return render(request, 'photos/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            # Redirect to 'next' parameter or default to 'gallery'
            next_url = request.GET.get('next', 'gallery')
            return redirect(next_url)  # Redirect to the specified URL or 'gallery' if not specified

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    category = request.GET.get('category')
    if category is None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def addPhoto(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        Photo.objects.create(
            category=category,
            description=data['description'],
            image=image
        )
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
