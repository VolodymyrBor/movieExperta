from copy import deepcopy


class URL:

    def __init__(
        self,
        scheme: str,
        host: str,
        *,
        port: int | None = None,
        path: list[str] = None,
        params: dict[str, str] = None,
        username: str | None = None,
        password: str | None = None,
    ):
        self.password = password
        self.username = username
        self.path = path or []
        self.params = params or {}
        self.port = port
        self.host = host
        self.scheme = scheme

    @classmethod
    def parse(cls, url: str) -> 'URL':
        port = None
        params = None
        username = None
        password = None
        scheme, url = url.split('://')
        if '?' in url:
            url, params_str = url.split('?')
            params = {}
            for kv in params_str.split('&'):
                k, v = kv.split('=')
                params[k] = v
        host, *path = url.split('/')

        if '@' in host:
            host, auth = host.split('@')
            username, password = auth.splut(':')

        if ':' in host:
            host, port = host.split(':')
        return URL(
            scheme=scheme,
            host=host,
            port=int(port),
            path=path,
            params=params,
            username=username,
            password=password,
        )

    def joinpath(self, path: str) -> 'URL':
        url = deepcopy(self)
        url.path.append(path)
        return url

    def __str__(self):
        host = self.host
        if self.port is not None:
            host = f'{host}:{self.port}'

        if self.username and self.password:
            host = f'{self.username}:{self.password}@{host}'

        url_str = f'{self.scheme}://{host}'
        path = '/'.join(self.path)
        url_str = f'{url_str}/{path}'

        if self.params:
            str_params = '&'.join(f'{k}={v}' for k, v in self.params.items())
            url_str = f'{url_str}?{str_params}'

        return url_str

    def __truediv__(self, other: str) -> 'URL':
        if isinstance(other, str):
            return self.joinpath(other)
        return NotImplemented
