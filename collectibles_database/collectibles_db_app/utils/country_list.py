from django.contrib.auth import get_user_model

User = get_user_model()

# fetching countries from user's db and adding to list
def get_country_names(user):
    items = user.collectible_items.all()
    country_names = set(item.country for item in items if item.country)
    # print(country_names)
    return list(country_names)
