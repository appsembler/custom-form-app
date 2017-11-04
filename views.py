from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from openedx.core.lib.api.authentication import (
    SessionAuthenticationAllowInactiveUser,
    OAuth2AuthenticationAllowInactiveUser,
)

from openedx.core.djangoapps.user_api.errors import UserNotFound, UserNotAuthorized, AccountUpdateError, AccountValidationError
from openedx.core.lib.api.parsers import MergePatchParser
from .api import update_account_settings, get_account_settings


class CMCUserProfileView(APIView):
	"""
	**Use Cases**

        Get or update a user's InterSystems User Profile information. Updates are supported
        only through merge patch.

    **Example Requests**:

        GET /api/user/v1/cmcuserprofile/{username}

        PATCH /api/user/v1/cmcuserprofile/{username}/{"key":"value"} "application/merge-patch+json"

    **Response Values for GET**

        If the user makes the request for her own account, or makes a
        request for another account and has "is_staff" access, the response
        contains:

        * username: The username associated with the account.

        * organization: The Organization associated with the user

        * job_title: The Job Title associated with the user

        * cmc_username: The Coordinate My Care Username associated with the user.


        For all text fields, clients rendering the values should take care
        to HTML escape them to avoid script injections, as the data is
        stored exactly as specified. The intention is that plain text is
        supported, not HTML.

        If no user exists with the specified username, a 404 error is
        returned.

    **Response Values for PATCH**

        Users can only modify their own account information. If the
        requesting user does not have username "username", this method will
        return with a status of 403 for staff access but a 404 for ordinary
        users to avoid leaking the existence of the account.

        If no user exists with the specified username, a 404 error is
        returned.

        If "application/merge-patch+json" is not the specified content type,
        a 415 error is returned.

        If the update could not be completed due to validation errors, this
        method returns a 400 error with all error messages in the
        "field_errors" field of the returned JSON.

        If the update could not be completed due to a failure at the time of
        the update, a 400 error is returned with specific errors in the
        returned JSON collection.

        If the update is successful, a 204 status is returned with no
        additional content.
	"""
	authentication_classes = (OAuth2AuthenticationAllowInactiveUser, SessionAuthenticationAllowInactiveUser)
	permission_classes = (permissions.IsAuthenticated,)
	parser_classes = (MergePatchParser,)

	def get(self, request, username):
	    """
	    GET /api/user/v1/cmcuserprofile/{username}
	    """
	    try:
	        account_settings = get_account_settings(request.user, username, view=request.QUERY_PARAMS.get('view'))
	    except UserNotFound:
	        return Response(status=status.HTTP_403_FORBIDDEN if request.user.is_staff else status.HTTP_404_NOT_FOUND)

	    return Response(account_settings)

	def patch(self, request, username):
	    """
	    PATCH /api/user/v1/cmcuserprofile/{username}

	    Note that this implementation is the "merge patch" implementation proposed in
	    https://tools.ietf.org/html/rfc7396. The content_type must be "application/merge-patch+json" or
	    else an error response with status code 415 will be returned.
	    """
	    try:
	        with transaction.commit_on_success():
	            update_account_settings(request.user, request.DATA, username)
	    except UserNotAuthorized:
	        return Response(status=status.HTTP_403_FORBIDDEN if request.user.is_staff else status.HTTP_404_NOT_FOUND)
	    except UserNotFound:
	        return Response(status=status.HTTP_404_NOT_FOUND)
	    except AccountValidationError as err:
	        return Response({"field_errors": err.field_errors}, status=status.HTTP_400_BAD_REQUEST)
	    except AccountUpdateError as err:
	        return Response(
	            {
	                "developer_message": err.developer_message,
	                "user_message": err.user_message
	            },
	            status=status.HTTP_400_BAD_REQUEST
	        )

	    return Response(status=status.HTTP_204_NO_CONTENT)
