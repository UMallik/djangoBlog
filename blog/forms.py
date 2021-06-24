from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.template.defaultfilters import slugify

# class AuthorForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     active = forms.BooleanField(required=False)
#     # custom validators
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         nae_l = name.lower()
#         if name_l == 'admin' or name_l == 'author':
#             raise ValidationError('Name cannot be admin or author')
#         return name_l
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         return email.lower()

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'email', 'active']
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         nae_l = name.lower()
#         if name_l == 'admin' or name_l == 'author':
#             raise ValidationError('Name cannot be admin or author')
#         return name_l
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         return email.lower()

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        if name == 'tag' or name == 'add' or name == 'update':
            raise ValidationError('Tag cannot be {}'.format(name))
        return self.cleaned_data['name']

    def clean(self):

        cleaned_data = super(TagForm,self).clean()
        name = cleaned_data.get('name')

        if name:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        if name == 'tag' or name == 'add' or name == 'update':
            raise ValidationError('Tag cannot be {}'.format(name))
        return self.cleaned_data['name']

    def clean(self):

        
        cleaned_data = super(CategoryForm,self).clean()
        name = cleaned_data.get('name')

        if name:
            cleaned_data['slug'] = slugify(name)
        return cleaned_data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
    
    
  
    def clean_name(self):
        name = self.cleaned_data['title'].lower()
        if name == 'tag' or name == 'add' or name == 'update':
            raise ValidationError('Tag cannot be {}'.format(name))
        return self.cleaned_data['name']

    def clean(self):
        cleaned_data = super(PostForm,self).clean()
        title = cleaned_data.get('title')

        if title:
            cleaned_data['slug'] = slugify(title)
        return cleaned_data

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'