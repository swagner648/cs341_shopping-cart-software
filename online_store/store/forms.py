from django import forms


class Search(forms.Form):
    search_text = forms.CharField(label="search_text", max_length=100)


class Add_To_Cart(forms.Form):
    ProductID = forms.IntegerField(label='ProductID')
    ProductSize = forms.CharField(label='ProductSize', max_length=5)
    Quantity = forms.IntegerField(label='Quantity')


class Update_Cart(forms.Form):
    ProductID = forms.IntegerField(label='ProductID')
    ProductSize = forms.CharField(label='ProductSize', max_length=5)
    Quantity = forms.IntegerField(label='Quantity')


class Apply_Coupon(forms.Form):
    CouponCode = forms.CharField(max_length=5)


class Checkout(forms.Form):
    FirstName = forms.CharField(max_length=50)
    LastName = forms.CharField(max_length=50)
    Email = forms.EmailField(max_length=254)
    Address = forms.CharField(max_length=50)
    City = forms.CharField(max_length=50)
    State = forms.CharField(max_length=2)
    ZIP = forms.IntegerField()


class Purchase(forms.Form):
    # TransactionProducts = forms.CharField()
    CustomerEmail = forms.CharField()
    CustomerAddress = forms.CharField()
    CustomerCity = forms.CharField(max_length=50)
    CustomerState = forms.CharField(max_length=2)
    CustomerZIP = forms.IntegerField()
