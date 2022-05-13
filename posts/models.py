from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.title} - {self.updated}'

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=(self.id, self.slug))
