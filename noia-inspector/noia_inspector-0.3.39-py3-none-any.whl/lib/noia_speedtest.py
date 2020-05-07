from speedtest import Speedtest, InvalidServerIDType, build_request, catch_request, ServersRetrievalError, \
    get_response_stream, printer, get_exception, SpeedtestServersError, etree_iter, xml, \
    distance, NoMatchedServers, gzip

try:
    import xml.etree.ElementTree as ET
    try:
        from xml.etree.ElementTree import _Element as ET_Element
    except ImportError:
        pass
except ImportError:
    from xml.dom import minidom as DOM
    from xml.parsers.expat import ExpatError
    ET = None


class NoiaSpeedtest(Speedtest):

    def get_servers(self, servers=None, exclude=None):
        """Retrieve a the list of speedtest.net servers, optionally filtered
        to servers matching those specified in the ``servers`` argument
        """
        if servers is None:
            servers = []

        if exclude is None:
            exclude = []

        self.servers.clear()

        for server_list in (servers, exclude):
            for i, s in enumerate(server_list):
                try:
                    server_list[i] = int(s)
                except ValueError:
                    raise InvalidServerIDType(
                        '%s is an invalid server type, must be int' % s
                    )

        urls = [
            'https://speedtest.noia.network/servers.xml'
        ]

        headers = {}
        if gzip:
            headers['Accept-Encoding'] = 'gzip'

        errors = []
        for url in urls:
            try:
                request = build_request(
                    '%s?threads=%s' % (url,
                                       self.config['threads']['download']),
                    headers=headers,
                    secure=self._secure
                )
                uh, e = catch_request(request, opener=self._opener)
                if e:
                    errors.append('%s' % e)
                    raise ServersRetrievalError()

                stream = get_response_stream(uh)

                serversxml_list = []
                while 1:
                    try:
                        serversxml_list.append(stream.read(1024))
                    except (OSError, EOFError):
                        raise ServersRetrievalError(get_exception())
                    if len(serversxml_list[-1]) == 0:
                        break

                stream.close()
                uh.close()

                if int(uh.code) != 200:
                    raise ServersRetrievalError()

                serversxml = ''.encode().join(serversxml_list)

                printer('Servers XML:\n%s' % serversxml, debug=True)

                try:
                    try:
                        try:
                            root = ET.fromstring(serversxml)
                        except ET.ParseError:
                            e = get_exception()
                            raise SpeedtestServersError(
                                'Malformed speedtest.net server list: %s' % e
                            )
                        elements = etree_iter(root, 'server')
                    except AttributeError:
                        try:
                            root = DOM.parseString(serversxml)
                        except ExpatError:
                            e = get_exception()
                            raise SpeedtestServersError(
                                'Malformed speedtest.net server list: %s' % e
                            )
                        elements = root.getElementsByTagName('server')
                except (SyntaxError, xml.parsers.expat.ExpatError):
                    raise ServersRetrievalError()

                for server in elements:
                    try:
                        attrib = server.attrib
                    except AttributeError:
                        attrib = dict(list(server.attributes.items()))

                    if servers and int(attrib.get('id')) not in servers:
                        continue

                    if (int(attrib.get('id')) in self.config['ignore_servers']
                            or int(attrib.get('id')) in exclude):
                        continue

                    try:
                        d = distance(self.lat_lon,
                                     (float(attrib.get('lat')),
                                      float(attrib.get('lon'))))
                    except Exception:
                        continue

                    attrib['d'] = d

                    try:
                        self.servers[d].append(attrib)

                    except KeyError:
                        self.servers[d] = [attrib]

                break

            except ServersRetrievalError:
                continue

        if (servers or exclude) and not self.servers:
            raise NoMatchedServers()

        return self.servers
