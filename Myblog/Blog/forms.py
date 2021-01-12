from .models import Comment,RATE_CHOICES,Review
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class Rateform(forms.ModelForm):
    text=forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}),required=False)
    rate=forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(),required=True)

    class Meta:
        model = Review
        fields = ('text','rate')