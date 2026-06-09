class DomainError(Exception):
    pass


class HubError(DomainError):
    pass


class ConnectionError(DomainError):
    pass
