"""Feature extraction shared by train_model.py and app.py.

IMPORTANT: the order of features here must stay the same between
training and prediction, otherwise the model gets wrong inputs.
"""
import re

KEYWORDS = ["urgent", "verify", "password", "click here", "bank",
            "suspended", "account", "login", "confirm", "winner", "free"]

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
IP_RE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}")
SHORTENERS = ("bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "cutt.ly")


def find_urls(text):
    return URL_RE.findall(text.lower())


def extract_features(text):
    """Return a list of numeric features (17 values)."""
    t = text.lower()
    urls = find_urls(t)
    feats = [
        len(urls),                                    # number of URLs
        max([len(u) for u in urls], default=0),       # longest URL length
        int(bool(IP_RE.search(t))),                   # URL uses an IP address
        sum("@" in u for u in urls),                  # '@' inside URLs
        sum("-" in u for u in urls),                  # '-' inside URLs
        t.count("!"),                                 # exclamation marks
    ]
    feats += [t.count(k) for k in KEYWORDS]           # keyword counts
    return feats


def red_flags(text):
    """Human-readable reasons why an email looks suspicious."""
    t = text.lower()
    urls = find_urls(t)
    flags = []

    found = [k for k in KEYWORDS if k in t]
    if found:
        flags.append("Suspicious keywords found: " + ", ".join(found))
    if urls:
        flags.append(f"{len(urls)} link(s) found in the email")
    if IP_RE.search(t):
        flags.append("A link uses a raw IP address instead of a domain name")
    if any("@" in u for u in urls):
        flags.append("A link contains '@' (often used to hide the real site)")
    if any(u.count("-") >= 2 for u in urls):
        flags.append("A link has many '-' symbols (common in fake domains)")
    if any(s in u for u in urls for s in SHORTENERS):
        flags.append("A shortened link is used (real destination is hidden)")
    if any(u.startswith("http://") for u in urls):
        flags.append("A link uses http:// (not secure)")
    if t.count("!") >= 3:
        flags.append("Many exclamation marks (pressure / urgency tone)")
    return flags


def advice(risk, text):
    """Practical next steps for the user, based on the risk level."""
    t = text.lower()
    tips = []
    if risk == "HIGH":
        tips += [
            "Do not click any link or open any attachment.",
            "Do not reply, and never share your password, OTP, PIN or card details.",
            "Report it as phishing or spam in your mail app, then delete it.",
            "If you already clicked or entered details: change that password now, "
            "turn on 2-step verification, and call your bank if money is involved.",
            "In India you can report cyber fraud at cybercrime.gov.in or call 1930.",
        ]
    elif risk == "MEDIUM":
        tips += [
            "Do not click the links yet.",
            "Check the sender’s full email address, not just the display name.",
            "Open the official website by typing its address yourself, then check your account there.",
            "If it claims to be from someone you know, confirm by phone or chat.",
        ]
    else:
        tips += [
            "Still check the sender’s email address before you act.",
            "Hover over links to see the real address before clicking.",
            "Never share OTP or passwords by email, even if the mail looks normal.",
        ]
    if IP_RE.search(t):
        tips.append("Real companies do not ask you to log in on a number-only address.")
    if "password" in t or "verify" in t:
        tips.append("Banks and big companies never ask for your password by email.")
    if any(w in t for w in ("urgent", "suspended", "immediately")):
        tips.append("Pressure to act fast is a classic trick. Stop and think first.")
    return tips
