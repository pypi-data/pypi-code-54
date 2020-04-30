
# Exceptions
class Error(Exception):
    """ Base class for exceptions """
    pass

class ConfigFileNotFoundError(Error):
    """ O arquivo de configuração não foi encontrado! """
    pass

class KeyFileNotFoundError(Error):
    """ A chave secreta não foi encontrada! """
    pass
