from textblob import TextBlob
import re
from googleapiclient.discovery import build
import emoji

class YouTubeAnalyzer:
    """Advanced YouTube sentiment analysis with emoji support and context awareness"""

    def __init__(self, api_key):
        """Initialize with YouTube API key"""
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.reset()
        self._init_sentiment_patterns()

    def _init_sentiment_patterns(self):
        """Initialize advanced sentiment detection patterns"""
               # Positive emojis (comprehensive list)
        self.positive_emojis = {
            '😊', '😀', '😃', '😄', '😁', '🙂', '😍', '🥰', '😘', '😗', '😙', '😚',
            '❤️', '💕', '💖', '💗', '💙', '💚', '💛', '🧡', '💜', '🖤', '🤍', '🤎',
            '🤗', '🥳', '🎉', '🎊', '🎈', '🎆', '🎇', '✨', '⭐', '🌟', '💫', '⚡',
            '👍', '👏', '🙌', '💪', '🤘', '🤟', '👌', '🤌', '🫶', '❣️', '💝', '💘',
            '🔥', '💯', '🏆', '🥇', '🎯', '✅', '☑️', '✔️', '🆒', '🆗', '🤩', '😎',
            '😇', '🥹', '🤝', '🌹', '🌺', '🌸', '🌼', '🌻', '🌷', '💐', '🎁', '🍰'
        }
        
        # Negative emojis (comprehensive list)
        self.negative_emojis = {
            '😢', '😭', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
            '😤', '😠', '😡', '🤬', '😱', '😨', '😰', '😥', '😓', '😪', '😴', '🤐',
            '💔', '💀', '☠️', '👎', '👊', '🖕', '😒', '🙄', '😑', '😐', '😬', '😶',
            '🤮', '🤢', '😷', '🤕', '🤒', '😵', '🥴', '😮‍💨', '😤', '💩', '🚫', '❌'
        }

        # Strong positive indicators
        self.positive_patterns = [
            r'\b(love|amazing|awesome|excellent|fantastic|wonderful|brilliant|perfect|great|beautiful|best)\b',
            r'\b(good|nice|cool|enjoy|enjoyed|enjoying|happy|glad|appreciate|thanks|thank you)\b',
            r'\b(impressive|outstanding|superb|magnificent|incredible|extraordinary|phenomenal)\b',
            r'(lol|lmao|haha|hehe|😂)+',
            r'\b(yes|yeah|yay|yup|absolutely|definitely|certainly)\b'
        ]
        
        # Strong negative indicators
        self.negative_patterns = [
            r'\b(hate|terrible|awful|horrible|worst|disgusting|pathetic|trash|garbage|stupid)\b',
            r'\b(bad|poor|disappointing|disappointed|sucks|boring|annoying|irritating)\b',
            r'\b(waste|useless|pointless|ridiculous|absurd|nonsense|cringe|cringy)\b',
            r'\b(no|nope|never|not good|not great|don\'t like|dislike)\b',
            r'\b(wtf|omg no|are you serious|seriously\?|this is bad)\b'
        ]
        
 
    # ================= UTILITIES =================
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL or ID"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def analyze_sentiment(self, text):
        """Advanced sentiment analysis with emoji, patterns, and context"""
        try:
            text_lower = text.lower()
            
            # 1. Emoji Analysis
            emoji_score = self._analyze_emojis(text)
            
            # 2. Pattern Matching (strong indicators)
            pattern_score = self._analyze_patterns(text_lower)
            
            # 3. TextBlob Polarity
            text_polarity = TextBlob(text).sentiment.polarity
            
            # 4. Intensity Modifiers (!!!, ???, CAPS)
            intensity = self._analyze_intensity(text)
            
            # 5. Context Analysis
            has_question = '?' in text
            text_length = len(text.strip())
            
            # Weighted combination based on message characteristics
            if text_length < 10:
                # Very short messages - trust emojis and patterns more
                final_score = emoji_score * 0.6 + pattern_score * 0.3 + text_polarity * 0.1
            elif text_length < 30:
                # Short messages - balanced approach
                final_score = emoji_score * 0.4 + pattern_score * 0.3 + text_polarity * 0.3
            else:
                # Longer messages - trust text analysis more
                final_score = emoji_score * 0.25 + pattern_score * 0.25 + text_polarity * 0.5
            
            # Apply intensity modifier
            final_score *= (1 + intensity * 0.3)
            
            # Questions are often neutral unless strongly positive/negative
            if has_question and abs(final_score) < 0.3:
                return 'Neutral'
            
            # Enhanced thresholds
            if final_score > 0.12:
                return 'Positive'
            elif final_score < -0.12:
                return 'Negative'
            return 'Neutral'
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 'Neutral'
    
    def _analyze_emojis(self, text):
        """Analyze emoji sentiment with weighted scoring"""
        emojis_in_text = [c for c in text if c in emoji.EMOJI_DATA]
        
        if not emojis_in_text:
            return 0
        
        pos_count = sum(1 for e in emojis_in_text if e in self.positive_emojis)
        neg_count = sum(1 for e in emojis_in_text if e in self.negative_emojis)
        total = len(emojis_in_text)
        
        if total == 0:
            return 0
        
        # Calculate score with emphasis on ratio
        score = (pos_count - neg_count) / total
        
        # Boost score for multiple same-sentiment emojis
        if pos_count > 2 or neg_count > 2:
            score *= 1.2
        
        return max(-1, min(1, score))
    
    def _analyze_patterns(self, text_lower):
        """Pattern-based sentiment detection"""
        pos_matches = sum(1 for pattern in self.positive_patterns 
                         if re.search(pattern, text_lower, re.IGNORECASE))
        neg_matches = sum(1 for pattern in self.negative_patterns 
                         if re.search(pattern, text_lower, re.IGNORECASE))
        
        # Strong indicators
        if pos_matches > neg_matches:
            return min(0.8, pos_matches * 0.3)
        elif neg_matches > pos_matches:
            return max(-0.8, -neg_matches * 0.3)
        
        return 0
    
    def _analyze_intensity(self, text):
        """Detect intensity modifiers (caps, punctuation)"""
        intensity = 0
        
        # Multiple exclamation marks
        if '!!' in text:
            intensity += 0.3
        
        # All caps words (minimum 3 chars)
        caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
        if caps_words:
            intensity += 0.2 * min(len(caps_words), 3)
        
        # Multiple question marks (confusion/frustration)
        if '??' in text:
            intensity += 0.1
        
        return min(intensity, 1.0)

    # ================= LIVE CHECK =================
    def get_live_chat_id(self, video_id):
        """Return active live chat ID if video is LIVE"""
        try:
            response = self.youtube.videos().list(
                part="liveStreamingDetails",
                id=video_id
            ).execute()

            if not response.get('items'):
                return None

            live_details = response['items'][0].get('liveStreamingDetails', {})
            return live_details.get('activeLiveChatId')
        except Exception as e:
            print(f"Live chat ID error: {e}")
            return None

    # ================= COMMENT FETCH =================
    def fetch_live_comments(self, live_chat_id):
        """Fetch live chat messages"""
        try:
            response = self.youtube.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="snippet,authorDetails",
                maxResults=100
            ).execute()

            comments = []
            for item in response['items']:
                text = item['snippet'].get('displayMessage')
                if not text:
                    continue

                comment = {
                    'author': item['authorDetails']['displayName'],
                    'text': text,
                    'sentiment': self.analyze_sentiment(text),
                    'timestamp': item['snippet']['publishedAt']
                }
                comments.append(comment)

            return comments
        except Exception as e:
            print(f"Live comment error: {e}")
            return []

    # ================= ANALYSIS START =================
    def start_analysis(self, video_url):
        """Start analysis ONLY if stream is LIVE"""
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return {
                'status': 'error',
                'message': 'Invalid YouTube URL',
                'is_live': False
            }

        live_chat_id = self.get_live_chat_id(video_id)

        # 🚫 BLOCK NON-LIVE VIDEOS
        if not live_chat_id:
            return {
                'status': 'error',
                'message': 'The link is not live',
                'is_live': False
            }

        # ✅ LIVE STREAM CONFIRMED
        self.comments_data = {
            'video_id': video_id,
            'live_chat_id': live_chat_id,
            'is_live': True,
            'comments': [],
            'stats': {
                'total': 0,
                'positive': 0,
                'neutral': 0,
                'negative': 0
            }
        }

        # Initial fetch
        for comment in self.fetch_live_comments(live_chat_id):
            self._add_comment(comment)

        return {
            'status': 'success',
            'message': 'Live stream detected. Analysis started.',
            'is_live': True
        }

    # ================= UPDATE LOOP =================
    def update_comments(self):
        """Fetch new live comments"""
        if not self.comments_data.get('is_live'):
            return self.comments_data

        new_comments = self.fetch_live_comments(self.comments_data['live_chat_id'])
        existing = {c['text'] for c in self.comments_data['comments']}

        for comment in new_comments:
            if comment['text'] not in existing:
                self._add_comment(comment)

        return self.comments_data

    # ================= INTERNAL =================
    def _add_comment(self, comment):
        self.comments_data['comments'].append(comment)
        self.comments_data['stats']['total'] += 1
        self.comments_data['stats'][comment['sentiment'].lower()] += 1

    # ================= PUBLIC =================
    def get_data(self):
        return {
            'comments': self.comments_data['comments'],
            'stats': self.comments_data['stats']
        }

    def reset(self):
        self.comments_data = {
            'comments': [],
            'stats': {'total': 0, 'positive': 0, 'neutral': 0, 'negative': 0}
        }