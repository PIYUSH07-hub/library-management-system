from django.shortcuts import render, get_object_or_404, redirect
from .forms import IssueBookForm, ReturnBookForm
from .models import Transaction, Member,Book
from django.contrib import messages
from datetime import date
import requests

def issue_book_view(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            book = form.cleaned_data['book']

            if member.debt > 500:
                messages.error(request, "Member has outstanding debt over ₹500.")
                return redirect('issue-book')

            if book.stock < 1:
                messages.error(request, "Book out of stock.")
                return redirect('issue-book')

            # Create transaction
            Transaction.objects.create(member=member, book=book)
            book.stock -= 1
            book.save()
            messages.success(request, f"Issued '{book.title}' to {member.name}.")
            return redirect('issue-book')
    else:
        form = IssueBookForm()
    return render(request, 'library/issue_book.html', {'form': form})

def return_book_view(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            txn_id = form.cleaned_data['transaction_id']
            rent_fee = form.cleaned_data['rent_fee']

            txn = get_object_or_404(Transaction, id=txn_id)

            if txn.return_date:
                messages.error(request, "Book already returned.")
                return redirect('return-book')

            txn.return_date = date.today()
            txn.rent_fee = rent_fee
            txn.save()

            txn.member.debt += rent_fee
            txn.member.save()

            txn.book.stock += 1
            txn.book.save()

            messages.success(request, f"Book returned. ₹{rent_fee} charged to {txn.member.name}.")
            return redirect('return-book')
    else:
        form = ReturnBookForm()
    return render(request, 'library/return_book.html', {'form': form})


def search_books(request):
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__icontains=query)
    return render(request, 'library/search_books.html', {'books': books, 'query': query})




def import_books(request):
    if request.method == 'POST':
        total_books = int(request.POST.get('total_books', 20))
        title_filter = request.POST.get('title', '')

        books_imported = 0
        page = 1

        while books_imported < total_books:
            response = requests.get(
                'https://frappe.io/api/method/frappe-library',
                params={'page': page, 'title': title_filter}
            )
            data = response.json().get('message', [])

            # Debug output
            print(f"Requesting: https://frappe.io/api/method/frappe-library?page={page}&title={title_filter}")
            print(f"Books Found: {len(data)}")

            if not data:
                break

            for item in data:
                if books_imported >= total_books:
                    break

                _, created = Book.objects.get_or_create(
                    title=item['title'],
                    authors=item['authors'],
                    isbn=item['isbn'],
                    publisher=item['publisher'],
                    defaults={'stock': 1, 'pages': item.get('num_pages') or 100}
                )

                if created:
                    books_imported += 1

            page += 1

        messages.success(request, f'{books_imported} books imported successfully.')
        return redirect('import_books')

    return render(request, 'library/import_books.html')
