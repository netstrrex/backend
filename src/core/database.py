from abc import ABC, abstractmethod
from typing import Any


class AbstractDatabase(ABC):
    @abstractmethod
    async def create_pool(self) -> None:
        """
        Create a database connection pool asynchronously.

        This method should be called during application initialization
        to establish and manage a pool of reusable connections.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def close_pool(self) -> None:
        """
        Close the database connection pool asynchronously.

        This method should be called when the application is shutting down
        to gracefully release all database connections.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(self, sql: str, *args: Any) -> None:
        """
        Execute an SQL query asynchronously.

        Args:
            sql (str): The SQL query string to be executed.
            *args (Any): Positional arguments to substitute into the query
                (e.g., parameters for prepared statements).

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def fetch(
        self, sql: str, *args: Any
    ) -> tuple[
        dict[Any, Any] | dict[str, Any] | dict[str, str] | dict[bytes, bytes], ...
    ]:
        """
        Execute an SQL query asynchronously and fetch multiple rows.

        Args:
            sql (str): The SQL query string to be executed.
            *args (Any): Positional arguments to substitute into the query
                (e.g., parameters for prepared statements).

        Returns:
            tuple[dict]: A list of rows, where each row is represented as a dictionary
            mapping column names to their corresponding values.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def create_schema_if_not_exist(self) -> None:
        """
        Create the database schema if it does not already exist.

        This method is intended to initialize the required database structures
        (e.g., tables, indexes, constraints) when setting up the application.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
