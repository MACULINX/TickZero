"""
VideoEditor: FFmpeg-based video processing for creating vertical highlights.
Converts 16:9 gameplay to 9:16 with blurred background and centered foreground.
"""
import subprocess
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEditor:
    """Handles video cutting and format conversion using FFmpeg."""
    
    def __init__(self, source_video, output_dir="highlights", use_gpu=True):
        """
        Initialize Video Editor.
        
        Args:
            source_video: Path to source recording (16:9)
            output_dir: Directory to save highlights
            use_gpu: Try to use hardware acceleration (NVENC)
        """
        self.source_video = source_video
        self.output_dir = output_dir
        self.use_gpu = use_gpu
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Check if GPU encoding is available
        self.gpu_available = self._check_gpu_support() if use_gpu else False
        
    def _check_gpu_support(self):
        """Check if NVENC (NVIDIA GPU encoding) is available."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'],
                capture_output=True,
                text=True,
                timeout=5
            )
            has_nvenc = 'h264_nvenc' in result.stdout
            if has_nvenc:
                logger.info("✓ NVENC GPU encoding available")
            else:
                logger.info("ℹ GPU encoding not available, will use CPU")
            return has_nvenc
        except Exception as e:
            logger.warning(f"Could not check GPU support: {e}")
            return False
    
    def create_highlight(self, start_time, end_time, output_name, label="highlight"):
        """
        Create a single vertical highlight clip.
        
        FILTER GRAPH EXPLANATION:
        - Background Layer: Scale to 1920px height → Crop to 1080x1920 → Heavy blur
        - Foreground Layer: Scale to 1080px width (maintains aspect) → Overlay centered
        - Result: 9:16 vertical video with blurred background + centered gameplay
        
        Args:
            start_time: Start timestamp in seconds (from video_time)
            end_time: End timestamp in seconds
            output_name: Name for output file (without extension)
            label: Label/description for the clip
            
        Returns:
            str: Path to created highlight, or None if failed
        """
        duration = end_time - start_time
        output_path = os.path.join(self.output_dir, f"{output_name}.mp4")
        
        logger.info(f"Creating highlight: {label}")
        logger.info(f"  Time: {start_time:.1f}s → {end_time:.1f}s ({duration:.1f}s)")
        logger.info(f"  Output: {output_path}")
        
        # Complex filter for 16:9 → 9:16 conversion
        # [0:v] = input video stream
        filter_complex = (
            # BACKGROUND: Blur layer that fills entire 9:16 frame
            "[0:v]scale=-1:1920,crop=1080:1920,boxblur=20:5[bg];"
            
            # FOREGROUND: Scaled gameplay centered on screen
            "[0:v]scale=1080:-1[fg];"
            
            # COMPOSITE: Overlay foreground on blurred background
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"
        )
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y']  # -y = overwrite output
        
        # Input configuration
        cmd.extend([
            '-ss', str(start_time),           # Seek to start (fast seek before input)
            '-i', self.source_video,          # Input file
            '-t', str(duration),              # Duration to encode
        ])
        
        # Video encoding
        cmd.extend(['-filter_complex', filter_complex])
        cmd.extend(['-map', '[v]'])  # Use filtered video output
        
        # Encoder selection
        if self.gpu_available:
            cmd.extend([
                '-c:v', 'h264_nvenc',         # NVIDIA GPU encoder
                '-preset', 'p4',              # Balanced preset (p1=fast, p7=slow)
                '-rc', 'vbr',                 # Variable bitrate
                '-cq', '23',                  # Quality (lower = better, 0-51)
                '-b:v', '5M',                 # Target bitrate
                '-maxrate', '8M',             # Max bitrate
                '-bufsize', '10M',            # Buffer size
            ])
        else:
            cmd.extend([
                '-c:v', 'libx264',            # CPU encoder (fallback)
                '-preset', 'medium',          # Encoding speed (faster = lower quality)
                '-crf', '23',                 # Quality (lower = better, 0-51)
            ])
        
        # Audio encoding
        cmd.extend([
            '-c:a', 'aac',                    # AAC audio codec
            '-b:a', '128k',                   # Audio bitrate
            '-ac', '2',                       # Stereo
        ])
        
        # Output configuration
        cmd.extend([
            '-movflags', '+faststart',        # Web optimization
            '-pix_fmt', 'yuv420p',            # Compatibility
            output_path
        ])
        
        try:
            # Execute FFmpeg
            logger.info("  ⚙ Encoding...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Check if file was created
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                    logger.info(f"  ✓ Created: {output_path} ({file_size:.1f} MB)")
                    return output_path
                else:
                    logger.error("  ✗ FFmpeg succeeded but file not found")
                    return None
            else:
                logger.error(f"  ✗ FFmpeg failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("  ✗ FFmpeg timeout (>5 minutes)")
            return None
        except Exception as e:
            logger.error(f"  ✗ Error running FFmpeg: {e}")
            return None
    
    def create_highlights_batch(self, highlights, prefix="clip"):
        """
        Create multiple highlights from a list.
        
        Args:
            highlights: List of dicts with 'start', 'end', 'label' keys
            prefix: Prefix for output filenames
            
        Returns:
            list: Paths to successfully created highlights
        """
        created_files = []
        
        for i, highlight in enumerate(highlights, 1):
            start = highlight.get('start', 0)
            end = highlight.get('end', 0)
            label = highlight.get('label', 'highlight')
            priority = highlight.get('priority', 5)
            
            # Generate filename
            output_name = f"{prefix}_{i:02d}_{label}_p{priority}"
            
            # Create the clip
            result = self.create_highlight(start, end, output_name, label)
            
            if result:
                created_files.append(result)
        
        logger.info(f"✓ Batch complete: {len(created_files)}/{len(highlights)} highlights created")
        return created_files
    
    def get_video_info(self):
        """
        Get source video information using ffprobe.
        
        Returns:
            dict: Video metadata (duration, resolution, fps, etc.)
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.source_video
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
        
        return None
