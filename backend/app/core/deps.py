from fastapi import Header


DUMMY_USER_ID = "demo_user_1"


def get_user_id(x_user_id: str | None = Header(default=None)) -> str:
    return x_user_id or DUMMY_USER_ID
