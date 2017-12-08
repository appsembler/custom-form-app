from django.core.exceptions import ObjectDoesNotExist

from openedx.core.lib.api.view_utils import add_serializer_errors

from openedx.core.djangoapps.user_api.errors import (
    AccountUpdateError, AccountValidationError, 
    UserAPIInternalError, UserAPIRequestError, UserNotFound, UserNotAuthorized
)
from openedx.core.djangoapps.user_api.helpers import intercept_errors
from django.contrib.auth.models import User

from .models import CMCUserProfile
from .serializers import CMCUserProfileSerializer


# @intercept_errors(UserAPIInternalError, ignore_errors=[UserAPIRequestError])
def get_account_settings(requesting_user, username=None, configuration=None, view=None):
    """Returns TX Gateway profile information for a user serialized as JSON.

    Note:
        If `requesting_user.username` != `username`, this method will return differing amounts of information
        based on who `requesting_user` is and the privacy settings of the user associated with `username`.

    Args:
        requesting_user (User): The user requesting the account information. Only the user with username
            `username` or users with "is_staff" privileges can get full account information.
            Other users will get the account fields that the user has elected to share.
        username (str): Optional username for the desired account information. If not specified,
            `requesting_user.username` is assumed.
        configuration (dict): an optional configuration specifying which fields in the account
            can be shared, and the default visibility settings. If not present, the setting value with
            key ACCOUNT_VISIBILITY_CONFIGURATION is used.
        view (str): An optional string allowing "is_staff" users and users requesting their own
            account information to get just the fields that are shared with everyone. If view is
            "shared", only shared account information will be returned, regardless of `requesting_user`.

    Returns:
         A dict containing account fields.

    Raises:
         UserNotFound: no user with username `username` exists (or `requesting_user.username` if
            `username` is not specified)
         UserAPIInternalError: the operation failed due to an unexpected error.
    """

    if username is None:
        username = requesting_user.username

    has_full_access = requesting_user.username == username or requesting_user.is_staff

    if not has_full_access:
        return {}

    profile = _get_cmcuserprofile(username)

    cmc_profile_serializer = CMCUserProfileSerializer(profile)
    
    account_settings = dict(**cmc_profile_serializer.data)
    return account_settings


@intercept_errors(UserAPIInternalError, ignore_errors=[UserAPIRequestError])
def update_account_settings(requesting_user, update, username=None):
    """Update TX Gateway user profile information.

    Note:
        It is up to the caller of this method to enforce the contract that this method is only called
        with the user who made the request.

    Arguments:
        requesting_user (User): The user requesting to modify account information. Only the user with username
            'username' has permissions to modify account information.
        update (dict): The updated account field values.
        username (str): Optional username specifying which account should be updated. If not specified,
            `requesting_user.username` is assumed.

    Raises:
        UserNotFound: no user with username `username` exists (or `requesting_user.username` if
            `username` is not specified)
        UserNotAuthorized: the requesting_user does not have access to change the account
            associated with `username`
        AccountValidationError: the update was not attempted because validation errors were found with
            the supplied update
        AccountUpdateError: the update could not be completed. Note that if multiple fields are updated at the same
            time, some parts of the update may have been successful, even if an AccountUpdateError is returned;
            in particular, the user account (not including e-mail address) may have successfully been updated,
            but then the e-mail change request, which is processed last, may throw an error.
        UserAPIInternalError: the operation failed due to an unexpected error.
    """

    if username is None:
        username = requesting_user.username

    profile = _get_cmcuserprofile(username)

    if requesting_user.username != username:
        raise UserNotAuthorized()

    # Build up all field errors, whether read-only, validation, or email errors.
    field_errors = {}

    cmc_profile_serializer = CMCUserProfileSerializer(profile, data=update)

    for serializer in (cmc_profile_serializer, ):
        field_errors = add_serializer_errors(serializer, update, field_errors)

    # If we have encountered any validation errors, return them to the user.
    if field_errors:
        raise AccountValidationError(field_errors)

    try:
        # If everything validated, go ahead and save the serializers.
        cmc_profile_serializer.save()

    except Exception as err:
        raise AccountUpdateError(
            u"Error thrown when saving TX Gateway profile updates: '{}'".format(err.message)
        )


def _get_cmcuserprofile(username):
    """
    Helper method to return the legacy user and profile objects based on username.
    """
    try:
        existing_user = User.objects.get(username=username)
        existing_user_profile = CMCUserProfile.objects.get(user=existing_user)
    except ObjectDoesNotExist:
        raise UserNotFound()

    return existing_user_profile
