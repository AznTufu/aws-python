import threading
from requests import Session, HTTPError
import time

class TEST():
    def __init__(self):
        
        self.session = Session()
        self.base_url = "https://pdfv2l2ceg.execute-api.eu-west-1.amazonaws.com/dev"
        
    def get_user (self):
        try:
            headers = {
                "httpMethod": "GET",
                "x-api-key": "bd15b0ef-968f-4bfb-9bdd-8e0f3f151bee"
            }
                    
            res = self.session.get(
                url=f"{self.base_url}/manageUser",
                headers=headers
            )
            print(res.text)
            res.raise_for_status()
        except HTTPError as e:
             print(f"HTTPError: {e.response.status_code} - {e.response.text}")

    def create_user(self, email):
        try:
            body = {
                 "email": email
            }

            res = self.session.post(
                url=f"{self.base_url}/getToken",
                json=body
            )
            print(res.text)
            res.raise_for_status()
            
            token_api = res.json().get('hash_value')
            if token_api:
                self.session.headers.update({"x-api-key": token_api})
                print(f"Token: {token_api}")
            else:
                print("No token")

        except HTTPError as e:
             print(f"HTTPError: {e.response.status_code} - {e.response.text}")

    def run_threads(self):
        emails = [
            "user1@domain.com", 
            "user2@domain.com", 
            "user3@domain.com"
        ]
        
        threads_create = []
        user_ids = []
        
        for email in emails:
            t = threading.Thread(target=self.create_user_thread, args=(email, user_ids))
            threads_create.append(t)
            t.start()
        
        for t in threads_create:
            t.join()

        threads_get = []
        for user_id in user_ids:
            t = threading.Thread(target=self.get_user, args=(user_id,))
            threads_get.append(t)
            t.start()
        
        for t in threads_get:
            t.join()

    def create_user_thread(self, email, user_ids):
        user_id = self.create_user(email)
        if user_id:
            user_ids.append(user_id)
            
test = TEST()
test.run_threads()
time.sleep(5)
test.run_threads()