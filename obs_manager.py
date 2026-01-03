"""
OBSManager: Handles OBS WebSocket connection and recording control.
Captures precise recording start timestamp for video synchronization.
"""
import time
from datetime import datetime
from obswebsocket import obsws, requests as obs_requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OBSManager:
    """Manages OBS WebSocket connection and recording operations."""
    
    def __init__(self, host="localhost", port=4455, password=""):
        """
        Initialize OBS WebSocket connection.
        
        Args:
            host: OBS WebSocket host (default: localhost)
            port: OBS WebSocket port (default: 4455 for OBS 28+)
            password: WebSocket password if configured
        """
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self.recording_start_time = None  # System timestamp when recording started (T=0)
        self.is_recording = False
        
    def connect(self):
        """Establish connection to OBS WebSocket."""
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            logger.info(f"✓ Connected to OBS WebSocket at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to OBS: {e}")
            return False
    
    def disconnect(self):
        """Close OBS WebSocket connection."""
        if self.ws:
            self.ws.disconnect()
            logger.info("Disconnected from OBS")
    
    def start_recording(self):
        """
        Start OBS recording and capture the precise start timestamp.
        This timestamp (T=0) is the reference point for all video cuts.
        
        Returns:
            float: System timestamp (time.time()) when recording started
        """
        try:
            # Check if already recording
            status = self.ws.call(obs_requests.GetRecordStatus())
            if status.getOutputActive():
                logger.warning("Recording already in progress")
                self.is_recording = True
                # If we don't have a start time, use current time as reference
                if not self.recording_start_time:
                    self.recording_start_time = time.time()
                return self.recording_start_time
            
            # Start recording
            self.ws.call(obs_requests.StartRecord())
            
            # Capture the EXACT moment recording started
            # This is our T=0 reference point for all video timestamps
            self.recording_start_time = time.time()
            self.is_recording = True
            
            logger.info(f"✓ Recording started at {datetime.fromtimestamp(self.recording_start_time).strftime('%H:%M:%S.%f')}")
            logger.info(f"  Reference timestamp (T=0): {self.recording_start_time}")
            
            return self.recording_start_time
            
        except Exception as e:
            logger.error(f"✗ Failed to start recording: {e}")
            return None
    
    def stop_recording(self):
        """Stop OBS recording."""
        try:
            self.ws.call(obs_requests.StopRecord())
            self.is_recording = False
            duration = time.time() - self.recording_start_time if self.recording_start_time else 0
            logger.info(f"✓ Recording stopped. Total duration: {duration:.2f}s")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to stop recording: {e}")
            return False
    
    def get_recording_status(self):
        """
        Get current recording status.
        
        Returns:
            dict: Recording status information
        """
        try:
            status = self.ws.call(obs_requests.GetRecordStatus())
            return {
                "is_recording": status.getOutputActive(),
                "recording_paused": status.getOutputPaused() if hasattr(status, 'getOutputPaused') else False,
                "start_time": self.recording_start_time
            }
        except Exception as e:
            logger.error(f"Error getting recording status: {e}")
            return {"is_recording": False, "recording_paused": False, "start_time": None}
    
    def calculate_video_timestamp(self, event_time):
        """
        Convert a system timestamp to video timestamp (seconds from recording start).
        
        CRITICAL SYNCHRONIZATION LOGIC:
        - OBS starts recording at T=0 (self.recording_start_time)
        - Game events arrive with system timestamps (event_time)
        - Video timestamp = event_time - recording_start_time
        
        Args:
            event_time: System timestamp (time.time()) when event occurred
            
        Returns:
            float: Seconds from start of recording (video timestamp)
        """
        if not self.recording_start_time:
            logger.warning("Recording start time not set. Cannot calculate video timestamp.")
            return 0.0
        
        video_timestamp = event_time - self.recording_start_time
        
        # Sanity check: video timestamp should be positive
        if video_timestamp < 0:
            logger.warning(f"Negative video timestamp detected: {video_timestamp}s. Event occurred before recording started.")
            return 0.0
        
        return video_timestamp
