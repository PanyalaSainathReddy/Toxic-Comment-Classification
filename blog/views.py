from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .forms import CommentForm
from .models import Post, Category
from .predict import SVC_Model
# from prml_helper.processor import Preprocessor

svc_model = SVC_Model()


def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment_text = comment.body
            print(svc_model.predict(comment_text)[0])
            print(comment_text)
            comment.save()
            form = CommentForm()

            return render(request, 'blog/detail.html', {'post': post, 'form': form})
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts': posts, 'query': query})
