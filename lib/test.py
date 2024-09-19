import toolkit.seldon_db_toolkit
import credentials as access


test1 = toolkit.retrieve_api_count(access)
test2 = toolkit.update_api_count(access, 1)
test3 = toolkit.retrieve_api_count(access)
print(test1)
print(test2)
print(test3)