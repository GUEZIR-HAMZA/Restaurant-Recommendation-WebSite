from django import forms
from Restaurant_Recommendation_WebSite.models import Users


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Users
        fields = ['username', 'password']


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Users
        fields = ['rating', 'comment']


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', required=False)

    class Meta:
        model = Users
        fields = ['search']


class FilterForm(forms.Form):
    filter = forms.CharField(max_length=50)

    class Meta:
        model = Users
        fields = ['filter']


class SortForm(forms.Form):
    sort_choices = [
        ('name', 'Name'),
        ('rating', 'Rating: Low to High'),
        ('-rating', 'Rating: High to Low'),
        ('price', 'Price: Low to High'),
        ('-price', 'Price: High to Low'),
    ]
    sort_by = forms.ChoiceField(choices=sort_choices, required=False, label='Sort By', initial='-rating')

    class Meta:
        model = Users
        fields = ['sort_by']


class FavoriteForm(forms.Form):
    favorite = forms.BooleanField(required=False)

    class Meta:
        model = Users
        fields = ['favorite']
