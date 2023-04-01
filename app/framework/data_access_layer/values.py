class Empty:

    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Empty, cls).__new__(cls)
        return cls._instance
