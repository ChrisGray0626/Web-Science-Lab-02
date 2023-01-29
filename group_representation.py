from datetime import datetime, timezone

listTerms = ['news', 'report', 'journal', 'write', 'editor', 'analyst', 'analysis', 'media', 'updates', 'stories',
             'trader', 'investor', 'forex', 'stock', 'finance', 'market']
listSpam = ['ebay', 'review', 'shopping', 'deal', 'sale', 'sales', 'link', 'click', 'marketing', 'promote', 'discount',
            'products', 'store', 'diet', 'weight', 'porn', 'followback', 'follow back', 'lucky', 'winners', 'prize',
            'hiring']


def calc_description_weight(description_text):
    if description_text is None:
        return 0
    description_tokens = description_text.split(" ")
    description_weight = 0
    description_max_weight = len(description_tokens) * 2
    for token in description_tokens:
        if token in listTerms:
            description_weight += 2
        elif token in listSpam:
            description_weight += 0.1
        else:
            description_weight += 1
    description_weight /= description_max_weight

    return description_weight


def calc_account_age_weight(created_at):
    created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    now = datetime.now(timezone.utc)
    account_age = (now - created_at).days
    if account_age < 1:
        account_age_weight = 0.05
    elif account_age < 30:
        account_age_weight = 0.1
    elif account_age < 90:
        account_age_weight = 0.25
    else:
        account_age_weight = 1

    return account_age_weight


def calc_followers_weight(followers_count):
    if followers_count < 50:
        follower_weight = 0.5
    elif followers_count < 5000:
        follower_weight = 1
    elif followers_count < 10000:
        follower_weight = 1.5
    elif followers_count < 100000:
        follower_weight = 2
    elif followers_count < 200000:
        follower_weight = 2.5
    else:
        follower_weight = 3
    follower_weight /= 3

    return follower_weight


def calc_verified_weight(verified):
    if verified:
        verified_weight = 1.5
    else:
        verified_weight = 1
    verified_weight /= 1.5

    return verified_weight


def calc_profile_image_weight(default_profile_image):
    if default_profile_image:
        profile_image_weight = 0.5
    else:
        profile_image_weight = 1

    return profile_image_weight


def calc_user_weight(user_data):
    # Calculate description weight
    description_text = user_data["description"]
    description_weight = calc_description_weight(description_text)
    # Calculate account age weight
    created_at = user_data["created_at"]
    account_age_weight = calc_account_age_weight(created_at)
    # Calculate follower weight
    followers_count = user_data["followers_count"]
    follower_weight = calc_followers_weight(followers_count)
    # Calculate verified weight
    verified = user_data["verified"]
    verified_weight = calc_verified_weight(verified)
    # Calculate profile image weight
    default_profile_image = user_data["default_profile_image"]
    profile_image_weight = calc_profile_image_weight(default_profile_image)
    # Aggregate weights
    aggregate_weight = (
                               description_weight + account_age_weight + follower_weight + verified_weight + profile_image_weight) / 5
    if aggregate_weight > 0.65:
        print("High quality text")
    elif aggregate_weight < 0.45:
        print("Low quality text")

    return aggregate_weight
