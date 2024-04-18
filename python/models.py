
from pydantic import BaseModel

# from typing import Any, Optional, Union

# class BasicResponse(BaseModel):
# 	success : bool
# 	error : Optional[str] = None
# 	message : Optional[str] = None

# class DataResponse(BasicResponse):
# 	data : Optional[Union[list, dict, Any]] = None

# class Responses:
# 	SUCCESS = 			BasicResponse(success=True,  message="The request has been completed")
# 	UNAUTHORIZED = 		BasicResponse(success=False, error="Unauthorized")
# 	NOT_IMPLEMENTED = 	BasicResponse(success=False, error="NotImplementedError")
# 	MISSING_PARAMETER = BasicResponse(success=False, error="Missing parameter.")
# 	INVALID_PARAMETER = BasicResponse(success=False, error="Invalid parameter.")

