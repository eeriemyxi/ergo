import io


class CustomStringIO(io.StringIO):
    def peek(self, n: int = 1) -> str:
        opos = self.tell()
        char = self.read(n)
        self.seek(opos)
        return char


def _pprint(*args, **kwargs):
    import pprint

    pprint.pprint(*args, **kwargs)


def isident(c: str) -> bool:
    return c.isalpha() or c == "-"
