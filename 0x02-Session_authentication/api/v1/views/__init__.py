#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

#!/usr/bin/env python3
"""
Initialization of views for the API
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views
from api.v1.views.index import *  # noqa
from api.v1.views.users import *  # noqa
from api.v1.views.session_auth import *  # noqa

