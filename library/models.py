from django.db import models
# from django.core.exceptions import ValidationError


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    num_pages = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    pages = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.authors}"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    debt = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

# class Transaction(models.Model):
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     return_date = models.DateField(null=True, blank=True)
#     rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"{self.member.name} - {self.book.title}"




class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # ✅ Temporary fix: allow null for existing rows
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    # ✅ Add null=True to avoid default prompt
    issue_date = models.DateField(auto_now_add=True, null=True)

    return_date = models.DateField(null=True, blank=True)

    # ✅ Set a default rent fee so no prompt needed
    rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.book.title} issued to {self.member}"



# class Transaction(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
#     issue_date = models.DateField(auto_now_add=True, null=True)
#     return_date = models.DateField(null=True, blank=True)
#     rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#     def clean(self):
#         if self.member:
#             # Calculate total outstanding rent
#             total_rent = Transaction.objects.filter(
#                 member=self.member,
#                 return_date__isnull=True  # not returned yet
#             ).exclude(pk=self.pk).aggregate(models.Sum('rent_fee'))['rent_fee__sum'] or 0

#             total_rent += self.rent_fee

#             if total_rent > 500:
#                 raise ValidationError("This member has exceeded the ₹500 rent limit.")

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Calls clean() before saving
#         super().save(*args, **kwargs)