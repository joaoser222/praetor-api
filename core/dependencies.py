from typing import List
from functools import wraps
from fastapi import Depends
from sqlalchemy.orm import selectinload
from apps.auth.dependencies import get_current_user
from apps.auth.models import User
from core.exceptions import ForbiddenException


def require_role(required_roles: List[str]):
    """
    Factory to create a dependency that checks if the current user
    has at least one of the required roles.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = {role.name for role in current_user.roles}
        if not any(role in user_roles for role in required_roles) and not current_user.is_superuser:
            raise ForbiddenException(detail=f"Requires one of the following roles: {', '.join(required_roles)}")
        return current_user

    return role_checker


def require_permission(required_permission: str):
    """
    Factory to create a dependency that checks if the current user
    has a specific permission through their roles.
    """
    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.is_superuser:
            return current_user

        user_permissions = set()
        for role in await current_user.awaitable_attrs.roles:
            for permission in await role.awaitable_attrs.permissions:
                user_permissions.add(permission.name)

        if required_permission not in user_permissions:
            raise ForbiddenException(detail=f"Action requires permission: '{required_permission}'")
        return current_user
    return permission_checker
