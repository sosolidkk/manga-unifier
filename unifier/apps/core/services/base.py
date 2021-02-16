import logging
from abc import ABC, abstractmethod
from typing import List

logger = logging.getLogger(__name__)


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class Invoker:
    _on_start = None
    _on_finish = None
    _chain_of_commands = None

    def set_on_start(self, command: Command) -> None:
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        self._on_finish = command

    def set_chain_of_commands(self, commands: List[Command]) -> None:
        self._chain_of_commands = commands

    def invoke(self) -> None:
        if isinstance(self._on_start, Command):
            logger.info("Invoking on_start command")
            self._on_start.execute()

        if isinstance(self._chain_of_commands, List[Command]):
            logger.info("Invoking chain of commands")
            [command.execute() for command in self._chain_of_commands]

        if isinstance(self._on_finish, Command):
            logger.info("Invoking on_finish command")
            self._on_finish.execute()

        logger.info("Invoker has finished all commands successfully")
