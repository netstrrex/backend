from pydantic import BaseModel, Field


# noinspection PyArgumentList
class PostgresSettings(BaseModel):
    host: str = Field(..., env="POSTGRES__HOST")
    port: int = Field(5432, env="POSTGRES__PORT")
    database: str = Field(..., env="POSTGRES__DATABASE")
    user: str = Field(..., env="POSTGRES__USER")
    password: str = Field(..., env="POSTGRES__PASSWORD")

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
