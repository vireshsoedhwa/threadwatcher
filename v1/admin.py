from django.contrib import admin

# Register your models here.

from .models import MediaItem
from .models import Thread
from .models import Post

admin.site.register(MediaItem)
admin.site.register(Thread)
admin.site.register(Post)