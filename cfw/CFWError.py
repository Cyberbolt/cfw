class CFWError(RuntimeError):
    pass


class ConfigurationCFWError(CFWError):
    pass

class WhitelistCFWError(CFWError):
    pass
