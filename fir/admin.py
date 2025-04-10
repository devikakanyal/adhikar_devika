from django.contrib import admin
from .models import FIR, Post, Comment , Lawyer  # replace with your actual model names

admin.site.register(FIR)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Lawyer)