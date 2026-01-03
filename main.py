"""
Main orchestration script for CS2 Capture-to-Content Pipeline.
Coordinates OBS recording, GSI event logging, and post-processing workflow.
"""
import sys
import time
import logging
from pathlib import Path

from obs_manager import OBSManager
from gsi_server import GSIServer
from ai_director import AIDirector
from video_editor import VideoEditor

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
        
        # Initialize components
        self.obs = OBSManager(
            host=self.config.get('obs_host', 'localhost'),
            port=self.config.get('obs_port', 4455),
            password=self.config.get('obs_password', '')
        )
        
        self.gsi = GSIServer(
            obs_manager=self.obs,
            port=self.config.get('gsi_port', 3000),
            log_file=self.config.get('log_file', 'match_log.json')
        )
        
        self.ai_director = None  # Initialize when needed (requires API key)
        self.video_editor = None  # Initialize during post-processing
    
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
        
        # Step 2: Start recording
        logger.info("\n[2/3] Starting OBS recording...")
        start_time = self.obs.start_recording()
        if not start_time:
            logger.error("Failed to start recording.")
            return False
        
        # Step 3: Start GSI server
        logger.info("\n[3/3] Starting GSI server...")
        self.gsi.start()
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ LIVE LOGGING ACTIVE")
        logger.info("=" * 60)
        logger.info("\nYou can now launch CS2 and play your match.")
        logger.info("Game events will be automatically logged with video timestamps.")
        logger.info("\nPress Ctrl+C when match is finished to stop logging.")
        logger.info("=" * 60 + "\n")
        
        return True
    
    def stop_live_logging(self):
        """Stop live logging and save event data."""
        logger.info("\n" + "=" * 60)
        logger.info("Stopping live logging...")
        logger.info("=" * 60)
        
        # Stop GSI server (this saves logs)
        self.gsi.stop()
        
        # Stop OBS recording
        self.obs.stop_recording()
        
        # Disconnect from OBS
        self.obs.disconnect()
        
        logger.info("\n✓ Live logging session complete")
        logger.info(f"✓ Events saved to: {self.gsi.log_file}")
    
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
        'use_gpu': True
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
                    pipeline.stop_live_logging()
        
        elif mode == 'process':
            # POST-PROCESSING MODE
            # Usage: python main.py process <video_path> [api_key] [min_priority]
            if len(sys.argv) < 3:
                print("Usage: python main.py process <video_path> [api_key] [min_priority]")
                print("Example: python main.py process recording.mp4 your-google-api-key 6")
                sys.exit(1)
            
            video_path = sys.argv[2]
            api_key = sys.argv[3] if len(sys.argv) > 3 else None
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
                    pipeline.stop_live_logging()
        
        elif choice == '2':
            video_path = input("Enter path to recorded video: ").strip()
            api_key = input("Enter Google API key (or press Enter to use env GOOGLE_API_KEY): ").strip() or None
            min_priority = input("Enter minimum priority (1-10, default 6): ").strip()
            min_priority = int(min_priority) if min_priority else 6
            
            pipeline.run_post_processing(video_path, api_key, min_priority)


if __name__ == '__main__':
    main()
