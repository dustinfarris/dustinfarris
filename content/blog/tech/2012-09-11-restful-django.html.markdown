Title: "RESTful Django"
Tags: Django REST

I've been taking a lot of time lately to determine a best practice way of incorporating a RESTful approach to Django views.  My goal is to come up with a solution so simple, using a third party library won't be necessary.

As a first step, I've borrowed a lot of ideas from Rails, which makes a RESTful framework practically [seamless][1].

The four HTTP methods that we most need support for are GET, POST, PUT, and DELETE.  This doesn't fully cover all potential "views" though, thus some methods become ambiguous.  For instance, GET may be used to return an object, or a list of objects.

An important question is how compact do we want our URL structure to be?  If we have a separate distinguishable URL for every action (not method), then the code is straight forward, but the URL structure perhaps becomes sloppy.  If we consolidate the actions into a few URL patterns, then the URL structure is cleaner, but the coding becomes complicated.  There is a tradeoff either way.

I've chosen to try the latter approach, using methods to give URLs multiple actions.

The primary actions I need for any basic model are:

* Create
* Show
* Show list
* Update
* Delete

And these can all be accomplished with our 4 methods and just two URLs:

* /objects/
* /object/id/

But we also want to return data in an appropriate manner for API calls, so we add JSON extensions and our URL list becomes:

* /objects/
* /objects.json
* /objects/id/
* /objects/id.json

So in ``urls.py`` we add these two patterns.  Assuming we've namespaced our application, this will look something like:

    :::python
    urlpatterns = ('',
        url(r'^s/$', ... ),
        url(r'^s\.json$', ..., {'as_json': True}),
        url(r'^/(?P<id>\d+)/$', ... ),
        url(r'^/(?P<id>\d+)\.json$', ..., {'as_json': True}),
    )

## A 4-way stop

So the difficult part becomes the views.  I decided to put a "management" view called ``do`` in front of the real workers to determine what the intended action is.  It polls the method used and any POST data that might point it in the right direction.  Hiding a ``_method`` input element in HTML pages works nicely for this when you want to call a method besides GET or POST (thanks Rails).

    :::python
    @csrf_exempt
    def do(request, **kwargs):
        if request.method == 'POST':
            method = request.POST.get('_method', 'POST')
        else:
            method = request.method
        return {
            'get': _show,
            'post': _create,
            'put': _update,
            'delete': _destroy,
        }[method.lower()](request, **kwargs)

Now that our request is pointed in the right direction, we have to handle it appropriately.

## Show

The show action is arguably the easiest to handle, we just have to determine if we are showing one object, or a list of objects.

    :::python
    def _show_list(request, as_json=False):
        queryset = MyObject.objects.all()
        if as_json:
            objs = []
            for obj in queryset.all():
                objs.append({
                  k:str(v) for k,v in obj.__dict__.items() if k is not '_state'})
            content = json.dumps(objs)
            return HttpResponse(content, content_type='application/json')
        return render(request, 'objects/object_list.html', {'object_list': queryset})

    def _show(request, id=None, as_json=False):
        if not id:
            return _show_list(request, as_json)
        obj = get_object_or_404(MyObject, id=id)
        if as_json:
            content = json.dumps({
                k:str(v) for k,v in obj.__dict__.items() if k is not '_state'})
            return HttpResponse(content, content_type='application/json')
        return render(request, 'objects/object_detail.html', {'object': obj})

## Create

Here is a stumbling point for me.  Everything "just works" here, but not explicitly.  The "form processing" functionality Django comes out of the box with just so happens to process any such data as long is it is appropriately keyed.  I would prefer a more robust method, but for now:

    :::python
    def new(request, form=None):
        form = form or NewObjectForm()
        return render(request, 'objects/new.html', {'form': form})

    def _create(request):
        form = NewObjectForm(request.POST)
        if form.is_valid():
            new_obj = form.save()
            messages.success(request, "New object created!")
            return redirect(new_obj)
        return new(request, form)

Note that we create a ``new`` view to display the standard HTML form for browser users.

## Update

The reason I'm not completely satisfied with the way I handle the create action becomes visible here in the update action.  The same mentality applies, except we can no longer rely on Django's form data parsing--a PUT request doesn't come with request.POST; so, we have to rely on the raw data.

    :::python
    def edit(request, id, form=None):
        obj = get_object_or_404(MyObject, id=id)
        form = form or EditObjectForm(instance=obj)
        return render(request, 'objects/edit.html', {'form': form})

    def _update(request, id):
        obj = get_object_or_404(MyObject, id=id)
        if request.method == 'PUT':
            raw_put_data = urlparse.parse_qs(request.raw_post_data)
            data = {k:v[0] for k,v in raw_put_data.items()}
            obj.attr1 = data.get('attr1', obj.attr1)
            obj.attr2 = data.get('attr2', obj.attr2)
            ...
            obj.save()
            return HttpResponse("Success")
        else:
            form = EditObjectForm(request.POST, instance=obj)
            if form.is_valid():
                updated_object = form.save()
                messages.success(request, "Object edit successful.")
                return redirect(updated_object)
            return edit(request, id, form)

## Delete

Last, but not least is the delete/destroy action.  I suppose this is the easiest to implement.

    :::python
    def _destroy(request, id):
        obj = get_object_or_404(MyObject, id=id)
        obj.delete()
        messages.success(request, "Object destroyed!")
        return redirect(_show_list)

So there's one way to get RESTfulish environment into Django.  It is far from perfect, and I haven't bothered trying to explain how to do user authentication and whatnot here since I'm still trying to wrap my head around it.  But at any rate, you should be able to runserver, and run basic HTTP methods against your data.

[1]: http://guides.rubyonrails.org/routing.html
