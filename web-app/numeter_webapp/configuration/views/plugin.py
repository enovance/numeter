from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from configuration.forms.plugin import Plugin_Form
from core.models import Host, Plugin, Data_Source
from core.models import User, Group
from core.utils.decorators import login_required, superuser_only
from core.utils import make_page
from core.utils.http import render_HTML_JSON


@login_required()
@superuser_only()
def index(request):
    """Get plugins and sources menu."""
    Plugins = Plugin.objects.all()
    Plugins_count = Plugins.count()
    Plugins = make_page(Plugins, 1, 20)
    return render(request, 'plugins/index.html', {
        'Plugins': Plugins,
        'Plugins_count': Plugins_count,
        'Sources_count': Data_Source.objects.count(),
        'Hosts': Host.objects.all(),
    })


@login_required()
@superuser_only()
def list(request):
    """List plugins and filter by request."""
    q = request.GET.get('q','')
    Plugins = Plugin.objects.web_filter(q)
    Plugins = make_page(Plugins, int(request.GET.get('page',1)), 20)
    return render(request, 'plugins/plugin-list.html', {
        'Plugins': Plugins,
        'Hosts': Host.objects.all(),
        'q':q,
    })


@login_required()
@superuser_only()
def create_from_host(request):
    """
    GET: Return plugin creation's modal.
    POST: Create submitted plguins.
    """
    if request.method == 'POST':
        host = Host.objects.get(id=request.POST['host_id'])
        plugins = host.create_plugins(request.POST.getlist('plugins[]'))
        messages.success(request, _("Plugin(s) created with success."))
        return render(request, 'base/messages.html', {})
    else:
        host = Host.objects.get(id=request.GET['host_id'])
        plugins = host.get_unsaved_plugins()
        return render(request, 'modals/create-plugins.html', {
            'plugins':plugins,
            'host':host,
        })



@login_required()
@superuser_only()
def get(request, plugin_id):
    """Get a plugin."""
    P = get_object_or_404(Plugin.objects.filter(pk=plugin_id))
    F = Plugin_Form(instance=P)
    return render(request, 'plugins/plugin.html', {
        'Plugin_Form': F,
    })


@login_required()
@superuser_only()
def update(request, plugin_id):
    """Update a plugin."""
    P = get_object_or_404(Plugin.objects.filter(pk=plugin_id))
    F = Plugin_Form(data=request.POST, instance=P)
    data = {}
    if F.is_valid():
        F.save()
        messages.success(request, _("Plugin updated with success."))
        data['response'] = 'ok'
        data['callback-url'] = P.get_absolute_url()
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))
        data['response'] = 'error'
    return render_HTML_JSON(request, data, 'base/messages.html', {})


@login_required()
@superuser_only()
def delete(request, plugin_id):
    """Delete a plugin."""
    P = get_object_or_404(Plugin.objects.filter(pk=plugin_id))
    P.delete()
    messages.success(request, _("Plugin deleted with success."))
    return render(request, 'base/messages.html', {})

# TODO
# @login_required()
# @superuser_only()
# def list_sources(request, plugin_id):
#     sources = Plugin.objects.get(id=plugin_id).get_data_sources()
#     messages.success(request, _("Sources creation finished."))
#     return render(request, 'base/messages.html', {})

@login_required()
@superuser_only()
def create_sources(request, plugin_id):
    """
    GET: Return source creation's modal.
    POST: Create submitted plguins.
    """
    P = get_object_or_404(Plugin.objects.filter(pk=plugin_id))
    if request.method == 'POST':
        P.create_data_sources(request.POST.getlist('sources[]'))
        messages.success(request, _("Sources creation finished."))
        return render(request, 'base/messages.html', {})
    else:
        return render(request, 'modals/create-sources.html', {
            'plugin': P,
            'sources': P.get_unsaved_sources()
        })


# TODO : Make unittest
@login_required()
@superuser_only()
def bulk_delete(request):
    """Delete several plugins in one request."""
    plugins = Plugin.objects.filter(pk__in=request.POST.getlist('ids[]'))
    plugins.delete()
    messages.success(request, _("Plugin(s) deleted with success."))
    return render_HTML_JSON(request, {}, 'base/messages.html', {})
