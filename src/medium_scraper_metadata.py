import requests
import json
from typing import List
from supabase import create_client, Client
import time
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MEDIUM_COOKIE = os.getenv('MEDIUM_COOKIE')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

tags = [
    # 'marketing', 'social-media-marketing', 'business', 'technology', 
    # 'social-media', 'entrepreneurship', 'startup', 'innovation', 
    # 'productivity', 'leadership', 'design', 'programming', 'cryptocurrency', 
    # 'blockchain', 'artificial-intelligence', 'data-science', 'machine-learning', 
    # 'web-development', 'python', 'deep-learning', 'ux', 'cybersecurity', 
    # 'software-development', 'software-engineering', 'react', 'apple', 
    # 'android', 'finance', 'investing', 'venture-capital', 'equality', 
    # 'privacy', 'freelancing', 'product-management', 'data-engineering', 
    # 'data-visualization', 
    # 'writing', 'media', 'photography', 'creativity', 
    # 'culture', 'education', 'journalism', 'history', 'economics', 'politics', 
    # 'spirituality', 'health', 'mental-health', 'relationships', 'mindfulness', 
    # 'fitness', 'self-improvement', 'life-lessons', 'life', 'travel', 'books', 
    # 'art', 'fiction', 'humor', 'nonfiction', 'poetry', 
    # 'music', 'film', 'sports', 
    # 'gaming', 'climate-change', 'sustainability', 'virtual-reality', 'self-driving-cars', 
    # 'internet-of-things', 'this-happened-to-me', 'religion', 'space', 'race', 
    # 'architecture', 'justice', 'cooking', 'comics', 'women-in-tech', 'satire', 
    # 'short-story', 'work', 'family', 'parenting', 'style', 'sexuality',
    'guided-meditation'
]


def fetch_data_medium_api(to_: str, from_ : str, limit_: int, cookie: str, tag:str) -> dict:
    url = "https://medium.com/_/graphql"

    payload = json.dumps([
    {
        "operationName": "WebInlineTopicFeedQuery",
        "variables": {
        "tagSlug": tag,
        "paging": {
            "to": f"{to_}",
            "from": f"{from_}",
            "limit": limit_,
            "source": "fe4347fb-0dc2-4865-a7c4-c3fe44d4fe60"
        },
        "skipCache": True
        },
        "query": "query WebInlineTopicFeedQuery($tagSlug: String!, $paging: PagingOptions!, $skipCache: Boolean) {\n  personalisedTagFeed(tagSlug: $tagSlug, paging: $paging, skipCache: $skipCache) {\n    items {\n      ...InlineFeed_tagFeedItem\n      __typename\n    }\n    pagingInfo {\n      next {\n        source\n        limit\n        from\n        to\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment InlineFeed_tagFeedItem on TagFeedItem {\n  feedId\n  moduleSourceEncoding\n  reason\n  post {\n    ...StreamPostPreview_post\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment StreamPostPreview_post on Post {\n  id\n  ...StreamPostPreviewContent_post\n  ...PostPreviewContainer_post\n  __typename\n}\n\nfragment StreamPostPreviewContent_post on Post {\n  id\n  title\n  previewImage {\n    id\n    __typename\n  }\n  extendedPreviewContent {\n    subtitle\n    __typename\n  }\n  ...StreamPostPreviewImage_post\n  ...PostPreviewFooter_post\n  ...PostPreviewByLine_post\n  ...PostPreviewInformation_post\n  __typename\n}\n\nfragment StreamPostPreviewImage_post on Post {\n  title\n  previewImage {\n    ...StreamPostPreviewImage_imageMetadata\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment StreamPostPreviewImage_imageMetadata on ImageMetadata {\n  id\n  focusPercentX\n  focusPercentY\n  alt\n  __typename\n}\n\nfragment PostPreviewFooter_post on Post {\n  ...PostPreviewFooterSocial_post\n  ...PostPreviewFooterMenu_post\n  ...PostPreviewFooterMeta_post\n  __typename\n  id\n}\n\nfragment PostPreviewFooterSocial_post on Post {\n  id\n  ...MultiVote_post\n  allowResponses\n  isPublished\n  isLimitedState\n  postResponses {\n    count\n    __typename\n  }\n  __typename\n}\n\nfragment MultiVote_post on Post {\n  id\n  creator {\n    id\n    ...SusiClickable_user\n    __typename\n  }\n  isPublished\n  ...SusiClickable_post\n  collection {\n    id\n    slug\n    __typename\n  }\n  isLimitedState\n  ...MultiVoteCount_post\n  __typename\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  __typename\n}\n\nfragment PostPreviewFooterMenu_post on Post {\n  id\n  ...BookmarkButton_post\n  ...OverflowMenuButton_post\n  __typename\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  isPublished\n  ...SusiClickable_post\n  __typename\n}\n\nfragment OverflowMenuButton_post on Post {\n  id\n  visibility\n  ...OverflowMenu_post\n  __typename\n}\n\nfragment OverflowMenu_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  ...AddToCatalogBase_post\n  ...ExplicitSignalMenuOptions_post\n  __typename\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment ExplicitSignalMenuOptions_post on Post {\n  ...NegativeSignalModal_post\n  __typename\n  id\n}\n\nfragment NegativeSignalModal_post on Post {\n  id\n  creator {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  collection {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment NegativeSignalModal_publisher on Publisher {\n  __typename\n  id\n  name\n}\n\nfragment PostPreviewFooterMeta_post on Post {\n  isLocked\n  postResponses {\n    count\n    __typename\n  }\n  ...usePostPublishedAt_post\n  ...Star_post\n  __typename\n  id\n}\n\nfragment usePostPublishedAt_post on Post {\n  firstPublishedAt\n  latestPublishedAt\n  pinnedAt\n  __typename\n  id\n}\n\nfragment Star_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewByLine_post on Post {\n  creator {\n    ...ReadNextPostAuthorDetails_user\n    __typename\n    id\n  }\n  collection {\n    ...ReadNextPostAuthorDetails_collection\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment ReadNextPostAuthorDetails_user on User {\n  ...useIsVerifiedBookAuthor_user\n  ...userUrl_user\n  ...UserMentionTooltip_user\n  ...UserAvatar_user\n  __typename\n  id\n}\n\nfragment useIsVerifiedBookAuthor_user on User {\n  verifications {\n    isBookAuthor\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment UserMentionTooltip_user on User {\n  id\n  name\n  bio\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  membership {\n    tier\n    __typename\n    id\n  }\n  name\n  username\n  ...userUrl_user\n}\n\nfragment UserFollowButton_user on User {\n  ...UserFollowButtonSignedIn_user\n  ...UserFollowButtonSignedOut_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedIn_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment ReadNextPostAuthorDetails_collection on Collection {\n  ...CollectionLinkWithPopover_collection\n  __typename\n  id\n}\n\nfragment CollectionLinkWithPopover_collection on Collection {\n  ...collectionUrl_collection\n  ...CollectionTooltip_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment CollectionTooltip_collection on Collection {\n  id\n  name\n  slug\n  description\n  subscriberCount\n  customStyleSheet {\n    header {\n      backgroundImage {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  ...CollectionAvatar_collection\n  ...CollectionFollowButton_collection\n  ...EntityPresentationRankedModulePublishingTracker_entity\n  __typename\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment CollectionFollowButton_collection on Collection {\n  __typename\n  id\n  name\n  slug\n  ...collectionUrl_collection\n  ...SusiClickable_collection\n}\n\nfragment SusiClickable_collection on Collection {\n  ...SusiContainer_collection\n  __typename\n  id\n}\n\nfragment SusiContainer_collection on Collection {\n  name\n  ...SignInOptions_collection\n  ...SignUpOptions_collection\n  __typename\n  id\n}\n\nfragment SignInOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment EntityPresentationRankedModulePublishingTracker_entity on RankedModulePublishingEntity {\n  __typename\n  ... on Collection {\n    id\n    __typename\n  }\n  ... on User {\n    id\n    __typename\n  }\n}\n\nfragment PostPreviewInformation_post on Post {\n  readingTime\n  isLocked\n  ...Star_post\n  ...usePostPublishedAt_post\n  __typename\n  id\n}\n\nfragment PostPreviewContainer_post on Post {\n  id\n  extendedPreviewContent {\n    isFullContent\n    __typename\n  }\n  visibility\n  pinnedAt\n  ...PostScrollTracker_post\n  ...usePostUrl_post\n  __typename\n}\n\nfragment PostScrollTracker_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  sequence {\n    sequenceId\n    __typename\n  }\n  __typename\n}\n\nfragment usePostUrl_post on Post {\n  id\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  collection {\n    id\n    domain\n    slug\n    __typename\n  }\n  isSeries\n  mediumUrl\n  sequence {\n    slug\n    __typename\n  }\n  uniqueSlug\n  __typename\n}\n"
    }
    ])
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'apollographql-client-name': 'lite',
    'apollographql-client-version': 'main-20241010-135743-d42bbd2e3c',
    'content-type': 'application/json',
    'cookie': cookie,
    'dnt': '1',
    'graphql-operation': 'WebInlineTopicFeedQuery',
    'medium-frontend-app': 'lite/main-20241010-135743-d42bbd2e3c',
    'medium-frontend-path': '/?tag=startup',
    'medium-frontend-route': 'homepage',
    'origin': 'https://medium.com',
    'priority': 'u=1, i',
    'referer': 'https://medium.com/?tag=startup',
    'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def insert_items_metadata_supabase(items: List[dict], tag:str) -> None:
    rows_to_insert = []
    for item in items:
        post = item.get('post', {})
        creator = post.get('creator', {})
        collection = post.get('collection')
        extended_preview_content = post.get('extendedPreviewContent', {})
        verifications = creator.get('verifications', {})
        post_responses = post.get('postResponses', {})

        # Handle possible None values for 'collection'
        slug = collection.get('slug') if collection else None
        domain = collection.get('domain') if collection else None
        description = collection.get('description') if collection else None
        subscriber_count = collection.get('subscriberCount') if collection else None

        # Convert timestamps from milliseconds to seconds and format as datetime strings
        first_published_at = post.get('firstPublishedAt')
        if first_published_at:
            first_published_at = datetime.fromtimestamp(first_published_at / 1000, tz=timezone.utc).isoformat()

        # Build the row to insert
        row = {
            'title': post.get('title'),
            'subtitle': extended_preview_content.get('subtitle'),
            'creator_name': creator.get('name'),
            'is_book_author': verifications.get('isBookAuthor'),
            'bio': creator.get('bio'),
            'medium_url': post.get('mediumUrl'),
            'slug': slug,
            'domain': domain,  # Changed 'DOMAIN' to 'domain' to match column name
            'description': description,
            'subscriber_count': subscriber_count,
            'post_responses_count': post_responses.get('count'),
            'visibility': post.get('visibility'),
            'clap_count': post.get('clapCount'),
            'unique_slug': post.get('uniqueSlug'),
            'module_source_encoding': str(item.get('moduleSourceEncoding')),
            'reason': str(item.get('reason')),
            'full_item': item,  # Ensure this is acceptable in your Supabase table
            'article_markdown': None,  # Assuming this is not available
            'topic_tag': tag,
            'first_published_at': first_published_at,
            'reading_time': round(post.get('readingTime'),2),
        }

        # Optional: Validate the row before inserting
        if not row['title'] or not row['unique_slug']:
            print(f"Skipping item due to missing required fields: {row}")
            continue

        rows_to_insert.append(row)

    if not rows_to_insert:
        print("No rows to insert.")
        return

    try:
        # print('rows_to_insert:', json.dumps(rows_to_insert, indent=2))
        response = supabase.table("articles").upsert(rows_to_insert).execute()
        print(f"Inserted {len(rows_to_insert)} rows into Supabase.")
        return response
    except Exception as exception:
        print(f"Error inserting data into Supabase: {exception}")
        return exception
    
# def get_markdown_from_url(url: str, cookie: str) -> str:
#     time.sleep(2)
#     response = requests.get(url)
#     url = f'https://r.jina.ai/{medium_url}'
#     headers = {
#         'X-Set-Cookie': f'cookie={cookie}; domain=medium.com'
#         }
#     return response.text


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

for tag in tags:
    print(f"[LOG] Fetching data for tag: {tag}")
    # Loop through the pages
    from_page = 10
    to_page = 20
    limit = 10

    while to_page < 201:
        print(f"     [LOG] from page: {from_page}, to page: {to_page}, limit: {limit}")
        data = fetch_data_medium_api(to_page, from_page, limit, MEDIUM_COOKIE, tag)
        # print('daata:',data)
        if not data:
            print("[ERROR] No data found")
            break

        # Extract items from the fetched data
        items = data[0].get('data', {}).get('personalisedTagFeed', {}).get('items', [])
        
        if not items:
            print("[ERROR] No items found in data")
            break

        # Process the data (print or save)
        # print(json.dumps(items, indent=2))
        insert_items_metadata_supabase(items, tag)

        # Add a random wait time between 1 and 5 seconds
        wait_time = random.uniform(1, 5)
        print(f"[INFO] Waiting for {wait_time:.2f} seconds before the next request...")
        time.sleep(wait_time)

        # Update the paging parameters
        from_page += limit
        to_page += limit
