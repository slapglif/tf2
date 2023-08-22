import boto3
from pydantic import BaseModel

REGION = 'us-east-2'

boto3.setup_default_session(
    region_name=REGION,
    profile_name='default',
)
class Data(BaseModel):
    subnet1: str
    subnet2: str
    alb_security_group: str
    keycloak_security_group: str