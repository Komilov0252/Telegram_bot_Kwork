from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from db import DB
from db.models import *
from web.provider import UsernameAndPasswordProvider

app = Starlette()  # FastAPI()

# Create admin
admin = Admin(DB._engine, title="Example: SQLAlchemy",
              base_url = '/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")]
              )

# Add view
admin.add_view(ModelView(User))
admin.add_view(ModelView(Customer))
admin.add_view(ModelView(Employee))
admin.add_view(ModelView(Job))
admin.add_view(ModelView(Post))
admin.add_view(ModelView(Subjob))
# admin.add_view(ModelView(association_post_to_job))
# admin.add_view(ModelView(association_subjob_to_employee))


# Mount admin to your app
admin.mount_to(app)