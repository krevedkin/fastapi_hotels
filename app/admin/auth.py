from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.dependencies import get_current_user
from app.auth.exceptions import InvalidCredentialsHTTPException
from app.auth.models import Users
from app.auth.utils import authenticate_user, create_access_token


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        form_data = await request.form()
        user = await authenticate_user(
            str(form_data["username"]),
            str(form_data["password"]),
        )

        if not user or not user.role == "admin":  # type: ignore
            raise InvalidCredentialsHTTPException

        if isinstance(user, Users):
            access_token = create_access_token(
                data={
                    "sub": user.email,
                    "user_id": user.id,
                }
            )
            request.session.update({"access_token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("access_token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)

        if not isinstance(user, Users):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if not user.role == "admin":
            request.session.clear()
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key="...")
