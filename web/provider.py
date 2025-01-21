import bcrypt
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider, AdminConfig, AdminUser
from starlette_admin.exceptions import FormValidationError, LoginFailed

from utils.Conf import CF


class UsernameAndPasswordProvider(AuthProvider):
    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response) -> Response:
        if len(username) < 3:
            """fFORM DATA VALIDATION"""
            raise FormValidationError(
                {'username' : 'Ensure username at least 3 characters'}
            )

        if username == CF.web.ADMIN_USERNAME and bcrypt.checkpw(password.encode(), CF.web.ADMIN_PASSWORD.encode()):
            """SAVE 'USERNAME' IN SESSION"""
            request.session.update({'username': username})
            return response
        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get('username') == CF.web.ADMIN_USERNAME:
            username = request.session['username']
            request.state.user = username
            return True
        return False
    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(
            app_title="Factor Bot Admin"
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        print(user, "====================================================")
        return AdminUser(username=user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
