from django import forms

from .models import Review, UserMovieStatus

class ReviewForm(forms.ModelForm):
    class Meta:
        model   = Review
        fields  = ['rating', 'comment']
        widgets = {
            'rating'  : forms.NumberInput(attrs={
                'min' : 1, 'max' : 5, 'class' : 'form-control'
            }),
            'comment'  : forms.Textarea(attrs={
                'rows' : 4, 'class' : 'form-control'
            }),
        }

class WatchStatusForm(forms.ModelForm):
    class Meta:
        model   = UserMovieStatus
        fields  = ['status']
        widgets = {'status' : forms.Select(attrs={
            'class' : 'form-select'
        })}