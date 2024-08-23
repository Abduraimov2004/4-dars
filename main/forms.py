from .models import *
from django import forms


class CourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Course
        fields = ['title', "created_at", 'description', 'duration',  'price', 'category', 'tags', 'language', 'image']



class UpdateCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'price', 'category', 'tags', 'language', 'image']
