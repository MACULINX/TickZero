"""
Main orchestration script for CS2 Capture-to-Content Pipeline.
Coordinates OBS recording, GSI event logging, and post-processing workflow.
"""
import sys
import time
import logging
import threading
from pathlib import Path

from src.core.obs_manager import OBSManager
from src.core.gsi_server import GSIServer
from src.core.ai_director import AIDirector
from src.core.video_editor import VideoEditor
from src.web.match_database import MatchDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CS2HighlightPipeline:
    """Main pipeline coordinator."""
    
    def __init__(self, config=None):
        """
        Initialize the pipeline with configuration.
        
        Args:
            config: Configuration dict (optional)
        """
        self.config = config or {}
        
        # Initialize database
        self.db = MatchDatabase(self.config.get('db_path', 'matches.db'))
        
        # Initialize components
        self.obs = OBSManager(
            host=self.config.get('obs_host', 'localhost'),
            port=self.config.get('obs_port', 4455),
            password=self.config.get('obs_password', '')
        )
        
        # Setup match callbacks
        match_start_callback = self._on_match_start if self.config.get('auto_recording', True) else None
        match_end_callback = self._on_match_end if self.config.get('continuous_mode') else None
        
        self.gsi = GSIServer(
            obs_manager=self.obs,
            port=self.config.get('gsi_port', 3000),
            log_file=self.config.get('log_file', 'match_log.json'),
            on_match_start=match_start_callback,
            on_match_end=match_end_callback
        )
        
        self.ai_director = None  # Initialize when needed (requires API key)
        self.video_editor = None  # Initialize during post-processing
        self.processing_thread = None  # Background processing thread
    
    def start_live_logging(self):
        """
        PHASE 1: Start live logging session.
        
        This connects to OBS, starts recording, and begins listening for CS2 events.
        Run this BEFORE starting your CS2 match.
        """
        logger.info("=" * 60)
        logger.info("CS2 CAPTURE-TO-CONTENT PIPELINE - LIVE LOGGING PHASE")
        logger.info("=" * 60)
        
        # Step 1: Connect to OBS
        logger.info("\n[1/3] Connecting to OBS WebSocket...")
        if not self.obs.connect():
            logger.error("Failed to connect to OBS. Make sure OBS is running and WebSocket is enabled.")
            return False
        
        # Step 2: Start recording (or wait for match to start)
        logger.info("\n[2/3] Preparing recording...")
        if self.config.get('auto_recording', True):
            logger.info("✓ Auto-recording enabled")
            logger.info("  Recording will start automatically when match begins")
        else:
            # Manual mode - start recording immediately
            logger.info("✓ Starting recording immediately (auto_recording disabled)")
            start_time = self.obs.start_recording()
            if not start_time:
                logger.error("Failed to start recording.")
                return False
        
        # Step 3: Start GSI server
        logger.info("\n[3/3] Starting GSI server...")
        self.gsi.start()
        
        logger.info("\n" + "=" * 60)
        logger.info("\n✓ LIVE LOGGING ACTIVE")
        logger.info("=" * 60)
        
        if self.config.get('auto_recording', True):
            logger.info("\n⏳ WAITING FOR MATCH TO START...")
            logger.info("Launch CS2 and join a match.")
            logger.info("Recording will begin automatically when the first round goes live.")
        else:
            logger.info("\n✓ RECORDING IN PROGRESS")
            logger.info("You can now launch CS2 and play your match.")
        
        logger.info("Game events will be automatically logged with video timestamps.")
        
        if self.config.get('continuous_mode'):
            logger.info("\n🔄 CONTINUOUS MODE ENABLED")
            logger.info("Highlights will be auto-processed after each match.")
            logger.info("Recording will continue for multiple matches.")
            logger.info("\nPress Ctrl+C when done playing to stop.")
        else:
            logger.info("\nPress Ctrl+C when match is finished to stop logging.")
        logger.info("=" * 60 + "\n")
        
        return True
    
    def _on_match_start(self):
        """
        Callback when match starts (first round goes live).
        Triggers automatic recording start.
        """
        logger.info("\n" + "=" * 60)
        logger.info("🎮 MATCH STARTED - BEGINNING RECORDING")
        logger.info("=" * 60)
        
        start_time = self.obs.start_recording()
        if start_time:
            logger.info("✓ Recording started successfully")
            logger.info("✓ All game events will be captured\n")
        else:
            logger.error("✗ Failed to start recording")
    
    def _on_match_end(self):
        """
        Callback when match ends in continuous mode.
        Stops current recording, triggers processing, and prepares for next match.
        """
        logger.info("\n" + "=" * 60)
        logger.info("🏁 MATCH ENDED")
        logger.info("=" * 60)
        
        # Get current recording path and stop recording
        recording_path = self.obs.get_last_recording_path()
        
        if self.obs.is_recording:
            logger.info("Stopping recording...")
            self.obs.stop_recording()
            time.sleep(1)  # Brief pause for file to be written
        
        if not recording_path:
            logger.warning("Cannot auto-process: recording path unknown")
            if self.config.get('continuous_mode'):
                logger.info("\n⏳ Ready for next match...\n")
            return
        
        # Save match to database
        match_id = self.db.save_match(
            video_path=recording_path,
            log_path=self.gsi.log_file
        )
        logger.info(f"✓ Match #{match_id} saved to database")
        
        # Start processing in background thread if auto-processing is enabled
        if self.config.get('auto_process', False):
            logger.info("Starting background processing...")
            self.processing_thread = threading.Thread(
                target=self._background_process,
                args=(recording_path,),
                daemon=True
            )
            self.processing_thread.start()
        
        # In continuous mode, wait for next match
        if self.config.get('continuous_mode'):
            logger.info("\n⏳ Ready for next match...")
            logger.info("Recording will start automatically when the next match begins.\n")
    
    def _background_process(self, video_path):
        """Process highlights in background while recording continues."""
        try:
            time.sleep(3)  # Wait for file to be fully written
            
            min_priority = self.config.get('auto_min_priority', 6)
            logger.info(f"\n[Background] Processing highlights from: {video_path}")
            
            self.run_post_processing(video_path, min_priority=min_priority)
            
            logger.info("\n[Background] Processing complete!\n")
        except Exception as e:
            logger.error(f"[Background] Processing failed: {e}")
    
    def stop_live_logging(self):
        """Stop live logging and save event data."""
        logger.info("\n" + "=" * 60)
        logger.info("Stopping live logging...")
        logger.info("=" * 60)
        
        # Stop GSI server (this saves logs)
        self.gsi.stop()
        
        # Get the recording file path before stopping
        recording_path = self.obs.get_last_recording_path()
        
        # Stop OBS recording
        self.obs.stop_recording()
        
        # Disconnect from OBS
        self.obs.disconnect()
        
        logger.info("\n✓ Live logging session complete")
        logger.info(f"✓ Events saved to: {self.gsi.log_file}")
        
        return recording_path
    
    def run_post_processing(self, source_video, api_key=None, min_priority=6):
        """
        PHASE 2 & 3: Post-processing workflow.
        
        Analyzes match logs with AI and creates highlight clips.
        Run this AFTER the match is complete and recorded.
        
        Args:
            source_video: Path to OBS recording
            api_key: Google API key (or set GOOGLE_API_KEY env variable)
            min_priority: Minimum priority for clips (1-10, default: 6)
        """
        logger.info("\n" + "=" * 60)
        logger.info("CS2 CAPTURE-TO-CONTENT PIPELINE - POST-PROCESSING PHASE")
        logger.info("=" * 60)
        
        # Verify source video exists
        if not Path(source_video).exists():
            logger.error(f"Source video not found: {source_video}")
            return False
        
        # Step 1: AI Analysis
        logger.info("\n[PHASE 2] AI DIRECTOR - Analyzing match events...")
        logger.info("=" * 60)
        
        self.ai_director = AIDirector(api_key=api_key)
        
        try:
            highlights = self.ai_director.analyze_match_log(self.gsi.log_file)
            
            if not highlights:
                logger.warning("No highlights identified by AI Director.")
                return False
            
            # Filter by priority
            highlights = self.ai_director.filter_highlights_by_priority(highlights, min_priority)
            
            if not highlights:
                logger.warning(f"No highlights with priority >= {min_priority}")
                return False
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return False
        
        # Step 2: Video Processing
        logger.info("\n[PHASE 3] VIDEO ENGINE - Creating highlight clips...")
        logger.info("=" * 60)
        
        self.video_editor = VideoEditor(
            source_video=source_video,
            output_dir=self.config.get('output_dir', 'highlights'),
            use_gpu=self.config.get('use_gpu', True)
        )
        
        # Create all highlights
        created_clips = self.video_editor.create_highlights_batch(highlights)
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ POST-PROCESSING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"\n✓ Created {len(created_clips)} highlight clips")
        logger.info(f"✓ Output directory: {self.video_editor.output_dir}")
        
        return True


def main():
    """Main entry point with example usage."""
    
    # Configuration
    config = {
        'obs_host': 'localhost',
        'obs_port': 4455,
        'obs_password': '',
        'gsi_port': 3000,
        'log_file': 'match_log.json',
        'output_dir': 'highlights',
        'use_gpu': True,
        'auto_recording': True,      # Automatically start/stop recording based on match detection
        'continuous_mode': True,     # Enable continuous multi-match recording
        'auto_process': True,        # Automatically process highlights after match
        'auto_min_priority': 6       # Minimum priority for auto-processing
    }
    
    pipeline = CS2HighlightPipeline(config)
    
    # Mode selection
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == 'live':
            # LIVE LOGGING MODE
            # Usage: python main.py live
            if pipeline.start_live_logging():
                try:
                    # Keep running until Ctrl+C
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    recording_path = pipeline.stop_live_logging()
                    
                    # Auto-process highlights if enabled
                    if config.get('auto_process', False):
                        logger.info("\n" + "=" * 60)
                        logger.info("AUTO-PROCESSING ENABLED")
                        logger.info("=" * 60)
                        
                        if recording_path:
                            logger.info(f"\nStarting automatic highlight processing...")
                            logger.info(f"Recording: {recording_path}")
                            
                            time.sleep(2)  # Brief pause for OBS to finish writing
                            
                            min_priority = config.get('auto_min_priority', 6)
                            pipeline.run_post_processing(recording_path, min_priority=min_priority)
                        else:
                            logger.warning("Could not auto-process: recording path not found")
                            logger.info("You can manually process with: python main.py process <video_path>")
        
        elif mode == 'process':
            # POST-PROCESSING MODE
            # Usage: python main.py process <video_path> [api_key] [min_priority]
            #    OR: python main.py process <video_path> [min_priority]
            if len(sys.argv) < 3:
                print("Usage: python main.py process <video_path> [api_key] [min_priority]")
                print("   OR: python main.py process <video_path> [min_priority]")
                print("Example: python main.py process recording.mp4 your-google-api-key 6")
                print("Example: python main.py process recording.mp4 6")
                sys.exit(1)
            
            video_path = sys.argv[2]
            
            # Smart argument parsing: detect if 3rd arg is API key or priority
            api_key = None
            min_priority = 6
            
            if len(sys.argv) > 3:
                third_arg = sys.argv[3]
                # If it's a number 1-10, treat as priority
                try:
                    possible_priority = int(third_arg)
                    if 1 <= possible_priority <= 10:
                        min_priority = possible_priority
                    else:
                        # Not a valid priority, assume it's an API key
                        api_key = third_arg
                        min_priority = int(sys.argv[4]) if len(sys.argv) > 4 else 6
                except ValueError:
                    # Not a number, it's an API key
                    api_key = third_arg
                    min_priority = int(sys.argv[4]) if len(sys.argv) > 4 else 6
            
            pipeline.run_post_processing(video_path, api_key, min_priority)
        
        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: live, process")
    
    else:
        # Interactive mode
        print("\n" + "=" * 60)
        print("CS2 CAPTURE-TO-CONTENT PIPELINE")
        print("=" * 60)
        print("\nSelect mode:")
        print("  1. Start live logging (run BEFORE match)")
        print("  2. Process recording (run AFTER match)")
        print("\nOr use command line:")
        print("  python main.py live")
        print("  python main.py process <video_path> [api_key] [min_priority]")
        print("=" * 60 + "\n")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            if pipeline.start_live_logging():
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    recording_path = pipeline.stop_live_logging()
                    
                    # Ask about auto-processing
                    if recording_path:
                        auto_process = input("\nAuto-process highlights now? (y/n): ").strip().lower()
                        if auto_process == 'y':
                            min_priority = input("Minimum priority (1-10, default 6): ").strip()
                            min_priority = int(min_priority) if min_priority else 6
                            
                            time.sleep(2)  # Brief pause
                            pipeline.run_post_processing(recording_path, min_priority=min_priority)
        
        elif choice == '2':
            video_path = input("Enter path to recorded video: ").strip()
            api_key = input("Enter Google API key (or press Enter to use env GOOGLE_API_KEY): ").strip() or None
            min_priority = input("Enter minimum priority (1-10, default 6): ").strip()
            min_priority = int(min_priority) if min_priority else 6
            
            pipeline.run_post_processing(video_path, api_key, min_priority)


if __name__ == '__main__':
    main()
