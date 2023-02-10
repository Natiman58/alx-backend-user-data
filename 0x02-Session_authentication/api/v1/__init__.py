#!/usr/bin/env python3
from flask import Blueprint

app_views = Blueprint("app.views", __name__, url_prefix="api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *