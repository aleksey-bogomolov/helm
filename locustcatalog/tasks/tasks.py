from locust import HttpLocust, TaskSet, task
import faker

fake = faker.Faker()

class FlowException(Exception):
   pass

class CatalogTest(TaskSet):

    @task(10)
    def get_product_id(self):
        self.client.get('/products/' + str(fake.random_int(3, 100000)), name='product_id')
        if post_response.status_code != 200:
            raise FlowException('Get product error')

    @task(1)
    def search(self):
        self.client.get('/search?q=' + fake.word(), name='product_search')
        if post_response.status_code != 200:
            raise FlowException('Search error')


class TestUsersCRUD(HttpLocust):
  task_set = CatalogTest
  min_wait = 1000
  max_wait = 3000