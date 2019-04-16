from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

from .dns import create_subdomain, update_if_necessary
from .models import User, Subdomain


def update(request, subdomain=None):
    """Checks whether a user is entitled to update a subdomain's IP and
    acts accordingly"""
    if not subdomain:
        msg = 'Missing subdomain'
        return HttpResponse(msg, status=400)
    subdomain = subdomain.lower()

    try:
        token = request.GET['token']
    except KeyError:
        msg = 'Bad request - token must be present in URL as GET parameter'
        return HttpResponse(msg, status=400)

    try:
        user_obj = User.objects.filter(token=token, is_active=True)[0]
        subdomain_obj = Subdomain.objects.filter(
            user=user_obj, name=subdomain)[0]
    except IndexError:
        return HttpResponse('Unauthorized', status=401)

    record_type = request.GET.get('type', 'A').upper()
    if record_type not in settings.RECORD_TYPES:
        msg = 'Bad request - illegal record type'
        return HttpResponse(msg, status=400)
    ip = request.GET.get('ip', request.META[settings.REMOTE_ADDR_KEY])

    result = update_if_necessary(
        subdomain_obj, ip, record_type, force=request.GET.get('force', False))
    return HttpResponse(result['msg'], status=result['status'])


@login_required
def create(request):
    subdomain = request.POST['subdomain'].lower()
    address = request.META[settings.REMOTE_ADDR_KEY] if request.POST.get('set_ipv4', False) else None
    try:
        create_subdomain(request.user, subdomain, address)
    except ValueError as e:
        messages.add_message(request, messages.ERROR, str(e))
    else:
        msg = 'Subdomain "{0}" created successfully!'
        messages.add_message(request, messages.SUCCESS, msg.format(subdomain))
    return redirect('frontend.views.account')


@login_required
def delete(request, subdomain=None):
    invalid = False
    try:
        subdomain_obj = Subdomain.objects.get(name=subdomain)
    except Subdomain.DoesNotExist as e:
        invalid = True
    if invalid or subdomain_obj.user != request.user:
        msg = 'Could not delete subdomain.'
        messages.add_message(request, messages.ERROR, msg)
    else:
        subdomain_obj.delete() # Deleted automatically on AWS by models.subdomain_delete
        msg = 'Subdomain {0} deleted.'.format(subdomain)
        messages.add_message(request, messages.SUCCESS, msg)
    return redirect('frontend.views.account')


@login_required
def reset_token(request):
    request.user.token = uuid4()
    request.user.save()
    return redirect('frontend.views.account')
