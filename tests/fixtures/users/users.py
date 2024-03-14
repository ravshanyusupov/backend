import pytest


@pytest.fixture
def cec_user(cec_user_factory):
    user = cec_user_factory.create(
        username=cec_user_factory.username,
        user_type=cec_user_factory.user_type,
    )
    user.set_password(cec_user_factory.password)
    user.raw_password = cec_user_factory.password
    user.save()

    return user


@pytest.fixture
def region_user(region_user_factory):
    user = region_user_factory.create(
        username=region_user_factory.username,
        user_type=region_user_factory.user_type,
        region=region_user_factory.region,
    )
    user.set_password(region_user_factory.password)
    user.raw_password = region_user_factory.password
    user.save()

    return user


@pytest.fixture
def district_user(district_user_factory):
    user = district_user_factory.create(
        username=district_user_factory.username,
        user_type=district_user_factory.user_type,
        region=district_user_factory.region,
        district=district_user_factory.district,
    )
    user.set_password(district_user_factory.password)
    user.raw_password = district_user_factory.password
    user.save()

    return user
