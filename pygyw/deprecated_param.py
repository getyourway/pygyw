import warnings


class deprecated_param:
    def __init__(self, deprecated_args, reason):
        self.deprecated_args = set(deprecated_args.split())
        self.reason = reason

    def __call__(self, callable):
        def wrapper(*args, **kwargs):
            found = self.deprecated_args.intersection(kwargs)
            if found:
                msg = "Parameter(s) %s deprecated; %s" % (', '.join(map("'{}'".format, found)), self.reason)
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return callable(*args, **kwargs)

        return wrapper
