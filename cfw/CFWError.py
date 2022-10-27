class CFWError(RuntimeError):
    pass


class ConfigurationCFWError(CFWError):
    pass


class ParameterCFWError(CFWError):
    pass


class ListCFWError(CFWError):
    pass
