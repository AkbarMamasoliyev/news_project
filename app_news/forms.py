from django import forms
from .models import Contact, News

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class EditNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body', 'image', 'category', 'status', 'author',]

    def __init__(self, *args, **kwargs):
        super(EditNewsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})