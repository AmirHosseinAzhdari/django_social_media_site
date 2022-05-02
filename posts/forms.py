from django import forms

from posts.models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
