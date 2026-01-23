"""
OBS Controller Module.

Handles robust communication with OBS Studio via WebSocket.
Features:
- Resilient connection with auto-reconnect
- Accurate timecode synchronization
- Context manager support
- Safe recording control
"""
import time
import logging
from typing import Optional, Dict, Any

# Using imports compatible with generic obs-websocket-py usage
# Adjust if using a specific version (e.g., obsws-python)
try:
    from obswebsocket import obsws, requests as obs_requests, events as obs_events
    from obswebsocket.exceptions import ConnectionFailure
except ImportError:
    # Fallback or mock for environments without the library (for type checking/planning)
    obsws = Any
    obs_requests = Any
    ConnectionFailure = Exception

logger = logging.getLogger(__name__)


class OBSClient:
    """
    Client for OBS Studio WebSocket interface.
    
    Implements Context Manager pattern for safe resource management.
    """
    
    def __init__(self, host: str = "localhost", port: int = 4455, password: str = "", 
                 connect_retries: int = 3, retry_delay: int = 2):
        """
        Initialize OBS Client.
        
        Args:
            host: OBS WebSocket host.
            port: OBS WebSocket port.
            password: OBS WebSocket password.
            connect_retries: Number of retries for initial connection.
            retry_delay: Seconds to wait between retries.
        """
        self.host = host
        self.port = port
        self.password = password
        self.retries = connect_retries
        self.retry_delay = retry_delay
        self.ws: Optional[obsws] = None
        self._is_connected = False
        
    def __enter__(self) -> 'OBSClient':
        """Context manager entry - establishes connection."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes connection."""
        self.disconnect()
        
    def connect(self) -> bool:
        """
        Establish connection to OBS with retry logic.
        
        Returns:
            bool: True if connected successfully, False otherwise.
        """
        if self._is_connected and self.ws:
            return True
            
        for attempt in range(1, self.retries + 2):
            try:
                logger.debug(f"Connecting to OBS ({self.host}:{self.port}), attempt {attempt}...")
                self.ws = obsws(self.host, self.port, self.password)
                self.ws.connect()
                self._is_connected = True
                logger.info("✓ Connected to OBS WebSocket")
                return True
            except (ConnectionFailure, Exception) as e:
                logger.warning(f"Failed to connect to OBS (attempt {attempt}): {e}")
                if attempt <= self.retries:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("✗ Could not connect to OBS after multiple attempts")
                    self._is_connected = False
                    return False
        return False
        
    def disconnect(self):
        """Disconnect from OBS."""
        if self.ws:
            try:
                self.ws.disconnect()
                logger.info("Disconnected from OBS")
            except Exception as e:
                logger.error(f"Error disconnecting from OBS: {e}")
            finally:
                self.ws = None
                self._is_connected = False
                
    def ensure_connection(self):
        """Ensure connection is active, reconnecting if necessary."""
        if not self._is_connected or not self.ws:
            logger.info("Connection lost, attempting to reconnect...")
            self.connect()
            
    def get_current_timestamp(self) -> int:
        """
        Get the precise recording timestamp from OBS.
        
        Returns:
            int: Current recording timestamps in milliseconds.
                 Returns 0 if not recording or error.
        """
        self.ensure_connection()
        if not self.ws:
            return 0
            
        try:
            # GetRecordStatus returns outputActive, outputDuration (ms), outputTimecode (str), etc.
            status = self.ws.call(obs_requests.GetRecordStatus())
            if status.getOutputActive():
                # outputDuration is typically in milliseconds
                return status.getOutputDuration()
            else:
                logger.debug("OBS is not recording, timestamp is 0")
                return 0
        except Exception as e:
            logger.error(f"Error getting timestamp: {e}")
            return 0
            
    def start_recording(self) -> bool:
        """
        Safely start recording.
        
        Checks if recording is already active to prevent errors.
        
        Returns:
            bool: True if recording started or was already active, False on error.
        """
        self.ensure_connection()
        if not self.ws:
            return False
            
        try:
            # Check status first
            status = self.ws.call(obs_requests.GetRecordStatus())
            if status.getOutputActive():
                logger.info("OBS is already recording")
                return True
                
            self.ws.call(obs_requests.StartRecord())
            logger.info("✓ OBS recording started")
            return True
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            return False
            
    def stop_recording(self) -> Optional[str]:
        """
        Safely stop recording and retrieve file path.
        
        Returns:
            Optional[str]: Path to the recording if successful, None otherwise.
        """
        self.ensure_connection()
        if not self.ws:
            return None
            
        try:
            # Check status first
            status = self.ws.call(obs_requests.GetRecordStatus())
            if not status.getOutputActive():
                logger.warning("OBS is not recording, nothing to stop")
                return None
                
            # Stop recording
            response = self.ws.call(obs_requests.StopRecord())
            logger.info("✓ OBS recording stopped")
            
            # Try to retrieve path from response
            # Note: Response structure depends on obs-websocket version
            path = None
            if hasattr(response, 'datain'):
                path = response.datain.get('outputPath')
            
            # Fallback if path not in response (rare, but good to handle)
            if not path:
                # Need to use GetLastReplayBufferReplay or similar if available, 
                # or just return success without path if API doesn't provide it easily here.
                # For now, let's just log.
                logger.debug("Could not retrieve output path directly from StopRecord response")
                
            return path
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
            return None
