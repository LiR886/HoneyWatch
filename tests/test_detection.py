from app.config import Settings


def test_high_value_username_parsing():
    settings = Settings(high_value_usernames="admin, root, Support")
    assert settings.high_value_username_set == {"admin", "root", "support"}
