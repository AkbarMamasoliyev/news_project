from django import forms
from .models import Contact, News, Comment

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': ""
        }

        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 1,
                'col': 4
            })
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})