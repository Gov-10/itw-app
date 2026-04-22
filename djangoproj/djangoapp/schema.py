from ninja import Schema
from typing import Optional
class UploadSchema(Schema):
    file_name:str
    content_type:Optional[str]="pdf"
