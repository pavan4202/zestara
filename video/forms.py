from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(error_messages={'required': 'Can not be empty',},
        widget=forms.Textarea(attrs = {'placeholder': 'Comment here' })
    )

    class Meta:
        model = Comment
        fields = ['content']

