"""
TickZero CLI Launcher.

Uses Typer to manage the application lifecycle.
Commands:
- record: Orchestrates OBS recording based on CS2 GSI events.
- process: Generates highlights using AI Director and Video Editor.
"""
import typer
import sys
import time
import logging
import threading
import signal
from pathlib import Path
from typing import Optional

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Launcher")

# Imports
from tickzero.core.gsi_server import GSIServer
from tickzero.obs_controller import OBSClient
from tickzero.ai_director import AIDirector
from tickzero.video_editor import VideoEditor
# We reuse MatchDatabase for retrieving last match info
from tickzero.web.match_database import MatchDatabase

app = typer.Typer(help="TickZero - CS2 Capture-to-Content Pipeline")

@app.command()
def record(
    gsi_port: int = 3000,
    obs_host: str = "localhost", 
    obs_port: int = 4455,
    obs_auth: str = ""
):
    """
    Start the Recording Session.
    
    1. Connects to OBS.
    2. Starts GSI Server.
    3. Waits for CS2 match to go LIVE -> Starts Recording.
    4. Waits for CS2 match END -> Stops Recording.
    """
    logger.info("Initializing TickZero Recording Session...")
    
    # Flags to control flow
    recording_active = threading.Event()
    stop_event = threading.Event()
    
    # Initialize OBS Client
    obs_client = OBSClient(host=obs_host, port=obs_port, password=obs_auth)
    
    def on_match_start():
        """Callback when match goes live."""
        logger.info("🎮 Signal: Match Started (LIVE)")
        if not recording_active.is_set():
            if obs_client.start_recording():
                recording_active.set()
                logger.info("🔴 Recording STARTED")
    
    def on_match_end():
        """Callback when match ends."""
        logger.info("🏁 Signal: Match Ended")
        if recording_active.is_set():
            path = obs_client.stop_recording()
            recording_active.clear()
            logger.info(f"💾 Recording STOPPED. Saved to: {path}")
            # We don't exit automatically in case user plays another match (continuous)
            # But the prompt implies "cycle", let's assume continuous for now or 
            # if the user wants single match, they can Ctrl+C.
    
    # Initialize GSI Server
    # Note: GSIServer expects an object with calculate_video_timestamp (or updated get_current_timestamp compat)
    gsi_server = GSIServer(
        obs_manager=obs_client,
        port=gsi_port,
        on_match_start=on_match_start,
        on_match_end=on_match_end
    )
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        logger.info("\n🛑 Interrupted by user. Shutting down...")
        stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Connect OBS
        with obs_client:
            # Start GSI
            gsi_server.start()
            
            logger.info("👀 Waiting for CS2 events... (Press Ctrl+C to stop)")
            
            # Helper: Check periodically if OBS is still connected
            while not stop_event.is_set():
                time.sleep(1)
                
    except Exception as e:
        logger.error(f"Critical Error: {e}")
        
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        if recording_active.is_set():
            logger.warning("Force stopping recording...")
            obs_client.stop_recording()
            
        gsi_server.stop()
        logger.info("Bye!")


@app.command()
def process(
    last: bool = typer.Option(False, "--last", help="Process the last recorded match automatically"),
    video: Optional[str] = typer.Option(None, help="Path to video file"),
    log: Optional[str] = typer.Option(None, help="Path to match_log.json"),
    output: str = "highlights",
    gpu: bool = True
):
    """
    Process highlights from a recording.
    """
    video_path = video
    log_path = log
    
    if last:
        # Fetch last match from DB or logs
        db = MatchDatabase()
        last_match = db.get_last_match() # Assuming this method exists or we fetch list
        if not last_match and not (video_path and log_path):
            # Fallback to checking file system if DB empty
            # For this implementation, let's rely on DB or args
             # Try to find latest match from db.get_all_matches
            matches = db.get_all_matches(limit=1)
            if matches:
                last_match = matches[0]
            
        if last_match:
            video_path = last_match.get('video_path')
            log_path = last_match.get('log_path')
            logger.info(f"Using last match: {video_path}")
        else:
            logger.error("No recent match found. Please specify --video and --log.")
            raise typer.Exit(code=1)
            
    if not video_path or not log_path:
        logger.error("Missing video or log path.")
        raise typer.Exit(code=1)
        
    if not Path(video_path).exists() or not Path(log_path).exists():
        logger.error("Video or Log file does not exist.")
        raise typer.Exit(code=1)
        
    # 1. AI Analysis
    logger.info("🤖 Starting AI Director analysis...")
    ai = AIDirector()
    highlights = ai.analyze_match_log(log_path)
    
    if not highlights:
        logger.warning("No highlights found.")
        return
        
    # 2. Video Rendering
    logger.info("🎬 Starting Video Editor rendering...")
    editor = VideoEditor(output_dir=output, use_gpu=gpu)
    clips = editor.create_highlights_batch(highlights, video_path)
    
    logger.info(f"✨ Done! Created {len(clips)} clips in '{output}/'")

if __name__ == "__main__":
    app()
