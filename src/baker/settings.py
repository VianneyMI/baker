"""Module defining environment variables for this scraper."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

path_to_root = Path(__file__).parents[1]


class _Settings(BaseSettings):
    """Settings for this scraper."""

    # -----------------------------------------------------------------------------
    # OPENAI
    # -----------------------------------------------------------------------------
    openai_api_key: str
    openai_model: str = 'gpt-4-turbo'

    model_config = SettingsConfigDict(
        env_file=[
            path_to_root / '.env',

        ]
    )


SETTINGS = _Settings()

if __name__ == '__main__':
    print(path_to_root)
    # test linting
