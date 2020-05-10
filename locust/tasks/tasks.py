from locust import HttpLocust, TaskSet, task

class FlowException(Exception):
   pass

class CRUD(TaskSet):

    @task(1)
    def testcrud(self):

        # step 1 create 
        new_user = {
            "userName": "TestUser",
            "firstName": "Donald",
            "lastName": "Tramp",
            "email": "donald.tramp@usa.com"
        }
        usercreate_response = self.client.post('/otusapp/users', json=new_user, name="createuser", headers={'Host': 'arch.homework'})
        if usercreate_response.status_code != 200:
           raise FlowException('User not created')
        user_id = usercreate_response.json().get('id')

        # step 2 read 
        userread_response = self.client.get(f'/otusapp/users/{user_id}', name='readusers[id]', headers={'Host': 'arch.homework'})
        if userread_response.status_code != 200:
           raise FlowException('User not read')

        # step 3 update 
        updated_user = {
            "userName": "UpdatedUser",
            "firstName": "Vasya",
            "lastName": "Pupkin",
            "email": "vasy.pupkin@russia.ru"
        }
        userupdate_response = self.client.put(f'/otusapp/users/{user_id}', json=updated_user, name='updateuser[id]', headers={'Host': 'arch.homework'})
        if userupdate_response.status_code != 200:
           raise FlowException('User not updated')

        # step 4 delete 
        deleteuser_response = self.client.delete(f'/otusapp/users/{user_id}', name='deleteuser[id]', headers={'Host': 'arch.homework'})
        if deleteuser_response.status_code != 200:
           raise FlowException('User not delete')

    @task(1)
    def stop(self):
        self.interrupt()

class UserBehavior(TaskSet):

    tasks = {CRUD: 1}

    # test homepage 
    @task(2)
    def home(self):
        post_response = self.client.get('/otusapp/', name="home", headers={'Host': 'arch.homework'})
        if post_response.status_code != 200:
            raise FlowException('Host not found')

    # test /health
    @task(3)
    def health(self):
        post_response = self.client.get('/otusapp/health', name="health", headers={'Host': 'arch.homework'})
        if post_response.status_code != 200:
           raise FlowException('Health not found')


    # get all users
    @task(2)
    def readallusers(self):
        allusersread_response = self.client.get(f'/otusapp/users/', name='getusers', headers={'Host': 'arch.homework'})
        if allusersread_response.status_code != 200:
           raise FlowException('Users not read')

class TestUsersCRUD(HttpLocust):
  task_set = UserBehavior
  min_wait = 1000
  max_wait = 3000