import bcrypt

from repositories import user_repository


def get_all_users(limit: int, offset: int) -> list[dict]:
    return user_repository.get_all_users(limit, offset)


def get_user_by_id(user_id: int) -> dict:
    return user_repository.get_user_by_id(user_id)


def update_user(user_id: int, dto: dict) -> dict:
    update_fields = dict(dto)

    if update_fields.get("password"):
        update_fields["password_hash"] = bcrypt.hashpw(
            update_fields["password"].encode(), bcrypt.gensalt()
        ).decode()
        del update_fields["password"]

    return user_repository.update_user(user_id, update_fields)


def delete_user(user_id: int) -> None:
    return user_repository.delete_user(user_id)
