from django import forms
from .models import WildAnimalCategory

class WildAnimalCategoryForm(forms.ModelForm):
    """Form for creating and updating Wild Animal Categories."""

    class Meta:
        model = WildAnimalCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-green-500',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-green-500',
                'placeholder': 'Enter description (optional)',
                'rows': 4
            }),
        }

    def clean_name(self):
        """Allow same name when editing the same instance."""
        name = self.cleaned_data['name'].strip()
        qs = WildAnimalCategory.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name



from django import forms
from .models import WildAnimal

class WildAnimalForm(forms.ModelForm):
    """Form for adding a new wild animal."""
    class Meta:
        model = WildAnimal
        fields = [
            'category',
            'name',
            'scientific_name',
            'habitat',
            'diet',
            'size',
            'weight',
            'lifespan',
            'conservation_status',
            'conservation_source',
            'about',
            'image',
        ]
        widgets = {
        'category': forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'name': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500',
            'placeholder': 'Enter animal name'
        }),
        'scientific_name': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500',
            'placeholder': 'Enter scientific name'
        }),
        'habitat': forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500',
            'rows': 2
        }),
        'diet': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'size': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'weight': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'lifespan': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'conservation_status': forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'conservation_source': forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
        'about': forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500',
            'rows': 3
        }),
        'image': forms.FileInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500'
        }),
    }



