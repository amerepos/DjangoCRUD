class BaseSchema:
    PATH = ''


    def get(self):
        raise NotImplemented('GET not Implemented!')

    def post(self, **data):
        raise NotImplemented('POST not Implemented!')

    def put(self, **data):
        raise NotImplemented('PUT not Implemented!')

    def delete(self):
        raise NotImplemented('DELETE not Implemented!')
