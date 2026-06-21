
import jwt 
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings 

def return_response(statuscode, message, data=None):
    if data is not None:
        return {
            'status': statuscode,
            'message': message,
            'data': data
        }
    else:
        return {
            'status': statuscode,
            'message': message
        }


def Decode_JWt(auth_header):
    if not auth_header:
        print("Authorization header missing")
        raise AuthenticationFailed("Authorization header missing")

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        # check allowed_pattern
        # if not payload.get("allowed_pattern"):
        #     raise AuthenticationFailed("Unauthenticated")

        # if payload.get("allowed_pattern") in ["ONROADZ","ONROADZMOBILE"]:
        #     id = payload.get("id")
        #     # CHECK ID ACTIVE OR INACTIVE IN TABLE 
        #     if id:
        #         get_profile = Profile.objects.filter(id=id).first()
        #         if get_profile:
        #             if get_profile.is_active == 1:
        #                 raise AuthenticationFailed("User is not active")


        #     if payload.get("allowed_pattern") == "ONROADZMOBILE":
        #         # CHECK A MOBILE APP VERSION
        #         if not payload.get("mobile_app_version"):
        #             raise AuthenticationFailed("Unauthenticated")
        #         else:
        #             if payload.get("mobile_app_version") != settings.MOBILE_APP_VERSION:
        #                 raise AuthenticationFailed("Unauthenticated")
                
        #         if not payload.get("device_id"):
        #             raise AuthenticationFailed("Unauthenticated")
        #         else:
        #             if payload.get("device_id") != get_profile.device_id:
        #                 raise AuthenticationFailed("Unauthenticated")
        return payload

    except jwt.ExpiredSignatureError:
        # print("Token expired")
        raise AuthenticationFailed("Token expired")

    except jwt.InvalidTokenError:
        # print("Invalid token")
        raise AuthenticationFailed("Invalid token")

    except Exception as e:
        # print(e)
        # print("Unauthenticated")
        raise AuthenticationFailed("Unauthenticated")
