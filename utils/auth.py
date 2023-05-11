from azure.identity import DefaultAzureCredential


class AuthenticationError(Exception):
    """
    Exception raised when authentication fails.
    """
    pass


def get_credential() -> DefaultAzureCredential:
    """
    Authenticate to Azure services using the default credential chain.

    Returns:
        A DefaultAzureCredential object representing the authenticated credential.

    Raises:
        AuthenticationError: If the authentication fails.
    """
    try:
        credential = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True
        )
        return credential
    except Exception as e:
        print(f"Error: Authentication failed: {str(e)}")
        raise AuthenticationError(str(e))
