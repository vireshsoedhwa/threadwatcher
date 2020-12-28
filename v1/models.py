from django.db import models

# Create your models here.

def file_directory_path(instance, filename):
    return 'input/{0}/{1}'.format(instance.id, "doc")


class MediaItem(models.Model):
    name = models.CharField(max_length=100)
    inputfile = models.FileField(upload_to=file_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    threadid = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
    summary = models.CharField(max_length=1000)
    active = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.threadid) + " " + str(self.active)

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    postid = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
    ext = models.CharField(max_length=10, null=True, blank=True)
    tim = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return str(self.postid) + " " + str(self.tim) + " " + str(self.ext)

# class Board(models.Model):
#     id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
#     summary = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)