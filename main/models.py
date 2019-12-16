from django.db import models
from datetime import datetime

# Create your models here.

# class Tag(models.Model):
#     pass

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_published = models.DateTimeField('date published', default=datetime.now)
    # tags = models.ManyToManyField(
    #     Tag,
    #     through='PostTag',
    #     through_fields=('tag', 'post'),
    # )

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.post_title

class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    # posts = models.ManyToManyField(
    #     Post,
    #     through='PostTag',
    #     through_fields=('tag', 'post'),
    # )

    posts = models.ManyToManyField(Post)

    def __str__(self):
        return '#'+self.tag_name

# class PostTag(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.tag.tag_name+':'+self.post.post_title
