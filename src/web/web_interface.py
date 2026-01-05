"""
Web Interface: Flask application for browsing match history and generating highlights.
Provides web UI for selecting past matches and triggering highlight generation.
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
from src.web.match_database import MatchDatabase
from pathlib import Path
import logging
import subprocess
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
db = MatchDatabase()


@app.route('/')
def index():
    """Main dashboard with recent matches and statistics."""
    recent_matches = db.get_all_matches(limit=10)
    stats = db.get_statistics()
    return render_template('index.html', matches=recent_matches, stats=stats)


@app.route('/matches')
def match_list():
    """Full match history page."""
    all_matches = db.get_all_matches(limit=100)
    return render_template('match_list.html', matches=all_matches)


@app.route('/match/<int:match_id>')
def match_detail(match_id):
    """Detailed view of a specific match."""
    match = db.get_match(match_id)
    if not match:
        return "Match not found", 404
    
    events = db.get_match_events(match_id)
    
    # Filter to show only kill events for timeline
    kill_events = [e for e in events if e.get('type') == 'kill']
    
    return render_template('match_detail.html', match=match, events=kill_events)


@app.route('/api/generate/<int:match_id>', methods=['POST'])
def generate_highlights(match_id):
    """API endpoint to trigger highlight generation for a match."""
    try:
        match = db.get_match(match_id)
        if not match:
            return jsonify({"status": "error", "message": "Match not found"}), 404
        
        # Get parameters from request
        min_priority = request.json.get('min_priority', 6) if request.json else 6
        
        # Start highlight generation in background thread
        thread = threading.Thread(
            target=_process_match_highlights,
            args=(match_id, match['video_path'], match['log_path'], min_priority)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "success", 
            "message": "Highlight generation started",
            "match_id": match_id
        })
        
    except Exception as e:
        logger.error(f"Error generating highlights: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def _process_match_highlights(match_id, video_path, log_path, min_priority):
    """
    Background task to process highlights for a match.
    
    Args:
        match_id: Match database ID
        video_path: Path to video file
        log_path: Path to match log
        min_priority: Minimum priority threshold
    """
    try:
        logger.info(f"Starting highlight processing for match #{match_id}")
        
        # Call main.py process command
        cmd = [
            'python', 'main.py', 'process',
            video_path,
            str(min_priority)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            # Mark match as processed
            db.update_match(match_id, processed=True)
            logger.info(f"✓ Successfully processed match #{match_id}")
        else:
            logger.error(f"✗ Processing failed for match #{match_id}: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error in background processing: {e}")


@app.route('/api/delete/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    """API endpoint to delete a match."""
    try:
        db.delete_match(match_id)
        return jsonify({"status": "success", "message": f"Match #{match_id} deleted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """API endpoint for statistics."""
    stats = db.get_statistics()
    return jsonify(stats)


def run_web_interface(port=5000, debug=False):
    """
    Start the Flask web server.
    
    Args:
        port: Port to run on (default: 5000)
        debug: Enable debug mode
    """
    logger.info(f"Starting web interface on http://localhost:{port}")
    app.run(debug=debug, port=port, host='localhost')


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_web_interface(port=port, debug=True)
