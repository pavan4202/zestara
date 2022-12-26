import smtplib

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mass_mail, send_mail
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import *
from django.utils.html import strip_tags
from django.views.generic import View


def get_page_list(paginator, page):

    """
    Paging logic
    if page number>=10:
        When the current page<=5, the starting page is 1
        When the current page>(total pages-5), the starting page is (total pages-9)
        In other cases, the starting page is (current page -5)
    """

    page_list = []

    if paginator.num_pages > 10:
        if page.number <= 5:
            start_page = 1
        elif page.number > paginator.num_pages - 5:
            start_page = paginator.num_pages - 9
        else:
            start_page = page.number - 5

        for i in range(start_page, start_page + 10):
            page_list.append(i)
    else:
        for i in range(1, paginator.num_pages + 1):
            page_list.append(i)

    return page_list

def ajax_required(f):
    """Not a mixin, but a nice decorator to validate than a request is AJAX"""
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def send_html_email(subject, html_message, to_list):
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, to_list, html_message=html_message)


def send_email(subject, content, to_list):

    """
    Example:
    subject = 'test subject'
    content = 'hello, this is content'
    to_list = ['abc@qq.com','abcd@163.com']
    send_email(subject, content, to_list)

    """
    try:
        message = (subject, content, settings.EMAIL_HOST_USER, to_list)
        # do not forget set password
        print("--> is sending email")
        send_mass_mail((message,))
    except smtplib.SMTPException :
        print("--> send fail")
        return HttpResponse("fail")
    else:
        print("--> send success")
        return HttpResponse("success")


class AuthorRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class AdminUserRequiredMixin(View):
    """
    管理员拦截器
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('myadmin:login')

        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(View):
    """
    超级用户拦截器
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse('无权限')

        return super().dispatch(request, *args, **kwargs)

