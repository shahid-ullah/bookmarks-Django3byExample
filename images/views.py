# images/views.py
from common.decorators import ajax_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ImageCreationForm
from .models import Image


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            # breakpoint()
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            # breakpoint()
            new_item.save()
            messages.success(request, "Image added successfully")

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreationForm(data=request.GET)
        # form = ImageCreationForm()

    return render(request,
            "images/image/create.html",
            {"section": "images",
                "form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
            'images/image/detail.html',
            {'section': 'images',
                'image': image})

@ajax_required
@login_required
@require_POST
def image_like(request):
    # breakpoint()
    """TODO: Docstring for image_like.
    :returns: TODO

    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "error"})


# @login_required
# def image_list(request):
#     images = Image.objects.all()
#     paginator = Paginator(images, 2)
#     page = request.GET.get('page')
#     try:
#         images = paginator.page(page)
#     except PageNotAnInteger:
#         # if page is not an integer deliver the first page
#         images = paginator.page(1)
#     except EmptyPage:
#         if request.is_ajax():
#             # if request is AJAX and the page is out of range
#             # return an empty page
#             return HttpResponse('')
#         # if page is out of range deliver the last page
#         images = paginator.page(paginator.num_pages)

#     if request.is_ajax():
#         return render(request, 'images/image/list_ajax.html',
#                 {'section': 'images', 'images': images})

#     return render(request, 'images/image/list.html',
#             {'section': 'images', 'images': images})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 2)
    page = request.GET.get('page')
    # breakpoint()
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # breakpoint()
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        # breakpoint()
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})
