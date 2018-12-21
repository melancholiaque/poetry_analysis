from django.db import models


class Poet(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Poem(models.Model):

    content = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content[:20]}...'
