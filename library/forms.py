from django import forms
from .models import Book, Member

class IssueBookForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all())
    book = forms.ModelChoiceField(queryset=Book.objects.all())

class ReturnBookForm(forms.Form):
    transaction_id = forms.IntegerField(label="Transaction ID")
    rent_fee = forms.DecimalField(label="Rent Fee (Rs.)", decimal_places=2)
