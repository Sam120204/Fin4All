import base64
import json
import os
import io
import ast
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from Fin4All.DB.main import *

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

@csrf_exempt
def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

@csrf_exempt
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

@csrf_exempt
def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

@csrf_exempt
def add_recommendation(request, username):
    if request.method == 'POST':
        data = json.loads(request.body)
        update_recommendation(username, data['suggestion'], data['type'])
        return HttpResponse("OK", status=200)
    return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def read_recommendation(request, username):
    if request.method == 'GET':
        return JsonResponse(get_recommendation(username), status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )