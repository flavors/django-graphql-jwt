__all__ = ["PathDict"]


def filter_strings(items):
    return tuple(item for item in items if isinstance(item, str))


class PathDict(dict):
    def __repr__(self):
        return f"<{self.__class__.__name__}: {super().__repr__()}>"

    def insert(self, path, value):
        self[filter_strings(path)] = value

    def parent(self, path):
        path = filter_strings(path)

        for depth in range(len(path) - 1):
            parent = path[: -1 - depth]

            if parent in self:
                value = self[parent]

                if depth:
                    self[path[:-1]] = value
                return value
        return None
