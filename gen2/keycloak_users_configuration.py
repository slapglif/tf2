
from keycloak import KeycloakAdmin

def configure_keycloak_users():
    # Connect to Keycloak
    keycloak_admin = KeycloakAdmin(server_url="https://auth.id.music",
                                   username="admin",
                                   password="password",
                                   realm_name="prod",
                                   verify=True)

    # Define a sample user
    user = {
        "username": "mbrown",
        "enabled": True,
        "email": "mbrown@solvd.com",
        "firstName": "Mike",
        "lastName": "Brown",
        "credentials": [{"type": "password", "value": "1121"}]
    }

    # Create the sample user
    keycloak_admin.create_user(payload=user)

    print('Keycloak users have been configured.')

# Calling the function to configure the Keycloak users

