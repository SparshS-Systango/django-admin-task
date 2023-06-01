
PLATFORMS = (
    ('paxnovelpay', 'paxnovelpay'),
    ('nexgoN86', 'nexgoN86'),
    ('paxemea', 'paxemea'),
    ('nexgoN6', 'nexgoN6')
)

USER_ROLES = (
    ('admin', 'admin'),
    ('employee', 'employee'),
)

PRODUCT_NAMES = (
    ('subscription_yavin', 'Abonnement Yavin'),
    ('renting_yavin', 'Location Yavin'),
    ('commission_proxi', 'Commissions Yavin flux proximite'),
    ('commission_vads', 'Commissions Yavin flux vads'),
    ("icpp_proxi", "Commissions CB, VISA, MASTERCARD d'interchange et d'acquisition flux proximite"),
    ("icpp_vads", "Commissions CB, VISA, MASTERCARD d'interchange et d'acquisition flux vads"),
    ('gateway_proxi', 'Frais de passerelle proximite'),
    ('gateway_vads', 'Frais de passerelle e-commerce'),
    ('chargeback', 'Commission litiges/impayes'),
    ('reimburse_unused_subscription', 'Remboursement abonnement en fin de mois'),
    ('sms', 'sms'),
    ('subscription_other', 'Abonnement'),
)

PRODUCT_NAME_TO_SHORT = {
    'commission_proxi': 'c-prox',
    'commission_vads': 'c-vads',
    'gateway_proxi': 'g-prox',
    'gateway_vads': 'g-vads',
    'monthly_subscription': 'sub',
    'quarterly_subscription': 'sub',
    'semester_subscription': 'sub',
    'annually_subscription': 'sub',
    'chargeback': 'chbk',
}

PRODUCT_NAME_TO_FEE_TYPE = {
    'subscription_yavin': 'monthly_subscription',
    'renting_yavin': 'monthly_subscription',
    'commission_proxi': 'commission_proxi',
    'commission_vads': 'commission_vads',
    "icpp_proxi": 'icpp_proxi',
    "icpp_vads": 'icpp_vads',
    'gateway_proxi': 'gateway_proxi',
    'gateway_vads': 'gateway_vads',
    'chargeback': 'chargeback',
    'sms': 'sms',
    'subscription_other': 'monthly_subscription',
    'reimburse_unused_subscription': 'reimburse_unused_subscription',
}

FEE_TYPE_TO_PRODUCT_NAME = {}
for k, v in PRODUCT_NAME_TO_FEE_TYPE.items():
    FEE_TYPE_TO_PRODUCT_NAME[v] = FEE_TYPE_TO_PRODUCT_NAME.get(v, []) + [k]

PRICING_PLAN_STATUSES = (
    ('open', 'open'),
    ('closed', 'closed')
)

VENDOR_TYPES = (
    ("reseller", "reseller"),
    ("cashback", "cashback"),
    ("accounting", "accounting"),
    ("yavin", "yavin"),
    ("unknown", "unknown"),
)

VENDOR_ECONOMIC_MODELS = (
    ("partnership", "partnership"), # there is no licence nor monthly retro commission
    ("retrocom", "retrocom"), # Yavin invoices the merchant and shares a retro commission to the vendor
    ("licence", "licence"), # the reseller invoices the merchant and pays a licence to Yavin
)
