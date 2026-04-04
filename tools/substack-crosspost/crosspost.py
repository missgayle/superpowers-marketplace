#!/usr/bin/env python3
"""Substack to Social Media Cross-Poster.

Monitors a Substack RSS feed for new posts, generates hashtags using Claude's API,
and produces formatted cross-posts for Twitter/X, Facebook, and Instagram.
"""

import argparse
import json
import os
import re
import string
import sys
import time
from collections import Counter
from datetime import datetime

import feedparser
import requests


# --- Configuration ---

def load_config(path):
    """Load config from JSON file, with env var overrides."""
    if not os.path.exists(path):
        print(f"Error: Config file '{path}' not found.")
        print("Copy config.example.json to config.json and edit it.")
        sys.exit(1)

    with open(path) as f:
        config = json.load(f)

    # Environment variable overrides
    env_map = {
        "ANTHROPIC_API_KEY": "anthropic_api_key",
        "SUBSTACK_FEED_URL": "feed_url",
        "TWITTER_API_KEY": ("twitter", "api_key"),
        "TWITTER_API_SECRET": ("twitter", "api_secret"),
        "TWITTER_ACCESS_TOKEN": ("twitter", "access_token"),
        "TWITTER_ACCESS_TOKEN_SECRET": ("twitter", "access_token_secret"),
        "FACEBOOK_PAGE_ID": ("facebook", "page_id"),
        "FACEBOOK_ACCESS_TOKEN": ("facebook", "access_token"),
        "INSTAGRAM_ACCOUNT_ID": ("instagram", "business_account_id"),
        "INSTAGRAM_ACCESS_TOKEN": ("instagram", "access_token"),
    }
    for env_key, config_path in env_map.items():
        val = os.environ.get(env_key)
        if val:
            if isinstance(config_path, tuple):
                config[config_path[0]][config_path[1]] = val
            else:
                config[config_path] = val

    return config


# --- Processed Post Tracking ---

def load_processed(path):
    """Load set of already-processed post GUIDs."""
    if os.path.exists(path):
        with open(path) as f:
            return set(json.load(f))
    return set()


def save_processed(path, processed_set):
    """Save processed post GUIDs to disk."""
    with open(path, "w") as f:
        json.dump(sorted(processed_set), f, indent=2)


# --- RSS Feed ---

def fetch_new_posts(feed_url, processed):
    """Parse RSS feed and return entries not yet processed."""
    feed = feedparser.parse(feed_url)

    if feed.bozo and not feed.entries:
        print(f"Warning: Feed parsing error: {feed.bozo_exception}")
        return []

    new_posts = []
    for entry in feed.entries:
        post_id = entry.get("id") or entry.get("link")
        if post_id not in processed:
            new_posts.append(entry)

    return new_posts


# --- Content Extraction ---

def extract_image(entry):
    """Extract the featured/hero image URL from a Substack post."""
    # Check for enclosures with image type
    if hasattr(entry, "enclosures"):
        for enc in entry.enclosures:
            if enc.get("type", "").startswith("image/"):
                return enc["href"]

    # Parse content HTML for first relevant <img> tag
    content_html = ""
    if hasattr(entry, "content") and entry.content:
        content_html = entry.content[0].value
    elif hasattr(entry, "summary"):
        content_html = entry.summary

    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content_html)

    # Prefer Substack CDN images (hero/featured images)
    for img_url in imgs:
        if "substackcdn.com" in img_url or "substack-post-media" in img_url:
            return img_url

    # Fallback to first image
    return imgs[0] if imgs else None


def extract_text_content(entry):
    """Get clean text from HTML content for hashtag generation."""
    content_html = ""
    if hasattr(entry, "content") and entry.content:
        content_html = entry.content[0].value
    elif hasattr(entry, "summary"):
        content_html = entry.summary

    clean = re.sub(r"<[^>]+>", " ", content_html)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


# --- Hashtag Generation ---

STOP_WORDS = frozenset([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "this", "that", "these",
    "those", "you", "he", "she", "it", "we", "they", "me", "him", "her",
    "us", "them", "my", "your", "his", "its", "our", "their", "what",
    "which", "who", "whom", "when", "where", "how", "not", "no", "nor",
    "if", "then", "than", "too", "very", "just", "about", "also", "more",
    "from", "here", "there", "all", "any", "each", "so", "as", "up", "out",
    "into", "over", "after", "before", "between", "under", "again", "only",
    "own", "same", "other", "new", "one", "two", "some", "such", "like",
    "many", "much", "most", "well", "back", "even", "still", "way", "take",
    "come", "make", "know", "think", "see", "look", "want", "give", "use",
    "find", "tell", "ask", "work", "seem", "feel", "try", "leave", "call",
    "good", "first", "last", "long", "great", "little", "right", "old",
    "big", "high", "different", "small", "large", "next", "early", "young",
    "important", "few", "public", "bad", "real", "best", "better", "sure",
    "free", "said", "people", "really", "going", "thing", "things", "time",
    "year", "years", "world", "life", "day", "part", "while", "though",
    "through", "being", "because", "since", "during", "without", "however",
    "never", "always", "already", "every", "another", "around", "down",
    "away", "yet", "until", "often", "both", "those", "once", "done",
    "getting", "got", "went", "made", "say", "says",
])


def generate_hashtags_keyword(title, text_content, count=10, custom_tags=None):
    """Generate hashtags using keyword frequency analysis (fallback method)."""
    # Weight title words 3x more than body
    words = title.lower().split() * 3 + text_content.lower().split()

    cleaned = []
    for w in words:
        w = w.strip(string.punctuation)
        if len(w) > 3 and w not in STOP_WORDS and not w.isdigit():
            cleaned.append(w)

    freq = Counter(cleaned)
    top_words = [word for word, _ in freq.most_common(count)]
    hashtags = [f"#{w.capitalize()}" for w in top_words]

    if custom_tags:
        hashtags = list(custom_tags) + hashtags

    return hashtags[: count + len(custom_tags or [])]


def generate_hashtags_claude(title, text_content, api_key, count=10, custom_tags=None):
    """Generate hashtags using Claude's API for contextual, trending-style tags."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Warning: 'anthropic' package not installed. Falling back to keyword method.")
        return generate_hashtags_keyword(title, text_content, count, custom_tags)

    client = Anthropic(api_key=api_key)

    # Send first ~2000 chars of content for efficiency
    excerpt = text_content[:2000]

    prompt = f"""Analyze this blog post and generate exactly {count} relevant hashtags for social media cross-posting.

Title: {title}

Content excerpt:
{excerpt}

Requirements:
- Return ONLY the hashtags, one per line, each starting with #
- Make them relevant to the post's topics, themes, and keywords
- Mix broad/trending tags with specific/niche tags for maximum reach
- Use CamelCase for multi-word hashtags (e.g., #SocialMedia not #socialmedia)
- Do NOT include generic tags like #Blog or #Article
- Focus on the subject matter, not the medium"""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()

        # Parse hashtags from response
        hashtags = [
            line.strip()
            for line in raw.split("\n")
            if line.strip().startswith("#")
        ]

        if not hashtags:
            print("Warning: Claude returned no hashtags. Falling back to keyword method.")
            return generate_hashtags_keyword(title, text_content, count, custom_tags)

        if custom_tags:
            hashtags = list(custom_tags) + hashtags

        return hashtags[: count + len(custom_tags or [])]

    except Exception as e:
        print(f"Warning: Claude API error: {e}. Falling back to keyword method.")
        return generate_hashtags_keyword(title, text_content, count, custom_tags)


def generate_hashtags(title, text_content, config):
    """Generate hashtags using the configured method."""
    count = config.get("hashtag_count", 10)
    custom_tags = config.get("custom_hashtags")
    api_key = config.get("anthropic_api_key", "")

    if api_key:
        return generate_hashtags_claude(title, text_content, api_key, count, custom_tags)
    else:
        print("Note: No Anthropic API key configured. Using keyword-based hashtags.")
        return generate_hashtags_keyword(title, text_content, count, custom_tags)


# --- Platform Formatting ---

TWITTER_URL_LENGTH = 23  # Twitter counts all URLs as 23 chars


def format_twitter(title, link, hashtags, max_len=280):
    """Format for Twitter/X: title + link + hashtags, within 280 chars."""
    tag_str = " ".join(hashtags)

    # Budget: max_len - URL (23) - newlines (4) - tag_str length
    available = max_len - TWITTER_URL_LENGTH - len(tag_str) - 4
    if len(title) > available:
        truncated_title = title[: available - 3] + "..."
    else:
        truncated_title = title

    return f"{truncated_title}\n\n{link}\n\n{tag_str}"


def format_facebook(title, description, link, hashtags):
    """Format for Facebook: title + description excerpt + link + hashtags."""
    tag_str = " ".join(hashtags)
    desc_excerpt = description[:300] + ("..." if len(description) > 300 else "")

    return f"{title}\n\n{desc_excerpt}\n\nRead more: {link}\n\n{tag_str}"


def format_instagram(title, description, hashtags):
    """Format for Instagram: caption style with hashtags at end."""
    tag_str = " ".join(hashtags)
    desc_excerpt = description[:500] + ("..." if len(description) > 500 else "")

    return f"{title}\n\n{desc_excerpt}\n\nLink in bio\n\n{tag_str}"


# --- Social Media Posting ---

def post_to_twitter(text, image_url, config):
    """Post to Twitter/X using v2 API via tweepy."""
    try:
        import tweepy
    except ImportError:
        print("Error: 'tweepy' package required for Twitter posting. pip install tweepy")
        return

    client = tweepy.Client(
        consumer_key=config["api_key"],
        consumer_secret=config["api_secret"],
        access_token=config["access_token"],
        access_token_secret=config["access_token_secret"],
    )

    media_id = None
    if image_url:
        auth = tweepy.OAuth1UserHandler(
            config["api_key"],
            config["api_secret"],
            config["access_token"],
            config["access_token_secret"],
        )
        api_v1 = tweepy.API(auth)

        resp = requests.get(image_url, timeout=30)
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(resp.content)
            tmp_path = f.name

        media = api_v1.media_upload(tmp_path)
        media_id = media.media_id
        os.unlink(tmp_path)

    kwargs = {"text": text}
    if media_id:
        kwargs["media_ids"] = [media_id]
    client.create_tweet(**kwargs)
    print("  -> Posted to Twitter/X")


def post_to_facebook(text, image_url, config):
    """Post to Facebook Page via Graph API."""
    page_id = config["page_id"]
    access_token = config["access_token"]

    if image_url:
        url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
        data = {"url": image_url, "caption": text, "access_token": access_token}
    else:
        url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
        data = {"message": text, "access_token": access_token}

    resp = requests.post(url, data=data, timeout=30)
    if resp.status_code == 200:
        print("  -> Posted to Facebook")
    else:
        print(f"  -> Facebook error: {resp.status_code} {resp.text}")


def post_to_instagram(text, image_url, config):
    """Post to Instagram via Graph API (business accounts only)."""
    if not image_url:
        print("  -> Instagram requires an image. Skipping.")
        return

    account_id = config["business_account_id"]
    access_token = config["access_token"]
    base = f"https://graph.facebook.com/v19.0/{account_id}"

    # Step 1: Create media container
    resp = requests.post(
        f"{base}/media",
        data={"image_url": image_url, "caption": text, "access_token": access_token},
        timeout=30,
    ).json()

    if "id" not in resp:
        print(f"  -> Instagram container error: {resp}")
        return

    # Step 2: Publish
    pub_resp = requests.post(
        f"{base}/media_publish",
        data={"creation_id": resp["id"], "access_token": access_token},
        timeout=30,
    ).json()

    if "id" in pub_resp:
        print("  -> Posted to Instagram")
    else:
        print(f"  -> Instagram publish error: {pub_resp}")


# --- Output ---

def output_terminal(title, image_url, twitter_text, facebook_text, instagram_text, hashtags):
    """Print formatted cross-posts to terminal."""
    print(f"\n{'=' * 60}")
    print(f"NEW POST: {title}")
    print(f"IMAGE: {image_url or 'No image found'}")
    print(f"HASHTAGS: {' '.join(hashtags)}")
    print(f"\n--- Twitter/X ---")
    print(twitter_text)
    print(f"[{len(twitter_text)} chars, URL counts as {TWITTER_URL_LENGTH}]")
    print(f"\n--- Facebook ---")
    print(facebook_text)
    print(f"\n--- Instagram ---")
    print(instagram_text)
    print(f"{'=' * 60}\n")


def output_json(title, link, image_url, twitter_text, facebook_text, instagram_text, hashtags):
    """Output structured JSON for Zapier/webhook integration."""
    data = {
        "title": title,
        "link": link,
        "image_url": image_url,
        "hashtags": hashtags,
        "twitter_text": twitter_text,
        "facebook_text": facebook_text,
        "instagram_text": instagram_text,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    print(json.dumps(data, indent=2))


# --- Main ---

def process_post(entry, config, output_format="terminal"):
    """Process a single RSS entry into cross-posts."""
    title = entry.title
    link = entry.link
    description = entry.get("summary", "")
    image_url = extract_image(entry)
    text_content = extract_text_content(entry)

    print(f"Processing: {title}")

    # Generate hashtags
    hashtags = generate_hashtags(title, text_content, config)

    # Format for each platform
    twitter_text = format_twitter(title, link, hashtags)
    facebook_text = format_facebook(title, description, link, hashtags)
    instagram_text = format_instagram(title, description, hashtags)

    # Output
    if config.get("dry_run", True):
        if output_format == "json":
            output_json(title, link, image_url, twitter_text, facebook_text, instagram_text, hashtags)
        else:
            output_terminal(title, image_url, twitter_text, facebook_text, instagram_text, hashtags)
    else:
        output_terminal(title, image_url, twitter_text, facebook_text, instagram_text, hashtags)

        if config.get("twitter", {}).get("enabled"):
            post_to_twitter(twitter_text, image_url, config["twitter"])
        if config.get("facebook", {}).get("enabled"):
            post_to_facebook(facebook_text, image_url, config["facebook"])
        if config.get("instagram", {}).get("enabled"):
            post_to_instagram(instagram_text, image_url, config["instagram"])

    return title, link


def main():
    parser = argparse.ArgumentParser(
        description="Substack to Social Media Cross-Poster",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --once --dry-run          Check feed once, print formatted posts
  %(prog)s --once --format json      Output as JSON (for Zapier/webhooks)
  %(prog)s --once                    Check feed once, post if APIs configured
  %(prog)s                           Poll every 15 minutes (default)
""",
    )
    parser.add_argument("--config", default="config.json", help="Path to config file (default: config.json)")
    parser.add_argument("--once", action="store_true", help="Run once then exit (no polling)")
    parser.add_argument("--dry-run", action="store_true", help="Print posts without publishing")
    parser.add_argument("--format", choices=["terminal", "json"], default="terminal",
                        help="Output format (default: terminal)")
    parser.add_argument("--all", action="store_true",
                        help="Process all posts, not just new ones (ignores processed.json)")
    args = parser.parse_args()

    # Resolve config path relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config if os.path.isabs(args.config) else os.path.join(script_dir, args.config)
    config = load_config(config_path)

    if args.dry_run:
        config["dry_run"] = True

    processed_file = config.get("processed_file", "processed.json")
    if not os.path.isabs(processed_file):
        processed_file = os.path.join(script_dir, processed_file)

    poll_interval = config.get("poll_interval_minutes", 15)

    while True:
        if args.all:
            processed = set()
        else:
            processed = load_processed(processed_file)

        new_posts = fetch_new_posts(config["feed_url"], processed)

        if not new_posts:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No new posts found.")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(new_posts)} new post(s).")

        for entry in new_posts:
            title, link = process_post(entry, config, args.format)

            # Track as processed
            post_id = entry.get("id") or link
            processed.add(post_id)
            save_processed(processed_file, processed)

        if args.once:
            break

        print(f"Sleeping {poll_interval} minutes until next check...")
        time.sleep(poll_interval * 60)


if __name__ == "__main__":
    main()
