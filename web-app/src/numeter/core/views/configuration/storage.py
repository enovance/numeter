from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from core.models import Storage, Host
from core.forms import Storage_Form
from core.utils.decorators import login_required, superuser_only
from core.utils import make_page


@login_required()
@superuser_only()
def storage_index(request):
    Storages = Storage.objects.all()
    Storages_count = Storages.count()
    Storages = make_page(Storages, 1, 20)
    return render(request, 'configuration/storages/index.html', {
        'Storages': Storages,
        'Storages_count': Storages_count,
        'Hosts_count': Host.objects.count(),
        'Bad_hosts_count': len(Storage.objects.get_bad_referenced_hostids())
    })


@login_required()
@superuser_only()
def storage_list(request):
    Storages = Storage.objects.all()
    q = request.GET.get('q','')
    if q:
        Storages = Storages.filter(name__icontains=request.GET.get('q',''))
    Storages = make_page(Storages, int(request.GET.get('page',1)), 20)
    return render(request, 'configuration/storages/storage-list.html', {
        'Storages': Storages,
        'q':q,
    })


@login_required()
@superuser_only()
def storage_get(request, storage_id):
    S = get_object_or_404(Storage.objects.filter(pk=storage_id))
    F = Storage_Form(instance=S)
    return render(request, 'configuration/storages/storage.html', {
        'Storage_Form': F,
    })


@login_required()
@superuser_only()
def storage_add(request):
    if request.method == 'POST':
        F = Storage_Form(request.POST)
        if F.is_valid():
            F.save()
            messages.success(request, _("Storage added with success."))
        else:
            for field,error in F.errors.items():
                messages.error(request, '<b>%s</b>: %s' % (field,error))
        return render(request, 'base/messages.html', {})
    else:
        return render(request, 'configuration/storages/storage.html', {
            'Storage_Form': Storage_Form(),
        })


@login_required()
@superuser_only()
def storage_update(request, storage_id):
    S = get_object_or_404(Storage.objects.filter(pk=storage_id))
    F = Storage_Form(data=request.POST, instance=S)
    if F.is_valid():
        F.save()
        messages.success(request, _("Storage updated with success."))
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))

    return render(request, 'base/messages.html', {})


@login_required()
@superuser_only()
def storage_delete(request, storage_id):
    S = get_object_or_404(Storage.objects.filter(pk=storage_id))
    S.delete()
    messages.success(request, _("Storage deleted with success."))
    return render(request, 'base/messages.html', {})


@login_required()
@superuser_only()
def storage_bad_hosts(request):
    if request.method == 'GET':
        hosts = Storage.objects.get_bad_referenced_hostids()
        return render(request, 'configuration/storages/bad-host-list.html', {
            'Hosts': Host.objects.filter(hostid__in=hosts),
        })
    else:
        Storage.objects.repair_hosts()
        messages.success(request, _("Hosts fixing finished."))
        return render(request, 'base/messages.html', {})


@login_required()
@superuser_only()
def storage_create_hosts(request, storage_id):
    Storage.objects.get(id=storage_id).create_hosts()
    messages.success(request, _("Hosts creation finished."))
    return render(request, 'base/messages.html', {})
