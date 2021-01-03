from django.db import models
# from django.db.models.functions import (
#     ExtractDay, ExtractHour, ExtractMinute, ExtractMonth,
#     ExtractQuarter, ExtractSecond, ExtractWeek, ExtractIsoWeekDay,
#     ExtractWeekDay, ExtractIsoYear, ExtractYear,
#  )
# Create your models here.

def file_directory_path(instance, filename):

    year = str(instance.created_at.year)
    month = str(instance.created_at.month)
    day = str(instance.created_at.day)

    date = year + "-" + month + "-" + day

    return 'data/{0}/{1}{2}'.format(date, instance.tim, instance.ext)


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
    mediafile = models.FileField(upload_to=file_directory_path, null=True, blank=True)
    fetched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.postid) + " " + str(self.tim) + " " + str(self.ext)

# class Board(models.Model):
#     id = models.DecimalField(max_digits=10,decimal_places=0,primary_key=True)
#     summary = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)