from pydantic import BaseModel, Field

class ResultData(BaseModel):
    estimated_delivery_price: float = Field(alias="estimated_delivery_price")
    index_price: float = Field(alias="index_price")

class DeribitPriceSchemaResponseRPCResponse(BaseModel):
    jsonrpc: str = Field(default="2.0")
    result_data: ResultData = Field(alias="result")
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool