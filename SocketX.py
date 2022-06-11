import socket
# Bind and commands
#
class SocketX():

    @staticmethod
    def __create_socket():
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            )
        return server

    @staticmethod
    def __bind(server, id, port): # address and port
        server.bind(
            (id, port) 
            )

    @staticmethod
    def __setListen(server, x):
        server.listen(x)

    @staticmethod
    def __connect(server):
        user_socket, address = server.accept()
        return user_socket, address

    @staticmethod
    def __close(server):
        server.close()
