"""cl.bin.cl"""

from __future__ import absolute_import

from kombu import Connection

from .base import Command, Option
from .. import Agent
from ..utils import instantiate

__all__ = ["cl", "main"]


class cl(Command):

    option_list = (
            Option("-i", "--id",
                default=None, action="store", dest="id",
                help="Id of the agent (or automatically generated)."),
            Option("-l", "--loglevel",
                default=None, action="store", dest="loglevel",
                help="Loglevel (CRITICAL/ERROR/WARNING/INFO/DEBUG)."),
            Option("-f", "--logfile",
                default=None, action="store", dest="logfile",
                help="Logfile. Default is stderr."),
            Option("-H", "--hostname",
                default=None, action="store", dest="hostname",
                help="Broker hostname."),
            Option("-P", "--port",
                default=None, action="store", type="int", dest="port",
                help="Broker port."),
            Option("-u", "--userid",
                default=None, action="store", dest="userid",
                help="Broker user id."),
            Option("-p", "--password",
                default=None, action="store", dest="password",
                help="Broker password."),
            Option("-v", "--virtual-host",
                default=None, action="store", dest="virtual_host",
                help="Broker virtual host"),
            Option("-T", "--transport",
                default=None, action="store", dest="transport",
                help="Broker transport"),
        )

    def run(self, *actors, **kwargs):
        id = kwargs.get("id")
        loglevel = kwargs.get("loglevel")
        actors = [instantiate(actor) for actor in list(actors)]

        connection = Connection(hostname=kwargs.get("hostname"),
                                port=kwargs.get("port"),
                                userid=kwargs.get("userid"),
                                password=kwargs.get("password"),
                                virtual_host=kwargs.get("virtual_host"),
                                transport=kwargs.get("transport"))
        agent = Agent(connection, actors=actors, id=kwargs.get("id"))
        agent.run_from_commandline(loglevel=kwargs.get("loglevel"),
                                   logfile=kwargs.get("logfile"))


def main(argv=None):
    return cl().execute_from_commandline(argv)


if __name__ == "__main__":
    main()
