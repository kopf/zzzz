from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from api.models import Subdomain


def index(request):
    return render(request, 'index.html')


def faq(request):
    return render(request, 'faq.html')


@login_required
def account(request):
    """Show account page"""
    subdomains = Subdomain.objects.filter(user=request.user)
    context = {'subdomains': subdomains,
               'allowed_subdomains': settings.USER_CLASSES[request.user.user_class]['domain_limit']}
    return render(request, 'account.html', context)


@login_required
def modify_account(request):
    """Edit / delete account page"""
    subdomains = Subdomain.objects.filter(user=request.user)
    context = {'subdomains': subdomains}
    return render(request, 'account_modify.html', context)


@login_required
def export_account_json(request):
    """Export an account as JSON"""
    subdomains = []
    for subdomain in Subdomain.objects.filter(user=request.user):
        subdomains.append({'name': subdomain.name, 'ip': subdomain.ip,
                           'ipv6': subdomain.ipv6, 'updated': subdomain.updated})
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'token': request.user.token,
        'subdomains': subdomains,
        'user_class': request.user.user_class,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login
    })


@login_required
def delete_account(request):
    if request.POST.get('username_verification') != request.user.username:
        messages.add_message(request, messages.ERROR, "Username verification failed.")
        return redirect('frontend.views.modify_account')
    request.user.delete()
    messages.add_message(request, messages.INFO, "Your account was successfully deleted.")
    return redirect('frontend.views.index')

def donate(request):
    return render(request, 'donate.html')


def startssl_validation_code(request):
    from django.http import HttpResponse
    return HttpResponse('TXpoemJEY1FJM0p2NlZYa0Q4OExGbkhPZ0tteVZJdm0wZzg0UjF0UC95az0')
