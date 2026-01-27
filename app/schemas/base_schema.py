from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseModelSchema(BaseModel):
    ## Для базовых настроек
    model_config = ConfigDict(from_attributes=True)
