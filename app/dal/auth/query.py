class Query:

    def __init__(self):
        self._query = None
        self._mapper = None

    def set_query(self, query):
        self._query = query

    def set_mapper(self, mapper):
        self._mapper = mapper
