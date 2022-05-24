from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    database_dsn: str
    database_table: str
    rapidpro_host: str
    rapidpro_token: str
    concurrency: int
    urn_type: str

    @classmethod
    def from_environment(cls: "type[Config]", env: dict[str, str]) -> "Config":
        try:
            database_dsn = env["DATABASE_DSN"]
            database_table = env["DATABASE_TABLE"]
            rapidpro_host = env["RAPIDPRO_HOST"]
            rapidpro_token = env["RAPIDPRO_TOKEN"]
            urn_type = env["URN_TYPE"]
        except KeyError as e:
            raise KeyError(f"Cannot find required environment variable {e.args[0]}")
        try:
            concurrency = int(env.get("CONCURRENCY", "1"))
        except ValueError:
            raise ValueError("CONCURRENCY environment variable is not an integer")
        return cls(
            database_dsn,
            database_table,
            rapidpro_host,
            rapidpro_token,
            concurrency,
            urn_type,
        )
