# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User

def login_view(request):
    # 檢查是否存在用戶
    if not User.objects.exists():
        return redirect('register')

    form = LoginForm(request.POST or None)
    msg = None
    LOGIN_FAILED = False

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = '表單無效'
                LOGIN_FAILED = True
        else:
            msg = '發生錯誤'


    return render(request, "accounts/login.html", {"form": form, "msg": msg, "LOGIN_FAILED": LOGIN_FAILED})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = '註冊成功'
            success = True

            # return redirect("/login/")

        else:
            msg = '註冊失敗'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
