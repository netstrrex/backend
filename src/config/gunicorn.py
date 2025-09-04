from pydantic import BaseModel, Field


# noinspection PyArgumentList
class GunicornSettings(BaseModel):
    host: str = Field("0.0.0.0", env="GUNICORN__HOST")
    port: int = Field(8000, env="GUNICORN__PORT")
    workers: int = Field(1, env="GUNICORN__WORKERS")

    @property
    def bind(self) -> str:
        return f"{self.host}:{self.port}"
