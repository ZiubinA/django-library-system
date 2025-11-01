from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Loan
from django.contrib.auth.models import User

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    # Checkout Form
    if request.method == 'POST' and 'checkout' in request.POST:
        book_id = request.POST.get('book_id')
        patron_username = request.POST.get('patron_username')
        try:
            book = Book.objects.get(id=book_id, status='available')
            patron = User.objects.get(username=patron_username)
            if patron.groups.filter(name='Patron').exists():
                Loan.objects.create(book=book, patron=patron)
                book.status = 'checked_out'
                book.save()
            else:
                print("Error: User is not in the Patron group.")

        except Book.DoesNotExist:
            print(f"Error: Book with ID {book_id} is not available.")
        except User.DoesNotExist:
            print(f"Error: Patron '{patron_username}' not found.")

    #Check-in Form
    if request.method == 'POST' and 'checkin' in request.POST:
        loan_id = request.POST.get('loan_id')

        try:
            loan = Loan.objects.get(id=loan_id)
            loan.book.status = 'available'
            loan.book.save()
            loan.delete()
        except Loan.DoesNotExist:
            print(f"Error: Loan with ID {loan_id} not found.")

    available_books = Book.objects.filter(status='available')
    active_loans = Loan.objects.all().order_by('-checkout_date') 
    context = {
        'books': available_books,
        'loans': active_loans
    }
    return render(request, 'library/librarian_dashboard.html', context)

def is_patron(user):
    return user.groups.filter(name='Patron').exists()

@login_required
@user_passes_test(is_patron)
def patron_dashboard(request):
    my_loans = Loan.objects.filter(patron=request.user).order_by('due_date')

    context = {
        'loans': my_loans
    }
    return render(request, 'library/patron_dashboard.html', context)

@login_required
def home(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.groups.filter(name='Librarian').exists():
        return redirect('librarian_dashboard')
    elif request.user.groups.filter(name='Patron').exists():
        return redirect('patron_dashboard')
    else:
        return redirect('accounts/login/')