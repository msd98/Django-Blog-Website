from django.views import generic
from .models import Post,Comment,Review
from .forms import CommentForm,Rateform
from django.shortcuts import render, get_object_or_404,redirect
from urllib.parse import quote_plus
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from django.views.generic import CreateView

def autosuggest(request):
    query=request.GET.get('term')
    allPosts = Post.objects.filter(title__icontains=query)
    mylist=[]
    mylist += [x.title for x in allPosts]
    return JsonResponse(mylist,safe=False)

def search(request):
    query=request.GET['query']
    if len(query)>60:
        allPosts = []
    else:
        allPosts = Post.objects.filter(title__icontains=query)
    params = {'allPosts':allPosts,'query':query}
    return render(request,'search.html',params)


def Likeview(request, slug):
    post=get_object_or_404(Post, slug=slug)
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('post_detail',args=[slug]))

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

class AddPostView(CreateView):
    model = Post
    template_name = 'create_post.html'
    fields = ('category','title','slug','author','content','status')

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    share_string=quote_plus(post.content)
    comments = post.comments.filter(active=True, parent__isnull=True)
    new_comment = None
    stuff=get_object_or_404(Post,slug=slug)
    total_likes=stuff.total_likes()
    liked=False
    if stuff.likes.filter(id=request.user.id).exists():
        liked=True
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,'share_string':share_string,
                                           'total_likes':total_likes,'liked':liked})

def rate(request,slug):
    template_name = 'rate.html'
    post = Post.objects.get(slug=slug)
    user=request.user

    if request.method=='POST':
        form=Rateform(request.POST)
        if form.is_valid():
            rate=form.save(commit=False)
            rate.user=user
            rate.post=post
            rate.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    else:
        form=Rateform()
    return render(request,template_name,{'form':form,'post':post})

