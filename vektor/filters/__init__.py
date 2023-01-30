from loader import dp
from .referral_start import ReferralStart


if __name__ == "filters":
    dp.filters_factory.bind(ReferralStart)
