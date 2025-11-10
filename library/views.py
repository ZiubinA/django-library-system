from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Loan, BookMessage
from django.contrib.auth.models import User

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

def is_patron(user):
    return user.groups.filter(name='Patron').exists()

@login_required
def home(request):
    if request.user.is_superuser: return redirect('/admin/')
    elif is_librarian(request.user): return redirect('librarian_dashboard')
    elif is_patron(request.user): return redirect('patron_dashboard')
    else: return render(request, 'library/home.html')

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            BookMessage.objects.create(book=book, patron=request.user, message=message_text)
            return redirect('book_detail', book_id=book.id)

    context = {
        'book': book,
        'messages': book.messages.all().order_by('-created_at')
    }
    return render(request, 'library/book_detail.html', context)

@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    if request.method == 'POST' and 'checkout' in request.POST:
        try:
            book = Book.objects.get(id=request.POST.get('book_id'))
            patron = User.objects.get(username=request.POST.get('patron_username'))
            if book.is_available and is_patron(patron):
                 Loan.objects.create(book=book, patron=patron, due_date=request.POST.get('due_date'))
        except (Book.DoesNotExist, User.DoesNotExist):
            pass 

    if request.method == 'POST' and 'checkin' in request.POST:
        Loan.objects.filter(id=request.POST.get('loan_id')).delete()

    context = {
        'books': Book.objects.all(),
        'loans': Loan.objects.all().order_by('due_date'),
        'patrons': User.objects.filter(groups__name='Patron'),
    }
    return render(request, 'library/librarian_dashboard.html', context)

@login_required
@user_passes_test(is_patron)
def patron_dashboard(request):
    my_loans = Loan.objects.filter(patron=request.user).order_by('due_date')
    return render(request, 'library/patron_dashboard.html', {'loans': my_loans})