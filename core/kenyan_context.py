"""
core/kenyan_context.py
Shadow — AI Fraud Detection System
AMD Hackathon 2026

Localized Kenyan fraud intelligence knowledge base.
Provides structured constants for scam classification, language detection,
fraud scoring, and pattern matching tuned to the Kenyan threat landscape.
"""

# ══════════════════════════════════════════════════════════════════════════════
# SCAM CATEGORIES
# ══════════════════════════════════════════════════════════════════════════════

SCAM_CATEGORIES = {
    "safaricom_impersonation": {
        "label": "Safaricom Impersonation",
        "description": "Fraudsters posing as Safaricom customer care, promotions, or network teams.",
        "risk_level": "HIGH",
        "keywords": [
            "safaricom", "customer care", "network upgrade", "sim registration",
            "promotion", "safaricom winner", "security update", "m-pesa pin",
            "deactivated", "update your details", "twaweza", "shinda"
        ],
        "example_patterns": [
            "Your Safaricom line will be suspended. Call 0700XXXXXX to verify.",
            "Niaje boss, laini yako ya Safaricom itafungwa leo. Tuma details zako nishughulikie haraka.",
        ],
    },

    "mpesa_reversal": {
        "label": "M-Pesa Reversal / Float Scam",
        "description": "Scammer claims mistaken send and asks for a refund, or fakes a transaction to an agent.",
        "risk_level": "HIGH",
        "keywords": [
            "sent by mistake", "refund", "reversal", "wrong number", "float",
            "agent", "rudisha", "nimekosea", "transaction failed", "pending"
        ],
        "example_patterns": [
            "Maze si ulifungiwa na MPESA yako? Boss nisamehe nilituma by mistake. Rudisha tu hiyo 500 haraka acha nishughulikie.",
            "I sent you KES 2,000 by mistake. Tafadhali rudisha niko na emergency ya hospitali."
        ],
    },

    "fuliza_scam": {
        "label": "Fuliza Abuse / Fake Alerts",
        "description": "Fake Fuliza overdraft notices demanding top-up fees or claiming fake debt.",
        "risk_level": "HIGH",
        "keywords": [
            "fuliza", "overdraft", "limit increased", "outstanding balance",
            "top-up fee", "crb", "clear your fuliza", "fuliza m-pesa"
        ],
        "example_patterns": [
            "Dear Customer, your Fuliza limit has been increased to KES 50,000. Send KES 500 to activate.",
            "Fuliza balance yako iko na arrears. Lipa sasa hivi au uwekwe CRB leo."
        ],
    },

    "betting_scam": {
        "label": "Betting / Jackpot Scam",
        "description": "Fake betting promotions, fixed matches, or 'jackpot won' messages.",
        "risk_level": "HIGH",
        "keywords": [
            "sportpesa", "betika", "odibets", "jackpot", "fixed odds", "multibet",
            "won", "congratulations", "registration fee", "sure bet", "odds"
        ],
        "example_patterns": [
            "Wewe umeshinda jackpot ya SportPesa ya 50K! Confirm details yako hapa: bit.ly/xxxxx Leo tu!",
            "100% Sure Fixed Matches available. Send KES 1,000 VIP registration fee to get today's odds."
        ],
    },

    "bonga_points_scam": {
        "label": "Bonga Points Scam",
        "description": "Fake notices to redeem Bonga points before expiry.",
        "risk_level": "MEDIUM",
        "keywords": [
            "bonga", "bonga points", "redeem", "expiry", "expire", "claim phones",
            "convert to cash", "dial *126#"
        ],
        "example_patterns": [
            "Your 15,000 Bonga points will expire today. Click here to redeem for KES 4,500 cash immediately.",
            "Redeem your Bonga points for a free smartphone. Tuma 500 ya delivery."
        ],
    },

    "kra_scam": {
        "label": "KRA Tax Scam",
        "description": "Fake Kenya Revenue Authority penalties, court summons, or tax arrears alerts.",
        "risk_level": "CRITICAL",
        "keywords": [
            "kra", "itax", "tax arrears", "overdue", "penalty", "court summons",
            "arrest", "warrant", "compliance", "pin certificate", "paye"
        ],
        "example_patterns": [
            "Mzee, hii ni KRA. Uko na arrears ya KES 23,450. Lipa ndani ya masaa 48 au utashtakiwa. Call 0756XXXXXX sasa.",
            "KRA Notice: Warrant of arrest issued for tax evasion. Call Inspector Kamau on 0722XXXXXX to clear."
        ],
    },

    "chama_scam": {
        "label": "Chama / SACCO Scam",
        "description": "Impersonation of SACCO officials or Chama treasurers requesting emergency transfers.",
        "risk_level": "MEDIUM",
        "keywords": [
            "chama", "sacco", "treasurer", "emergency fund", "contribution",
            "loan approval", "disbursement", "shares"
        ],
        "example_patterns": [
            "Niaje, member wa chama amepata ajali. Tuma contribution yako kwa hii namba mpya ya treasurer.",
            "Your SACCO loan of KES 100,000 is approved. Send KES 2,500 insurance fee to disburse."
        ],
    },
    
    "whatsapp_scam": {
        "label": "WhatsApp Deregistration Scam",
        "description": "Threatens WhatsApp account deletion and requests OTPs.",
        "risk_level": "CRITICAL",
        "keywords": [
            "whatsapp", "deregistered", "verification code", "blocked",
            "update whatsapp", "six digit code"
        ],
        "example_patterns": [
            "Your WhatsApp account is being registered on another device. Send the 6-digit code to cancel.",
            "Akaunti yako ya WhatsApp itafungwa. Confirm namba yako sasa."
        ],
    },

    "fake_job": {
        "label": "Fake Job Offer",
        "description": "Employment offers requiring upfront payments.",
        "risk_level": "MEDIUM",
        "keywords": [
            "job offer", "hiring now", "daily earnings", "registration fee",
            "training fee", "shortlisted", "send cv", "online job"
        ],
        "example_patterns": [
            "Urgent vacancy! Earn KSH 1,500/day. No experience needed. Send KSH 500 registration fee.",
            "Kazi iko. Pay KES 1,000 training fee to start immediately."
        ],
    },

    "sim_swap": {
        "label": "SIM Swap Attack",
        "description": "Social engineering to gain control of a phone number.",
        "risk_level": "CRITICAL",
        "keywords": [
            "sim swap", "sim replacement", "port number", "national id",
            "id card", "date of birth", "confirm identity", "verify account"
        ],
        "example_patterns": [
            "To complete your SIM replacement, provide your National ID and date of birth.",
            "Laini yako inabadilishwa. Call back immediately to cancel."
        ],
    },

    "otp_theft": {
        "label": "OTP / Code Theft",
        "description": "Phishing for one-time passwords via USSD push or fake app upgrades.",
        "risk_level": "CRITICAL",
        "keywords": [
            "otp", "verification code", "share code", "6 digit", "4 digit",
            "do not share", "stk push", "mobile banking update"
        ],
        "example_patterns": [
            "Safaricom is upgrading your account. The code we sent will confirm your new package. Nipatie hiyo code.",
            "Tumekutumia code ya M-banking. Soma hiyo code nikuwekee account sawa."
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# SHENG SCAM GLOSSARY
# ══════════════════════════════════════════════════════════════════════════════

SHENG_SCAM_GLOSSARY = {
    # Financial / M-Pesa terms
    "pesa":       "money",
    "mkwanja":    "cash / money",
    "chapaa":     "money",
    "hela":       "money (Swahili)",
    "doh":        "money (Sheng)",
    "send fare":  "send money for transport (common scam pretext)",
    "nitumie":    "send me (Swahili — often 'send me money')",
    "izo pesa":   "that money",
    
    # Scam action terms
    "ronga":      "con / trick",
    "thifte":     "steal",
    "nganya":     "con / overcharge",
    "mchoro":     "scheme / plan",
    "mchezaji":   "player / hustler / scammer",

    # Urgency / pressure terms
    "haraka":     "hurry / urgency",
    "sasa hivi":  "right now",
    "leo tu":     "today only",
    "shida":      "problem / trouble",
    "wacha mchezo": "stop playing around (pressure)",
    "acha story": "stop the stories / get to it",
    "funga deal": "close the deal",

    # Identity / trust manipulation
    "boss":       "term used to create false familiarity",
    "chief":      "term used to create false authority/trust",
    "mzee":       "elder/sir — used to sound respectful/legitimate",
    "buda":       "dad / old man",
    "budako":     "your dad",

    # Hooks
    "nipigie":    "call me",
    "sema":       "say / tell me",
    "click hapa": "click here",
    "code yako":  "your code",
    "confirm":    "confirm",
}

# ══════════════════════════════════════════════════════════════════════════════
# SWAHILI URGENCY PHRASES
# ══════════════════════════════════════════════════════════════════════════════

SWAHILI_URGENCY_PHRASES = [
    # Time pressure
    "haraka sana", "saa moja tu", "leo tu", "kesho itakuwa imechelewa",
    "muda mfupi", "ndani ya dakika", "usikawilie", "jibu sasa hivi", "fanya sasa",
    
    # Threat / consequence language
    "akaunti yako itafungwa", "nambari yako itakatwa", "utashtakiwa",
    "hatua za kisheria", "kupoteza pesa zako", "akaunti imezuiwa", "laini yako itazimwa",
    "uwekwe crb", "warrant ya kushikwa",
    
    # Authority impersonation
    "ofisi ya kra", "safaricom rasmi", "serikali ya kenya", "polisi wa kenya", "benki kuu",
    
    # Promise / reward urgency
    "umeshinda", "zawadi yako inakungoja", "pata pesa zako sasa", "nafasi ya mwisho",
]

# ══════════════════════════════════════════════════════════════════════════════
# FRAUD SCORING INDICATORS
# ══════════════════════════════════════════════════════════════════════════════

FRAUD_SCORING_INDICATORS = {
    # Critical signals (weight 3)
    "requests_otp_or_pin":         {"weight": 3, "category": "credential_theft",   "description": "Asks for OTP, PIN, or password"},
    "requests_national_id":        {"weight": 3, "category": "identity_theft",     "description": "Requests National ID number"},
    "sim_swap_language":           {"weight": 3, "category": "sim_swap",           "description": "Contains SIM swap request patterns"},
    "external_link_present":       {"weight": 3, "category": "phishing",           "description": "Contains URL to external site"},
    "impersonates_authority":      {"weight": 3, "category": "impersonation",      "description": "Poses as KRA, Safaricom, bank, or gov agency"},
    "whatsapp_deregistration":     {"weight": 3, "category": "account_takeover",   "description": "Threatens WhatsApp deregistration"},

    # High signals (weight 2)
    "requests_upfront_payment":    {"weight": 2, "category": "advance_fee",        "description": "Asks for fee/deposit to claim prize or job"},
    "unrealistic_returns":         {"weight": 2, "category": "investment_fraud",   "description": "Promises guaranteed or extreme profits"},
    "urgency_language_detected":   {"weight": 2, "category": "social_engineering", "description": "Uses high-pressure urgency phrases"},
    "threat_of_suspension":        {"weight": 2, "category": "intimidation",       "description": "Threatens account/line suspension"},
    "prize_win_claim":             {"weight": 2, "category": "lottery_scam",       "description": "Claims recipient has won a prize"},
    "wrong_number_reversal":       {"weight": 2, "category": "mpesa_fraud",        "description": "Claims wrong M-Pesa send, requests refund"},
    "fuliza_threat":               {"weight": 2, "category": "intimidation",       "description": "Threatens Fuliza CRB listing or demands fee"},

    # Moderate signals (weight 1)
    "sheng_scam_vocabulary":       {"weight": 1, "category": "language",           "description": "Contains known Sheng fraud vocabulary"},
    "swahili_urgency_phrase":      {"weight": 1, "category": "language",           "description": "Contains Swahili urgency/pressure phrases"},
    "unknown_sender_number":       {"weight": 1, "category": "identity",           "description": "Sender number not recognized or suspicious format"},
    "excessive_capitalization":    {"weight": 1, "category": "formatting",         "description": "Excessive use of CAPS for urgency"},
    "multiple_exclamation_marks":  {"weight": 1, "category": "formatting",         "description": "Three or more consecutive exclamation marks"},
    "calls_to_unknown_number":     {"weight": 1, "category": "redirection",        "description": "Directs user to call an unfamiliar number"},
}

MAX_FRAUD_SCORE = sum(v["weight"] for v in FRAUD_SCORING_INDICATORS.values())

def calculate_fraud_score(triggered_indicators: list[str]) -> dict:
    """
    Calculate fraud score and risk level using absolute raw score thresholds.
    """
    raw_score = 0
    breakdown = {}

    for key in triggered_indicators:
        if key in FRAUD_SCORING_INDICATORS:
            indicator = FRAUD_SCORING_INDICATORS[key]
            raw_score += indicator["weight"]
            breakdown[key] = indicator

    # Category combo bonus
    categories_hit = {ind["category"] for ind in breakdown.values()}
    if "credential_theft" in categories_hit and "impersonation" in categories_hit:
        raw_score += 2
        breakdown["combo_credential_impersonation"] = {"weight": 2, "category": "combo", "description": "High-risk combo: Impersonation + Credential theft"}

    normalised = round((raw_score / MAX_FRAUD_SCORE) * 100, 1)

    # Use absolute raw score thresholds for real-world accuracy
    if raw_score >= 6:
        risk_level = "CRITICAL"
    elif raw_score >= 4:
        risk_level = "HIGH"
    elif raw_score >= 2:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "raw_score":        raw_score,
        "max_score":        MAX_FRAUD_SCORE,
        "normalised_score": normalised,
        "risk_level":       risk_level,
        "breakdown":        breakdown,
    }


# ══════════════════════════════════════════════════════════════════════════════
# LEGITIMATE VS SUSPICIOUS PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

LEGITIMATE_PATTERNS = {
    "mpesa_confirmation": {
        "description": "Genuine M-Pesa transaction confirmation from Safaricom shortcode",
        "sender_patterns": ["MPESA", "M-PESA", "Safaricom"],
        "message_patterns": [
            r"[A-Z0-9]{10} Confirmed\.",             # Transaction code format
            r"Ksh[\d,]+\.00 sent to",                # Send confirmation
            r"You have received Ksh",                # Receive confirmation
            r"New M-PESA balance",                   # Balance notification
        ],
        "characteristics": [
            "Comes from official Safaricom shortcodes (e.g., MPESA)",
            "Contains valid 10-character transaction reference",
            "Never asks for PIN or personal info",
            "Balance shown matches expected transaction",
        ],
    },

    "bank_notification": {
        "description": "Legitimate bank alert from registered shortcode",
        "characteristics": [
            "Comes from registered bank shortcode",
            "Contains partial account number (masked)",
            "Does not ask for credentials",
        ],
    },

    "kra_itax": {
        "description": "Authentic KRA notification",
        "characteristics": [
            "Directs to itax.kra.go.ke (official domain only)",
            "Never asks for PIN via SMS",
            "References your specific KRA PIN number",
        ],
    },
}

SUSPICIOUS_PATTERNS = {
    "spoofed_sender": {
        "description": "Sender name mimics a legitimate entity but uses a different number",
        "signals": [
            "Displays 'Safaricom' or 'KRA' as sender but from a mobile number (07xx)",
            "Sender ID slightly misspelled: 'Saf4ricom', 'M-Pes4'",
        ],
    },

    "credential_extraction": {
        "description": "Message designed to harvest security credentials",
        "signals": [
            "Asks for M-Pesa PIN",
            "Requests OTP or verification code via STK push or call",
            "Asks user to 'confirm' by sending a code",
        ],
    },

    "fake_mpesa_send": {
        "description": "Fabricated M-Pesa confirmation to trick agent or seller",
        "signals": [
            "Screenshot of M-Pesa confirmation (cannot be verified via SMS)",
            "Claims transaction reference that doesn't follow Safaricom format",
            "Transaction reference contains lowercase letters",
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# KENYAN PHONE NUMBER PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

KENYAN_PHONE_PATTERNS = {
    # Updated 2025 prefixes
    "safaricom":  [r"^(\+?254|0)(7(0[0-9]|1[0-9]|2[0-9]|4[0-3]|4[5-6]|48|5[7-9]|6[8-9]|9[0-9])|1(1[0-5]))\d{6}$"],
    "airtel":     [r"^(\+?254|0)(7(3[0-9]|5[0-6]|6[2]|8[0-9])|1(0[0-6]))\d{6}$"],
    "telkom":     [r"^(\+?254|0)77\d{7}$"],
    "equitel":    [r"^(\+?254|0)76[3-6]\d{6}$"],
    "shortcodes": {
        "MPESA":       "Safaricom M-Pesa official sender",
        "Safaricom":   "Safaricom official communications",
        "KRA":         "Kenya Revenue Authority",
        "Equity":      "Equity Bank",
        "KCB":         "KCB Bank",
        "Co-opBank":   "Co-operative Bank",
    },
    "suspicious_prefixes": [
        "+1",   # US numbers used in some scams
        "+44",  # UK numbers
        "+234", # Nigerian numbers (419 scams)
        "+27",  # South African numbers
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# RISK LEVEL METADATA
# ══════════════════════════════════════════════════════════════════════════════

RISK_LEVELS = {
    "CRITICAL": {
        "score_range": (6, 100),
        "color":       "#FF1744",
        "emoji":       "🚨",
        "action":      "Do NOT comply. Block sender. Report to Safaricom/DCI.",
        "description": "Almost certainly a scam. Immediate danger.",
    },
    "HIGH": {
        "score_range": (4, 5),
        "color":       "#FF6D00",
        "emoji":       "⚠️",
        "action":      "Do not share any information. Verify independently.",
        "description": "Strong fraud indicators present.",
    },
    "MEDIUM": {
        "score_range": (2, 3),
        "color":       "#FFD600",
        "emoji":       "🔶",
        "action":      "Proceed with caution. Verify sender identity.",
        "description": "Some suspicious elements detected.",
    },
    "LOW": {
        "score_range": (0, 1),
        "color":       "#00C853",
        "emoji":       "✅",
        "action":      "Appears safe, but always stay alert.",
        "description": "No significant fraud signals detected.",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# REPORTING CONTACTS
# ══════════════════════════════════════════════════════════════════════════════

REPORTING_CONTACTS = {
    "Safaricom Fraud SMS":   "Forward SMS to 333 (Free)",
    "Safaricom Care":        "100 or 0722 000 000",
    "DCI Cybercrime Unit":   "+254 20 4343000 / cybercrime@dci.go.ke",
    "CA Kenya":              "complaints@ca.go.ke",
    "KRA Fraud Tip":         "fraudtipoffs@kra.go.ke",
    "Banking Fraud (CBK)":   "cps@centralbank.go.ke",
}
