# images/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ImageCreationForm


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
