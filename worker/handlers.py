"""Event Handlers — mirrors n8n nodes. Each function handles one event type."""

def handle_tap(user_id: str, payload: dict):
    coins = payload.get("coins", 1)
    print(f"  🐹 [TAP] User {user_id} tapped! +{coins} coins")
    return {"action": "score_updated", "coins_added": coins}

def handle_upgrade(user_id: str, payload: dict):
    item = payload.get("item", "unknown")
    cost = payload.get("cost", 0)
    print(f"  ⚡ [UPGRADE] User {user_id} bought: {item} for {cost} coins")
    return {"action": "upgrade_applied", "item": item}

def handle_login(user_id: str, payload: dict):
    print(f"  🔑 [LOGIN] User {user_id} logged in")
    return {"action": "session_started"}

def handle_score_update(user_id: str, payload: dict):
    score = payload.get("score", 0)
    print(f"  🏆 [SCORE] User {user_id} new score: {score}")
    return {"action": "leaderboard_updated", "score": score}

def handle_unknown(user_id: str, payload: dict):
    print(f"  ❓ [UNKNOWN] Unhandled event for user {user_id}: {payload}")
    return {"action": "skipped"}
