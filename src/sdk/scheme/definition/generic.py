from marshmallow import Schema, post_load, post_dump


class DataObjectScheme(Schema):
    @classmethod
    def iter_from(cls, schema_object, keys):
        for key in keys:
            yield key, getattr(schema_object, key)

    @post_dump(pass_many=False)
    def clean(self, data, **kwargs):
        if "route" in data:
            data["cid"] = data["route"]
            del data["route"]
        return data

    @post_load
    def to_object(self, data, **kwargs):
        """
        Build generic Schema type from dict
        :param data: dict with schema data
        :return: SchemaMeta(**data)
        """

        attrs = data.copy()
        meta_params = {"register": False}
        attrs["Meta"] = type(
            "GeneratedMeta", (getattr(self.__class__, "Meta", object),), meta_params
        )
        schema_cls = type(self.__class__.__name__, (self.__class__,), attrs)
        schema_cls.iterable = lambda: self.iter_from(schema_cls, data.keys())
        return schema_cls
