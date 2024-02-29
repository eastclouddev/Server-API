from pydantic_settings  import BaseSettings
import os
print(os.listdir("/etc"))
with open('/etc/envfile') as f:
    print(f.read())


class Settings(BaseSettings):
    APP_NAME: str = "My FastAPI App"
    DATABASE_URL: str

    class Config:
        extra = "allow"
        env_file = "etc/envfile"
        env_file_encoding = "utf-8"

settings = Settings()
