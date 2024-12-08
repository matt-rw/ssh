"""
`.Server` is an interface that overrides `.ServerInterface`.
"""

from logging import getLogger

from paramiko.server import ServerInterface
from paramiko.common import (
    AUTH_FAILED,
    AUTH_SUCCESSFUL
)
from paramiko import (
    OPEN_SUCCEEDED,
    OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
)


logger = getLogger()


class SSHServerInterface(ServerInterface):
    """
    This class overrides Paramiko ServerInterface.

    Methods on this class are called from Paramiko's primary thread, so you
    shouldn't do too much work in them. (Nothing that blocks or sleeps).
    """

    def check_channel_request(self, kind, chanid):
        """
        Determine if a channel request of a given type will be granted, and 
        return ``OPEN_SUCCEEDED`` or an error code. This method is 
        called in server mode when the client requests a channel, after 
        authentication is complete.

         :param str kind:
            the kind of channel the client would like to open (usually
            ``"session"``).
        :param int chanid: ID of the channel
        :return: an `int` success or failure code (listed above)
        """
        if kind == 'session':
            logger.info('Session channel request accepted')
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def get_allowed_auths(self, username):
        """
        Return a list of authentication methods supported by the server.
        This list is sent to clients attempting to authenticate, to inform 
        them of authentication methods that might be successful.

        This "list" is actually a string of comma-separated names of types
        of authentication. Possible values are ``"password"``, 
        ``"publickey"``, and ``"none"``.

        The default implementation always returns ``"password"``.

        :param str username: the username requesting authentication.
        :return: a comma-separated `str` of authentication types
        """
        return 'publickey'

    def check_auth_none(self, username):
        """
        Determine if a client may open channels with no (further)
        authentication.

        Return ``AUTH_FAILED`` if the client must authenticate, or 
        ``AUTH_SUCCESSFUL`` if it's okay for the client to not 
        authenticate.

        The default implementation always returns ``AUTH_FAILED``.

        :param str username: the username of the client.
        :return:
            ``AUTH_FAILED`` if the authentication fails; ``AUTH_SUCCESSFUL``
            if it succeeds.
        :rtype: int
        """
        return AUTH_SUCCESSFUL

    def check_auth_password(self, username, password):
        """
        Determine if a given username and password supplied by the 
        client is acceptable for use in authentication.

        Return ``AUTH_FAILED`` if the password is not accepted,
        ``AUTH_SUCCESSFUL`` if the password is accepted and completes
        the authentication, or ``AUTH_PARTIALLY_SUCCESSFUL`` if your
        authentication is stateful, and this key is accepted for
        authentication, but more authentication is required. (In 
        this latter case, `get_allowed_auths` will be called to 
        report to the client what options it has for continuing 
        the authentication.)

        The default implementation always returns ``AUTH_FAILED``.

        :param str username: the username of the authenticating client.
        :param str password: the password given by the client.
        :return:
            ``AUTH_FAILED`` if the authentication fails;
            ``AUTH_SUCCESSFUL`` if it succeeds;
            ``AUTH_PARTIALLY_SUCCESSFUL`` if the password
            auth is successful, but the authentication must continue.
        :rtype: int
        """
        return AUTH_FAILED

    def check_auth_publickey(self, username, key):
        """
        Determine if a given key supplied by the client is acceptable
        for use in authentication. You should override this method
        in server mode to check the username and key and decide if you would
        accept a signature made using this key.

        Return ``AUTH_FAILED`` if the key is not accepted,
        ``AUTH_SUCCESSFUL`` if the key is accepted and completes the 
        authentication, or ``AUTH_PARTIALLY_SUCCESSFUL`` if your 
        authentication is stateful, and this key is accepted for 
        authentication, but more authentication is required. (In this 
        latter case, `get_allowed_auths` will be called to report to the 
        client what options it has for continuing the authentication.)

        Note that you don't have to actually verify any key 
        signature here. If you're willing to accept the key, Paramiko will do
        the work of verifying the client's signature.

        The default implementation always returns ``AUTH_FAILED``.

        :param str username: the username of the authenticating client
        :param .Pkey key: the key object provided by the client
        :return:
            ``AUTH_FAILED`` if the client can't authenticate with this key;
            ``AUTH_SUCCESSFUL`` if it can; ``AUTH_PARTIALLY_SUCCESSFUL`` if it
            can authenticate with this key but must continue with 
            authentication
        :rtype: int
        """
        return AUTH_SUCCESSFUL

    def check_auth_interactive(self, username, submethods):
        """Begin an interactive challenge, if supported."""
        return AUTH_FAILED

    def check_auth_interactive_response(self, responses):
        """Continue or finish an interactive authentication challenge."""
        return AUTH_FAILED

    # ...gssapi requests...

    def check_port_forward_request(self, address, port):
        """
        Handle a request for port forwarding. The client is asking
        that connections to the given address and port be forwarded back 
        across this ssh connection. An address of ``"0.0.0.0"`` indicates
        a global address (any address associated with this server) and a 
        port of ``0`` indicates that no specific port is requested (usually
        the OS will pick a port).

        The default implementation always returns ``False``, rejecting the
        port forwarding request. If the request is accepted, you should 
        return the port opened for listening.

        :param str address: the requested address
        :param int port: the requested port
        :return:
            the port number (`int`) that was opened for listening, 
            or ``False`` to reject
        """
        return False

    def cancel_port_forward_request(self, address, port):
        """
        The client would like to cancel a previous port-forwarding request.
        If the given address and port is being forwarded across this 
        ssh connection, the port should be closed.

        :param str address: the forwarded address
        :param int port: the forwarded port
        """
        pass

    def check_global_request(self, kind, msg):
        """
        Handle a global request of the given ``kind``. This method is called
        in server mode and client mode, whenever the remote host makes 
        a global request. If there are any arguments to the request, they 
        will be in ``msg``.

        There aren't any useful global requests defined, aside from port
        forwarding, so usually this type of request is an extension to the
        protocol.

        If the request was successful and you would like to return contextual 
        data to the remote host, return a tuple. Items in the tuple will be 
        sent back with the successful result. (Note that the items in the 
        tuple can only be strings, ints, or bools.)

        The default implementation always returns ``False``, indicating that 
        it does not support any global requests.

        .. note:: Port forwarding requests are handled separately, in 
            `check_port_forward_request`.

        :param str kind: the kind of global request being made.
        :param .Message msg: any extra arguments to the request.
        :return:
            ``True`` or a `tuple` of data if the request was granted;
            ``False`` otherwise.
        """
        return False

        # ...Channel requests...

        def check_channel_subsystem_request(self, channel, name):
            """
            Determine if a requested subsystem will be provided to the 
            client on the given channel. If this method returns ``True``, 
            all future I/O through this channel will be assumed to be 
            connected to the requested subsystem. An example of a subsystem 
            is ``sftp``.

            The default implementation checks for a subsystem handler assigned
            via `.Transport.set_subsystem_handler`. If one has been set, 
            the handler is invoked and this method returns ``True``. 
            Otherwise it returns ``False``.

            .. note:: Because the default implementation uses the `.Transport` 
                to identify valid subsystems, you probably won't need to 
                override this method.

            :param .Channel channel: the `.Channel` the pty request 
                arrived on.
            :param str name: name of the requested subsystem.
            :return:
                ``True`` if this channel is not hooked up to the requested
                subsystem; ``False`` if that subsystem can't or won't be 
                provided.
            """
            transport = channel.get_transport()
            handler_class, args, kwargs = transport._get_subsystem_handler(name)
            if handler_class is None:
                return False
            handler = handler_class(channel, name, self, *args, **kwargs)
            handler.start()
            return True

        def check_channel_forward_agent_request(self, channel):
            """
            Determine if the client will be provided with a forward agent
            session. If this method returns ``True``, the server will
            allow SSH Agent forwarding.

            The default implementation always returns ``False``.

            :param .Channel channel: the `.Channel` the request arrived on.
            :return: 
                ``True`` if the AgentForward was loaded; ``False`` if not

            If ``True`` is returned, the server should create an 
            :class:`AgentServerProxy` to access the agent.
            """
            return False

        def check_channel_direct_tcpip_request(self, chanid, origin, destination):
            """
            Determine if a local port forwarding channel will be granted, 
            and return ``OPEN_SUCCEEDED`` or an error code. This method is 
            called in server mode when the client requests a channel, after
            authentication is complete.

            The ``chanid`` parameter is a small number that uniquely
            identifies the channel within a `.Transport`. A `.Channel` object
            is not created unless this method returns ``OPEN_SUCCEEDED`` --
            once a `.Channel` object is created, you can call 
            `.Channel.get_id` to retrieve the channel ID.

            The origin and destination parameters are (ip_address, port) 
            tuples that correspond to both ends of the TCP connection in the 
            forwarding tunnel.

            The return value should either be ``OPEN_SUCCEEDED`` (for ``0``)
            to allow the channel request, or one of the following error 
            codes to reject it:

                - ``OPEN_FAILED_ADMINSTRATIVELY_PROHIBITED``
                - ``OPEN_FAILED_CONNECT_FAILED``
                - ``OPEN_FAILED_UNKNOWN_CHANNEL_TYPE``
                - ``OPEN_FAILED_RESOURCE_SHORTAGE``

            The default implementation always returns
            ``OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED``.

            :param int chanid: ID of the channel
            :param tuple origin:
                2-tuple containing the IP address and port of the 
                originator (client side)
            :param tuple destination:
                2-tuple containing the IP address and port of the 
                destination (server side)
            :return: an `int` success or failure code (listed above)
            """
            return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_channel_env_request(self, channel, name, value):
            """
            Check whether a given environment variable can be specified 
            for the given channel. This method should return ``True`` 
            if the server is willing to set the specified environment
            variable. Note that some environment variables (e.g., PATH)
            can be exceedingly dangerous, so blindly allowing the client 
            to set the environment is almost certainly not a good idea.

            The default implementation always returns ``False``.

            :param channel: the `.Channel` the env request arrived on
            :param str name: name
            :param str value: Channel value
            :returns: a boolean
            """
            return False

        def get_banner(self):
            """
            A pre-login banner to display to the user. The message may 
            span multiple lines separated by crlf pairs. The language 
            should be in rfc3066 style, for example: en-US.

            The default implementation always returns ``(None, None)``.

            :returns: A tuple containing the banner and language code.

            .. versionadded:: 2.3
            """
            return (None, None)






