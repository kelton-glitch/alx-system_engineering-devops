#!/usr/bin/python3
"""Function to count words in all hot posts on a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """Prints counts of given words found in a hot post given the subreddit.
    Args:
        subreddit (str); The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (dict): The dictionary of word counts.
        after (str): The next page in the listing.
        count (int): The total number of posts searched.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    try:
        results = response.json().get("data")
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return
    
    after = results.get("after")
    count += results.get("dist")
    for post in results.get("children"):
        title = post.get("data").get("title").lower().split()
        for word in word_list:
            instances[word] = instances.get(word, 0) + title.lower().split(
                " ").count(word.lower())
            if instances[word] == 0:
                del instances[word]
            else:
                instances[word] = instances[word]
    
    if after is None:
        if len(instances) == 0:
            print("")
            return
        for key, value in sorted(instances.items(),
                                 key=lambda item: (-item[1], item[0])):
            print("{}: {}".format(key, value))
        return
    else:
        return count_words(subreddit, word_list, instances, after, count)
