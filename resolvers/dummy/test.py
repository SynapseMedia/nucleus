class DummyResolver:
    def __str__(self):
        return 'Test'

    def __call__(self, *args, **kwargs):
        return {}
