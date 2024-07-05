import datetime
from django import forms
from django.forms.widgets import DateInput
from django.utils.safestring import mark_safe

from blog.models import Post
from store.models import Artwork, Category, Medium

class DatePickerWidget(DateInput):
    def __init__(self, attrs=None, format='%Y-%m-%d'):
        self.format = format
        super().__init__(attrs={'class': 'datepicker form-control', 'data-provide': 'datepicker'}, format=format)

    def render(self, name, value, attrs=None, renderer=None):
        render_value = value.strftime(self.format) if isinstance(value, datetime.date) else ''
        final_attrs = self.build_attrs(attrs, {'name': name})
        return mark_safe(f'<input type="text" value="{render_value}"{" ".join([f"{k}={v}" for k, v in final_attrs.items()])} />')
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'event_date', 'event_place', 'thumbnail']
        labels = {
            'title': 'Nom évènement',
            'description': 'Description',
            'content': 'Plus de détail',
            'event_date': 'Date évènement',
            'event_place': 'Lieu évènement',
            'thumbnail': 'Miniature',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'event_date': DatePickerWidget(attrs={'class': 'form-control datepicker'}),
            'event_place': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'price', 'stock', 'width', 'height', 'thumbnail', 'category', 'medium']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'price': 'Prix',
            'stock': 'Stock',
            'width': 'Largeur',
            'height': 'Hauteur',
            'thumbnail': "Image de l'œuvre",
            'category': 'Catégorie',
            'medium': 'Medium',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'medium': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': "Nom de la Category",
            'description': "Description",
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MediumForm(forms.ModelForm):
    class Meta:
        model = Medium
        fields = ['name']
        labels = {
            'name': "Nom du support",
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
