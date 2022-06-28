from django.contrib import admin

from account.models import Post,Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Post, PostAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Vote, VoteAdmin)