from typing import List
import authorizer
import schemas

authorizers: List[authorizer.Authorizer] = []

token = ""
for authorizer in authorizers:
    if authorizer.should_validate(token=token):
        token_info: schemas.TokenInfo = authorizer.get_valid_info(token=token)
