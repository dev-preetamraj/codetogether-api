import logging
import requests

logger = logging.getLogger('accounts')


class GithubProvider:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self, auth_token: str) -> str | None:
        try:
            params = f'?client_id={self.client_id}&client_secret={self.client_secret}&code={auth_token}'
            res = requests.post(
                f'https://github.com/login/oauth/access_token{params}',
                headers={
                    "Accept": "application/json"
                }
            )
            if res.status_code == 200:
                data = res.json()
                return data.get('access_token')
            return None
        except Exception as e:
            logger.error(f'GithubProvider - get_access_token: {e}')
            return None

    def get_user(self, access_token: str):
        try:
            res = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f"Bearer {access_token}"
                }
            )
            if res.status_code != 200:
                return None
            return res.json()
        except Exception as e:
            logger.error(f'GithubProvider - get_user: {e}')
            return None

    def get_emails(self, access_token: str):
        try:
            res = requests.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f"Bearer {access_token}"
                }
            )

            if res.status_code != 200:
                return None
            return res.json()
        except Exception as e:
            logger.error(f'GithubProvider - get_emails: {e}')
            return None

    def get_primary_email(self, emails) -> str | None:
        for email in emails:
            if email.get('primary'):
                return email.get('email')
        return None
