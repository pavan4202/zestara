from django.shortcuts import render
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template.loader import render_to_string
#from ratelimit.decorators import ratelimit

from video.forms import CommentForm
from video.models import Video

# Create your views here.

def submit_comment(request,pk):

    video = get_object_or_404(Video, pk = pk)
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # print('success')
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.nickname = request.user.nickname
        new_comment.avatar = request.user.avatar
        new_comment.video = video
        new_comment.save()

        data = dict()
        data['nickname'] = request.user.nickname
        data['avatar'] = request.user.avatar
        data['timestamp'] = datetime.fromtimestamp(datetime.now().timestamp())
        data['content'] = new_comment.content

        comments = list()
        comments.append(data)

        html = render_to_string(
            "comment/comment_single.html", {"comments": comments})

        # remove the "html": html" to remove json code in the new page of the redirect
        #return JsonResponse({"code":0,"html": html})
    #return JsonResponse({"code":1,'msg':'Comment failed!'})
    return render(request, 'video/detail.html')


def get_comments(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    page = request.GET.get('page')
    page_size = request.GET.get('page_size')
    video_id = request.GET.get('video_id')
    video = get_object_or_404(Video, pk=video_id)
    comments = video.comment_set.order_by('-timestamp').all()
    comment_count = len(comments)

    paginator = Paginator(comments, page_size)
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = []

    if len(rows) > 0:
        code = 0
        html = render_to_string(
            "comment/comment_single.html", {"comments": rows})
    else:
        code = 1
        html = ""

    return JsonResponse({
        "code":code,
        "html": html,
        "comment_count": comment_count
    })
