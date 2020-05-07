class Extensions:
    class Path:
        """ Represents a flask path type, this passes
        the extra url parts instead of treating it like a url
        """
        pass
    
    class Request:
        """ Represents the url request data """
        pass


if __name__ == '__main__':
    print(Extensions.site_paths)
