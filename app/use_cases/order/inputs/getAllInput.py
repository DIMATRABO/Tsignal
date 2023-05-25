class GetAllInput:
    webhook_id :str = None
    user_id: str = None

    def __init__(self, webhook_id=None, user_id=None):
        self.webhook_id = webhook_id
        self.user_id = user_id