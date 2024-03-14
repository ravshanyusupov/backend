from src.apps.dictionary.services.crud import district_crud
from src.apps.users.models import User
from ninja_lib.error import DomainException


class ProductNormDomain:
    def __init__(self, user, data) -> None:
        self.user = user
        self.user_type = user.user_type
        self.data = data


class ProductNormCore(ProductNormDomain):
    async def check_for_district(self):
        if self.data.district_id and self.user_type == User.CEC:
            raise DomainException(4006)
        if not self.data.district_id and self.user_type == User.REGION:
            raise DomainException(4008)

    async def check_whether_the_user_region_matches_the_provided_region(self):
        if not (self.data.region_id == self.user.region_id):
            raise DomainException(4007)

    async def check_if_the_district_is_located_in_this_region(self):
        instance = await district_crud.read(pk=self.data.district_id)
        if not (self.data.region_id == instance.region_id):
            raise DomainException(4009)

    async def check_whether_the_user_district_matches_the_provided_district(self):
        if not (self.data.district_id == self.user.district_id):
            raise DomainException(4010)

    async def check_instance_for_district(self):
        if self.data.district and self.user_type == User.CEC:
            raise DomainException(4011)
        if not self.data.district and self.user_type == User.REGION:
            raise DomainException(4011)

    async def check_if_the_district_is_located_in_this_user_region(self):
        instance = await district_crud.read(pk=self.data.district_id)
        if not (self.user.region_id == instance.region_id):
            raise DomainException(4011)


class ProductNormCreate(ProductNormCore):
    async def validator(self):
        filters = {
            User.CEC: self.check_cec_user_payload,
            User.REGION: self.check_region_user_payload,
        }

        filter_args = filters.get(self.user_type)
        await filter_args()

    async def check_cec_user_payload(self):
        await self.check_for_district()

    async def check_region_user_payload(self):
        await self.check_whether_the_user_region_matches_the_provided_region()
        await self.check_for_district()
        await self.check_if_the_district_is_located_in_this_region()


class ProductNormRead(ProductNormCore):
    async def validator(self):
        filters = {
            User.CEC: self.allow_any,
            User.REGION: self.check_instance_for_region_user,
            User.DISTRICT: self.check_instance_for_district_user,
        }

        filter_args = filters.get(self.user_type)
        await filter_args()

    async def allow_any(self):
        pass

    async def check_instance_for_region_user(self):
        await self.check_whether_the_user_region_matches_the_provided_region()

    async def check_instance_for_district_user(self):
        await self.check_whether_the_user_district_matches_the_provided_district()


class ProductNormPatch(ProductNormCore):
    def __init__(self, user, data, payload) -> None:
        super().__init__(user, data)
        self.payload = payload

    async def validator(self):
        filters = {
            User.CEC: self.check_instance_for_cec_user,
            User.REGION: self.check_instance_for_region_user,
        }

        filter_args = filters.get(self.user_type)
        await filter_args()

        if self.payload.region_id or self.payload.district_id:
            await ProductNormCreate(self.user, self.payload).validator()

    async def check_instance_for_cec_user(self):
        await self.check_instance_for_district()

    async def check_instance_for_region_user(self):
        await self.check_instance_for_district()
        await self.check_if_the_district_is_located_in_this_user_region()


class ProductNormDelete(ProductNormCore):
    async def validator(self):
        filters = {
            User.CEC: self.check_instance_for_cec_user,
            User.REGION: self.check_instance_for_region_user,
        }

        filter_args = filters.get(self.user_type)
        await filter_args()

    async def check_instance_for_cec_user(self):
        await self.check_instance_for_district()

    async def check_instance_for_region_user(self):
        await self.check_instance_for_district()
        await self.check_if_the_district_is_located_in_this_user_region()
