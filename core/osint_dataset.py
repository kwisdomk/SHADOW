"""
core/osint_dataset.py
Kenyan fraud OSINT synthetic dataset and intelligence layer.
Provides a deterministic threat simulation, prompt grounding, and testing layer.
"""

import random

# 1. Load Structure (Metadata & SCAM_CATEGORIES)
METADATA = {
    "source": "OSINT & Public Cyber Threat Advisories (Safaricom, DCI, KRA, Africa Check)",
    "region": "Kenya",
    "target_audience": "Hackathon MVP - Defensive AI Training",
    "last_updated": "2026-05-06"
}

SCAM_CATEGORIES = {
    "mpesa_reversal": {
        "name": "M-Pesa Fake Reversal Scam",
        "common_structure": "Fake system generated M-Pesa SMS + Follow-up frantic text/call begging for a refund.",
        "linguistic_markers": ["by mistake", "rudisha", "mtoto yuko hosi", "tafadhali", "balance is *LOCKED*"],
        "red_flags": ["Sender is a regular phone number (07xx) not 'MPESA'", "Grammar errors in system text", "High emotional pressure"],
        "synthetic_examples": [
            "MPESA ODG1LIPNX1 Confirmed.You have received Ksh 8,500 from JOHN MWANGI 06/05/26 New M-PESA balance is *(LOCKED)* Pay bills via M-PESA.",
            "Maze si ulifungiwa na MPESA yako? Boss nisamehe nilituma by mistake. Rudisha tu hiyo 5k haraka acha nishughulikie mgonjwa.",
            "Aki naomba urudishe ile pesa nimekutumia by mistake saa hii. Ni ya fees ya mtoto tafadhali."
        ]
    },
    "safaricom_impersonation": {
        "name": "Safaricom Impersonation / USSD Hijack",
        "common_structure": "Authority figure warning about account block + instruction to dial a USSD code (usually call forwarding or M-Pesa pin reset).",
        "linguistic_markers": ["line yako imefungwa", "double registration", "customer care", "piga *33*"],
        "red_flags": ["Sender is not 0722000000", "Use of fear/threat of disconnection", "Instructions to dial obscure MMI/USSD codes"],
        "synthetic_examples": [
            "Habari kutoka Safaricom. Laini yako inatumika na mtu mwingine (double registration). Piga *33*0000* kuzuia hii haraka.",
            "Dear Customer, your M-Pesa account will be suspended in 2 hours due to lack of update. Click https://safaricom-update.cc to verify.",
            "Customer care: We have detected unusual activity on your line. Reply with your ID number and M-Pesa PIN to secure your account."
        ]
    },
    "fuliza_scam": {
        "name": "Fuliza Limit Boost Scam",
        "common_structure": "Social media style text offering an impossible upgrade to Safaricom's overdraft limit, demanding an upfront 'activation' fee.",
        "linguistic_markers": ["sema thanks", "nikuboostie fuliza", "hakuna stress", "limit up to 100k", "fuliza limit yako"],
        "red_flags": ["Promises to bypass official Safaricom algorithms", "Requires upfront payment to unlock credit", "Uses excessive Sheng/slang for a financial product"],
        "synthetic_examples": [
            "KAMA ULIPATA FULIZA SEMA THANKS. Inbox nikuboostie fuliza from 0 to 100k in 2 minutes hii January hakuna stress.",
            "Safaricom promotion: Kuongeza Fuliza limit yako hadi 50,000, tuma KES 300 kwa Till 889XXX for system activation.",
            "Niaje buda, niko na mchoro wa ku-hack Fuliza. Tuma 500 nikuwekee limit ya 80k sai sai."
        ]
    },
    "kra_penalty": {
        "name": "Fake KRA Penalty / Arrest Threat",
        "common_structure": "Impersonation of Kenya Revenue Authority (KRA) citing unpaid taxes, threatening arrest, and providing a rogue payment link or number.",
        "linguistic_markers": ["tax arrears", "utashtakiwa", "masaa 48", "warrant of arrest", "KRA ALERT"],
        "red_flags": ["KRA does not issue arrest warrants via SMS", "Payment directed to a mobile number instead of official PayBill 220220", "Extreme urgency"],
        "synthetic_examples": [
            "KRA ALERT: Uko na tax arrears ya KES 23,450 kwa iTax system yako. Lipa ndani ya masaa 48 au utashtakiwa. Call 0756XXXXXX sasa.",
            "FINAL NOTICE: A warrant of arrest has been issued against your ID for tax evasion. Pay KES 5,000 clearance fee via link: kra-clearance.info",
            "Mzee, hii ni KRA. Uko na penalty ya 15k. Wacha mchezo, lipa sai ndio tusitume mapolisi kwa ofisi yako."
        ]
    },
    "betting_scam": {
        "name": "Betting / Jackpot Scams",
        "common_structure": "False notification of a massive jackpot win from popular Kenyan betting sites (SportPesa, Betika), requesting a 'withdrawal fee'.",
        "linguistic_markers": ["umeshinda jackpot", "SportPesa ya 50K", "registration fee", "withdrawal code"],
        "red_flags": ["Winning a contest you never entered", "Requirement to pay money to receive money", "Sender uses a standard phone number"],
        "synthetic_examples": [
            "Hongera! Wewe ndio mshindi wa 500k SportPesa Weekly Jackpot. Tuma 2,500 ya registration fee kupokea pesa kwa MPESA yako leo.",
            "Betika: Namba yako imechaguliwa kushinda KES 75,000. Tuma 1,050 processing fee kwa Till namba 554XXX kupata withdrawal code.",
            "Boss, niko na fixed matches za leo uhakika 100%. Tuma 1k nikutumie odds za 50, usikose hii form."
        ]
    },
    "bonga_points": {
        "name": "Bonga Points Theft",
        "common_structure": "Fake expiry warning designed to panic the user into clicking a phishing link, or an agent tricking the user into transferring points.",
        "linguistic_markers": ["zina-expire leo", "redeem for cash", "Bonga points zako"],
        "red_flags": ["Links leading to non-Safaricom domains", "Unsolicited requests for Bonga PINs"],
        "synthetic_examples": [
            "Safaricom: Bonga points zako (10,500) zina-expire leo saa sita usiku. Click hapa kuredeem kwa cash haraka: bit.ly/bonga-redeem",
            "Dear customer, convert your 5,000 Bonga points to KES 1,500 cash. Reply with your M-Pesa PIN to authorize transfer.",
            "Your expenditure of Ksh50 worth 250 points to Otenyo Momanyi Aruya Till 5307214 was successful."
        ]
    },
    "whatsapp_deregistration": {
        "name": "WhatsApp Deregistration / OTP Theft",
        "common_structure": "Scammer triggers a WhatsApp login code to the victim's phone, then messages claiming they sent it by mistake to steal the account.",
        "linguistic_markers": ["nilituma code", "by mistake", "naomba unitumie", "WhatsApp verification"],
        "red_flags": ["Anyone asking for a 6-digit SMS code", "Sudden WhatsApp registration SMS when you aren't logging in"],
        "synthetic_examples": [
            "Boss nisamehe, nilituma code ya WhatsApp kwa namba yako by mistake. Naomba unitumie hiyo code 6-digits haraka niingie kwa group ya kazi.",
            "WARNING: Your WhatsApp is being deregistered on this device. Share the SMS code sent to you to cancel the deregistration.",
            "Niaje buda, simu yangu imeharibika, na-login kwa simu mpya. Nimekutumia code, isomee ndio ni-activate WhatsApp."
        ]
    },
    "fake_jobs": {
        "name": "Fake Job / Recruitment Scams",
        "common_structure": "Offer for a lucrative, often international or NGO job (UN, TSC) that requires an upfront 'facilitation' or 'medical' fee.",
        "linguistic_markers": ["shortlisted", "NGO jobs", "medical fee", "facilitation fee", "interview tomorrow"],
        "red_flags": ["Paying to get a job", "Guaranteed employment", "Interviews scheduled via informal SMS"],
        "synthetic_examples": [
            "Dear applicant, you have been shortlisted for the UN NGO Data Clerk position. Pay KES 1,500 medical fee to Till 8392XX before interview tomorrow.",
            "TSC Recruitment 2026: Umechaguliwa. Tuma 3,000 ya processing fee kwa HR Manager 0712XXXXXX kureserve position yako.",
            "Niko na mchoro ya job huku Qatar. Tuma 5k ya kuanzisha process ya visa, mshahara ni 150k per month. Wacha mchezo."
        ]
    },
    "chama_sacco": {
        "name": "Chama / SACCO / Family Emergency",
        "common_structure": "Targeted social engineering. Scammer hacks a WhatsApp group or spoofs a number to impersonate a treasurer or relative in distress.",
        "linguistic_markers": ["nimepata accident", "tuma haraka", "chama contribution", "ntakurudishia"],
        "red_flags": ["Sudden change in payment numbers for a Chama", "Refusal to take a voice call during an 'emergency'"],
        "synthetic_examples": [
            "Buda, nimepata accident hapa Naivasha. Tuma 3k haraka nilipe doctor, ntakurudishia jioni niki-settle.",
            "Members, our Chama account is undergoing maintenance. Please send this month's 5k contribution to the new Treasurer Till: 8821XX.",
            "Mum, simu yangu imeanguka kwa maji na niko shule. Tuma fare 1,500 kwa hii namba ya mwalimu ndio nirudi home."
        ]
    },
    "otp_sim_swap": {
        "name": "SIM Swap / Banking OTP Theft",
        "common_structure": "Sophisticated phishing attempting to get the user's National ID and Banking OTPs to initiate a SIM Swap and drain accounts.",
        "linguistic_markers": ["system upgrade", "confirm your details", "National ID", "Equity mobile"],
        "red_flags": ["Bank/Telco calling from a personal line", "Requests for National ID over SMS"],
        "synthetic_examples": [
            "Dear Equity Bank customer, your mobile banking is due for an upgrade. Reply with your National ID and the OTP sent to you to avoid account suspension.",
            "Safaricom: We are upgrading the network in your area. Please confirm your ID number to prevent your line from being switched off.",
            "Mzee, mimi ni agent wa bank yako. Tuko na system error, hebu nisomee ile code imeingia kwa simu yako ndio turudishe pesa yako."
        ]
    }
}

# 3. Risk Mapping
RISK_MAPPING = {
    "mpesa_reversal": "HIGH",
    "safaricom_impersonation": "CRITICAL",
    "fuliza_scam": "CRITICAL",
    "kra_penalty": "CRITICAL",
    "otp_sim_swap": "CRITICAL",
    "betting_scam": "MEDIUM",
    "fake_jobs": "MEDIUM",
    "bonga_points": "MEDIUM",
    "chama_sacco": "HIGH",
    "whatsapp_deregistration": "HIGH"
}

# 2. Core Functions
def get_category(category_id: str) -> dict:
    """Returns the dictionary for a specific scam category."""
    return SCAM_CATEGORIES.get(category_id, {})

def search_by_keyword(text: str) -> list:
    """
    Searches through all categories' linguistic markers for a match.
    Returns a list of dicts with category_id and data.
    """
    results = []
    text_lower = text.lower()
    for cat_id, cat_data in SCAM_CATEGORIES.items():
        for marker in cat_data.get("linguistic_markers", []):
            if marker.lower() in text_lower:
                results.append({"category_id": cat_id, "data": cat_data})
                break
    return results

def get_random_example(category_id: str, deterministic: bool = True) -> str:
    """
    Returns an example string from a category.
    If deterministic is True, it returns a predictable example without randomness.
    """
    category = get_category(category_id)
    if not category:
        return ""
        
    examples = category.get("synthetic_examples", [])
    if not examples:
        return ""
        
    if deterministic:
        # Pseudo-deterministic choice based on the length of the category name
        index = len(category.get("name", "")) % len(examples)
        return examples[index]
    
    return random.choice(examples)

def classify_synthetic_message(text: str) -> dict:
    """
    Classifies a message and assigns a probable category and risk level.
    Implements a special SAFE Detection check for legitimate M-Pesa.
    """
    text_lower = text.lower()
    
    # 4. SAFE Detection (Legitimate MPESA confirmation patterns)
    if "confirmed" in text_lower and "received" in text_lower and "ksh" in text_lower:
        # Ensure it lacks common reversal or scam terms before calling it safe
        if not any(x in text_lower for x in ["by mistake", "rudisha", "locked"]):
            return {
                "probable_category": "legitimate_transaction",
                "risk_level": "LOW",
                "matched_markers": []
            }

    # Perform keyword search
    matches = search_by_keyword(text)
    
    if not matches:
        return {
            "probable_category": "unknown",
            "risk_level": "UNKNOWN",
            "matched_markers": []
        }
        
    # Pick the highest risk match
    best_match = matches[0]
    best_risk = RISK_MAPPING.get(best_match["category_id"], "UNKNOWN")
    
    risk_weights = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0, "UNKNOWN": -1}
    for match in matches:
        risk = RISK_MAPPING.get(match["category_id"], "UNKNOWN")
        if risk_weights.get(risk, -1) > risk_weights.get(best_risk, -1):
            best_match = match
            best_risk = risk

    # Find which markers were actually matched
    matched_markers = [marker for marker in best_match["data"]["linguistic_markers"] if marker.lower() in text_lower]

    return {
        "probable_category": best_match["category_id"],
        "risk_level": best_risk,
        "matched_markers": matched_markers
    }

# 6. Output Smoke Test
if __name__ == "__main__":
    print("=" * 60)
    print(" Shadow OSINT Dataset - Smoke Test")
    print("=" * 60)
    
    test_cases = [
        "Maze nilikosea nikatuma thao, rudisha haraka",
        "KRA ALERT: Uko na tax arrears ya KES 23,450 kwa iTax system yako.",
        "Confirmed. You have received KSh 500 from John."
    ]
    
    for case in test_cases:
        print(f"\n[Test] Message: '{case}'")
        result = classify_synthetic_message(case)
        print(f"Probable Category : {result.get('probable_category')}")
        print(f"Risk Level        : {result.get('risk_level')}")
        if result.get("matched_markers"):
            print(f"Matched Markers   : {result.get('matched_markers')}")
        print("-" * 60)
