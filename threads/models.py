from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    type = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            {"can_moderate_threads", "Can moderate threads"},
        ]

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            {"can_moderate_comments", "Can moderate comments"},
        ]
