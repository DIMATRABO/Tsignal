class GetAllInput:
    webhook_id :str = None

    def __init__(self, webhook_id=None):
        self.webhook_id = webhook_id
        