from django.db import models

# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question
    
class Answer(models.Model):
    answer = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, related_name='answers', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

class Vote(models.Model):
    session_key = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
