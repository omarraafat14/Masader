from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class TenCallesPerMinute(UserRateThrottle):
    scope = 'ten'

class FiveCallesPerMinute(AnonRateThrottle):
    scope = 'five'