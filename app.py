from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import YouTubeAnalyzer

app = Flask(__name__)
CORS(app)

# YouTube API configuration
YOUTUBE_API_KEY = 'AIzaSyC_gguzxPUari0_sN5XKG3Xe5tw_MmHKYw'  

# Initialize the analyzer
analyzer = YouTubeAnalyzer(YOUTUBE_API_KEY)

@app.route('/start', methods=['POST'])
def start_analysis():
    """Start analyzing a YouTube video"""
    data = request.json
    video_url = data.get('video_url', '')
    
    if not video_url:
        return jsonify({'status': 'error', 'message': 'No video URL provided'}), 400
    
    try:
        result = analyzer.start_analysis(video_url)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/comments', methods=['GET'])
def get_comments():
    """Get current comments and stats"""
    analyzer.update_comments()
    data = analyzer.get_data()
    return jsonify(data)

@app.route('/reset', methods=['POST'])
def reset():
    """Reset all data"""
    result = analyzer.reset()
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    print("YouTube Live Comments Sentiment Analyzer Backend")
    print("=" * 50)
    print("Starting in 2 minutes...")
    app.run(debug=True, port=5000)