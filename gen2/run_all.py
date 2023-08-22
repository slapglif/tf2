from gen2 import Data
from gen2.cognito_identity_pool_configuration import configure_cognito_identity_pool
from gen2.cognito_user_pool_configuration import configure_cognito_user_pool
from gen2.keycloak_clients_configuration import configure_keycloak_clients
from gen2.keycloak_federation_configuration import configure_keycloak_federation
from gen2.keycloak_oidc_idp_configuration import configure_keycloak_oidc_idp
from gen2.keycloak_provisioning_with_ecs import provision_keycloak_with_ecs
from gen2.keycloak_realms_configuration import configure_keycloak_realms
from gen2.keycloak_users_configuration import configure_keycloak_users
from gen2.load_balancer_configuration import configure_load_balancer
from gen2.networking_configuration import configure_networking

def main():
    global data
    try:
        print("provisioning infrastructure...")
        status = provision_keycloak_with_ecs()
        if not status:
            raise Exception("Failed to provision infrastructure")
    except Exception as e:
        print("An error occurred while provisioning infrastructure:", e)
        return

    try:
        # configure networking
        print("Starting Networking Configuration...")
        subnet1, subnet2, alb_security_group, keycloak_security_group = configure_networking()
        data = Data(
            subnet1=subnet1['Subnet']['SubnetId'],
            subnet2=subnet2['Subnet']['SubnetId'],
            alb_security_group=alb_security_group['GroupId'],
            keycloak_security_group=keycloak_security_group['GroupId']
        )
        print("Networking Configuration Completed.")
    except Exception as e:
        print("An error occurred during Networking Configuration:", e)
        return

    try:
        print("\nStarting Cognito Configuration...")
        status1 = configure_cognito_user_pool()
        status2 = configure_cognito_identity_pool()
        if not status1 or not status2:
            raise Exception("Failed to configure Cognito")
        print("Cognito Configuration Completed.")
    except Exception as e:
        print("An error occurred during Cognito Configuration:", e)
        return

    def _build_keycloak():
        try:
            """
            This function configures Keycloak
            :return:    None
            """
            print("Starting Keycloak Configuration...")
            status1 = configure_keycloak_realms()
            status2 = configure_keycloak_clients()
            status3 = configure_keycloak_users()
            status4 = configure_keycloak_oidc_idp()
            status5 = configure_keycloak_federation()
            if not status1 or not status2 or not status3 or not status4 or not status5:
                raise Exception("Failed to configure Keycloak")
            print("Keycloak Configuration Completed.")
        except Exception as e:
            print("An error occurred during Keycloak Configuration:", e)

    try:
        _build_keycloak()
    except Exception as e:
        print("An error occurred during Keycloak Configuration:", e)
        return

    try:
        print("\nStarting API Gateway Configuration...")
        status = configure_load_balancer(data)
        if not status:
            raise Exception("Failed to configure API Gateway")
        print("API Gateway Configuration Completed.")
    except Exception as e:
        print("An error occurred during API Gateway Configuration:", e)
        return

    print("\nAll configurations have been applied successfully!")

if __name__ == "__main__":
    main()
