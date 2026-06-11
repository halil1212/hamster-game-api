"""Dispatcher — routes each event_type to the correct handler. Like n8n Switch node."""
from worker.handlers import handle_tap, handle_upgrade, handle_login, handle_score_update, handle_unknown

HANDLER_REGISTRY = {
    "tap": handle_tap,
    "upgrade": handle_upgrade,
    "login": handle_login,
    "score_update": handle_score_update,
}

def dispatch(event_type: str, user_id: str, payload: dict) -> dict:
    handler = HANDLER_REGISTRY.get(event_type, handle_unknown)
    return handler(user_id, payload)
