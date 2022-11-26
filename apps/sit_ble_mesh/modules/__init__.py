class Module:
    def __init__(self):
        pass

    def initialize(self, app):
        self.app = app

    def setup_cli(self, parser):
        pass

    async def handle_cli(self, args):
        pass
