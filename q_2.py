from datetime import datetime, timezone

import util

listTerms = ['news', 'report', 'journal', 'write', 'editor', 'analyst', 'analysis', 'media', 'updates', 'stories',
             'trader', 'investor', 'forex', 'stock', 'finance', 'market']
listSpam = ['ebay', 'review', 'shopping', 'deal', 'sale', 'sales', 'link', 'click', 'marketing', 'promote', 'discount',
            'products', 'store', 'diet', 'weight', 'porn', 'followback', 'follow back', 'lucky', 'winners', 'prize',
            'hiring']

if __name__ == '__main__':
    dir_path = "data"
    jsons = util.load_jsons(dir_path)
    for json_data in jsons:
        # Calculate description weight
        description_text = json_data["user"]["description"]
        if description_text is None:
            description_weight = 0
        else:
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
        # Calculate account age weight
        created_at = json_data["user"]["created_at"]
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
        # Calculate follower weight
        followers_count = json_data["user"]["followers_count"]
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
        # Calculate verified weight
        verified = json_data["user"]["verified"]
        if verified:
            verified_weight = 1.5
        else:
            verified_weight = 1
        verified_weight /= 1.5
        # Calculate profile image weight
        default_profile_image = json_data["user"]["default_profile_image"]
        if default_profile_image:
            profile_image_weight = 0.5
        else:
            profile_image_weight = 1
        # Calculate quality score
        quality_score = (description_weight + account_age_weight + follower_weight + verified_weight + profile_image_weight) / 5
        if quality_score > 0.65:
            print("High quality text")
        elif quality_score < 0.45:
            print("Low quality text")
