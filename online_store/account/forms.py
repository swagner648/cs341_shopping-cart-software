from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    states = (
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
    )
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=True)
    CustomerAddress = forms.CharField(max_length=50)
    CustomerCity = forms.CharField(max_length=50)
    CustomerState = forms.ChoiceField(choices=states)
    CustomerZIP = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'CustomerAddress', 'CustomerCity', 'CustomerState', 'CustomerZIP', 'password1', 'password2')
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')