import json

import requests
import yaml

config_yaml = 'vault_configs.yml'


def load_secrets():
    print('Loading yaml...')
    config = yaml.safe_load(open(config_yaml))
    vault_url = config['URL']
    role_id = config['ROLEID']
    secret_id = config['SECRETID']
    vault = config['VAULT']

    response = requests.request("POST", verify=False,
                                url=vault_url + "/v1/auth/ldap/login",
                                headers={'Content-Type': 'application/json'},
                                data='{"role_id": "%s", "secret_id": "%s"}' % (role_id, secret_id))

    j = response.json()

    session_token = j['auth']['client_token']
    who_am_i = j['auth']['metadata']['role_name']

    read_vault_response = requests.request("GET", verify=False,
                                           url=vault_url + vault,
                                           headers={'X-Vault-Token': session_token})
    vault_response_json = json.loads(response.text)['data']['data']
    print(vault_response_json)


if __name__ == "__main__":
    load_secrets()