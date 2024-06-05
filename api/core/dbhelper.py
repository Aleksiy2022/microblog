from asyncio import current_task

from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine

from .config import settings


class DatabaseHelper:
    """
    Helper class for working with the database.

    This class provides methods for creating and configuring
    an asynchronous database engine and managed sessions.

    Attributes
    ----------
    engine : sqlalchemy.ext.asyncio.AsyncEngine
        The asynchronous database engine created based on the provided URL.
    session_factory : sqlalchemy.ext.asyncio.async_sessionmaker
        The factory for creating asynchronous sessions.
    sc_session : sqlalchemy.ext.asyncio.async_scoped_session
        The managed session associated with the current task.

    Methods
    -------
    init(self, url: str, echo: bool = False)
        Initializes an instance of DatabaseHelper with the specified parameters.
    get_scoped_session(self)
        Returns a new managed session associated with the current task.
    """

    def __init__(self, url: str, echo: bool = False):
        """
        Initialize an instance of DatabaseHelper.

        Parameters
        ----------
        url : str
            The URL for connecting to the database.
        echo : bool
            Flag indicating whether SQL queries should be logged.
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.sc_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )

    def get_scoped_session(self):
        """
        Return a new managed session associated with the current task.

        Returns
        -------
        sqlalchemy.ext.asyncio.async_scoped_session
            The managed session.
        """
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )


db_helper = DatabaseHelper(
    url=settings.db_url,
)
test_db_helper = DatabaseHelper(
    url=settings.test_db_url,
)
