from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse

from .forms import CommentForm
from .models import Comment
# Create your views here.
@login_required
def comment_delete(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        response = HttpResponse('Forbidden Action')
        response.status_code = 403
        return response

    parent_obj_url = obj.content_object.get_absolute_url()

    if request.method == "POST" or "GET":
        obj.delete()
        messages.success(request, 'This comment has been deleted.')
        return HttpResponseRedirect(parent_obj_url)

    context = {
        "object": obj,
        "parent_obj_url": parent_obj_url
    }
    return HttpResponseRedirect(parent_obj_url)

def comment_thread(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent

    content_object = obj.content_object
    content_id = obj.content_object.id

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None

        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj
        )
        print(f"{new_comment}")
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        "comment": obj,
        "form": form
    }
    return render(request, "comment_thread.html", context)
