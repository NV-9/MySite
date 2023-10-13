from django.shortcuts import render
from django.http import HttpRequest
from .models import Post


def post_view(request, slug: str = None):
    if slug is not None:
        try:
            post: Post = Post.objects.get(slug = slug)
            if post.published == True:
                context = {'post': post}
                return render(request, "myblog/post.html", context = context)
        except:
            pass 
    context = {'posts': Post.objects.filter(published = True)}
    return render(request, "myblog/listing.html", context = context)
    
    
