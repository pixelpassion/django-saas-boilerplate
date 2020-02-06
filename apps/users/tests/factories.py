import factory

from apps.users.models import User

from .constants import TEST_PASSWORD


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "email{:03}@mail.com".format(n))
    username = factory.LazyAttribute(lambda user: f"{user.email}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    privacy_policy = True

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):  # noqa
        obj.set_password(TEST_PASSWORD)
        obj.save()
