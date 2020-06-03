from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default='2050-12-15')
    # published_date = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.pk})

    def approved_comments(self):
        return self.comments.filter(approved=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=250,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()


    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('blog:post_list')
