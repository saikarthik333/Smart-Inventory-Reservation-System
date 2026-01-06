from app.storage import store


class FairnessService:
    """
    Computes user fairness score and decides reservation TTL.
    """

    def get_fairness_score(self, user_id: str) -> float:
        stats = store.get_user_stats(user_id)

        total = stats["total_reservations"]
        success = stats["successful_checkouts"]

        if total == 0:
            return 1.0  #new users get full trust

        return success / total

    def get_ttl_seconds(self, user_id: str) -> int:
        score = self.get_fairness_score(user_id)

        if score >= 0.7:
            return 300  # 5 minutes
        elif score >= 0.4:
            return 180  # 3 minutes
        else:
            return 60   # 1 minute
