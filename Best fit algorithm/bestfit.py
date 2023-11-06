# List of available OSINT tools or APIs for each platform
osint_tools = {
    "Instagram": [
        {"name": "Tool A", "capability": ["profile data", "media scraping", "follower analysis"]},
        {"name": "Tool B", "capability": ["geolocation data", "comment analysis", "sentiment analysis"]},
        {"name": "Tool C", "capability": ["message tracking", "hashtag tracking", "image recognition"]},
        {"name": "Tool D", "capability": ["mentions analysis", "captions analysis", "geotagged media"]},
        # Add more Instagram tools with their capabilities
    ],
    "Twitter": [
        {"name": "Tool E", "capability": ["tweets and retweets", "user mentions", "follower analysis"]},
        {"name": "Tool F", "capability": ["hashtags analysis", "geolocation data", "sentiment analysis"]},
        {"name": "Tool G", "capability": ["URL tracking", "trending topics analysis", "real-time feeds"]},
        {"name": "Tool H", "capability": ["advanced keyword search", "timeline analysis", "influencer tracking"]},
        # Add more Twitter tools with their capabilities
    ],
    "Telegram": [
        {"name": "Tool I", "capability": ["chat extraction", "group analysis", "media extraction"]},
        {"name": "Tool J", "capability": ["user activities", "message tracking", "file analysis"]},
        {"name": "Tool K", "capability": ["bot tracking", "channel analysis", "metadata extraction"]},
        {"name": "Tool L", "capability": ["message history", "chat sentiment analysis", "voice recognition"]},
        # Add more Telegram tools with their capabilities
    ],
    "Dark Web": [
        {"name": "Tool M", "capability": ["dark web monitoring", "anonymous forums tracking"]},
        {"name": "Tool N", "capability": ["dark web marketplace data", "crypto analysis"]},
        {"name": "Tool O", "capability": ["threat intelligence", "TOR network analysis", "dark web social media tracking"]},
        {"name": "Tool P", "capability": ["illegal content tracking", "suspicious transactions", "deep web search"]},
        # Add more Dark Web tools with their capabilities
    ],
}

# Search criteria or requirements for OSINT
search_criteria = [
    "follower analysis", "tweets and retweets"
]

# Define the target social network (set to None if not specified)
target_social_network = None  # Change this to "Instagram", "Twitter", "Telegram", or "Dark Web" as needed

# Initialize variables to track the best-fit tool
best_tools = []
best_fit_score = 0

# Iterate through tools from all social networks if the target is not specified
if target_social_network is not None:
    tools = osint_tools.get(target_social_network, [])
else:
    tools = [tool for tools in osint_tools.values() for tool in tools]

for tool in tools:
    tool_name = tool["name"]
    tool_capabilities = tool["capability"]

    # Calculate the tool's fit score by counting the matching criteria
    fit_score = sum(1 for criteria in search_criteria if criteria in tool_capabilities)

    # Update the best-fit tool if the current tool has a higher fit score
    if fit_score > best_fit_score:
        best_tools = [tool_name]
        best_fit_score = fit_score
    elif fit_score == best_fit_score:
        best_tools.append(tool_name)

# Check if a best-fit tool was found
if best_tools is not None:
    print(f"Best-fit OSINT tools for the criteria: {best_tools}")
else:
    print("No suitable OSINT tool found for the given criteria.")