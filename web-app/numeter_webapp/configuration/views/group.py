from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from core.models import Group
from configuration.forms.group import Group_Form
from core.utils.decorators import login_required, superuser_only
from core.utils import make_page
from core.utils.http import render_HTML_JSON


@login_required()
@superuser_only()
def list(request):
    Groups = Group.objects.all()
    q = request.GET.get('q','')
    if q:
        Groups = Groups.filter(name__icontains=request.GET.get('q',''))
    Groups = make_page(Groups, int(request.GET.get('page',1)), 20)
    return render(request, 'users/group-list.html', {
        'Groups': Groups,
        'q':q,
    })


@login_required()
@superuser_only()
def add(request):
    if request.method == 'POST':
        F = Group_Form(request.POST)
        data = {}
        if F.is_valid():
            G = F.save()
            messages.success(request, _("Group added with success."))
            data['response'] = 'ok'
            data['callback-url'] = G.get_absolute_url()
        else:
            for field,error in F.errors.items():
                messages.error(request, '<b>%s</b>: %s' % (field,error))
            data['response'] = 'error'
        return render_HTML_JSON(request, data, 'base/messages.html', {})
    else:
        return render(request, 'users/group.html', {
            'Group_Form': Group_Form(),
        })


@login_required()
@superuser_only()
def get(request, group_id):
    G = get_object_or_404(Group.objects.filter(pk=group_id))
    F = Group_Form(instance=G)
    return render(request, 'users/group.html', {
        'Group_Form': F,
    })


@login_required()
@superuser_only()
def update(request, group_id):
    G = get_object_or_404(Group.objects.filter(pk=group_id))
    F = Group_Form(data=request.POST, instance=G)
    data = {}
    if F.is_valid():
        F.save()
        messages.success(request, _("Group updated with success."))
        data['response'] = 'ok'
        data['callback-url'] = G.get_absolute_url()
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))
        data['response'] = 'error'
    return render_HTML_JSON(request, data, 'base/messages.html', {})


@login_required()
@superuser_only()
def delete(request, group_id):
    G = get_object_or_404(Group.objects.filter(pk=group_id))
    G.delete()
    messages.success(request, _("Group deleted with success."))
    return render(request, 'base/messages.html', {})


# TODO : Make unittest
@login_required()
@superuser_only()
def bulk_delete(request):
    """Delete several groups in one request."""
    groups = Group.objects.filter(pk__in=request.POST.getlist('ids[]'))
    groups.delete()
    messages.success(request, _("Group(s) deleted with success."))
    return render_HTML_JSON(request, {}, 'base/messages.html', {})
