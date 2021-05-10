from .models import Post, Category ,Comment
from django import forms

choices = Category.objects.all().values_list('name','name')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'category': forms.Select(choices=choices,attrs={'class':'form-control'})
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
           }
