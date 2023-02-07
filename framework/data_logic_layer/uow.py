class BaseUnitOfWork:

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def rollback(self):
        pass

    def commit(self):
        pass
