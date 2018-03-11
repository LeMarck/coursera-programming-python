import asyncio

METRIC = []


class ServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport

    def data_received(self, data: bytes):
        req = data.decode()[:-1].split(' ')
        method = req[0]
        query = req[1:]
        if method == 'get':
            res = self._get(query)
        elif method == 'put':
            res = self._put(query)
        else:
            res = 'error\nwrong command\n\n'
        self.transport.write(res.encode())

    @staticmethod
    def _get(query):
        if len(query) != 1:
            return 'error\nwrong command\n\n'

        data = list(map(lambda info: ' '.join(info),
                        METRIC if query[0] == '*' else filter(
                            lambda info: info[0] == query[0],
                            METRIC)))

        res = '\n'.join(['ok'] + data)

        return f'{res}\n\n'

    @staticmethod
    def _put(query):
        if len(query) != 3:
            return 'error\nwrong command\n\n'

        data = list(filter(lambda info: info == query, METRIC))
        if len(data) == 0:
            METRIC.append(query)

        return 'ok\n\n'


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(ServerProtocol, host, int(port))

    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()
