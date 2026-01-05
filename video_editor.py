"""
VideoEditor: FFmpeg-based video processing for creating vertical highlights.
Converts 16:9 gameplay to 9:16 with simple center crop.
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
        
        # Check for GPU support (returns encoder name or None)
        self.gpu_encoder, self.gpu_type = self._check_gpu_support() if use_gpu else (None, None)
        self.gpu_available = self.gpu_encoder is not None
        
    def _check_gpu_support(self):
        """
        Check for available GPU encoders in priority order:
        1. NVIDIA NVENC (h264_nvenc)
        2. AMD AMF (h264_amf) 
        3. Intel QuickSync (h264_qsv)
        4. Fallback to CPU (libx264)
        
        Returns:
            tuple: (encoder_name, encoder_type) or (None, None) if only CPU available
        """
        # Priority order: NVIDIA > AMD > Intel > CPU
        encoders_to_test = [
            ('h264_nvenc', 'NVIDIA NVENC', 'nvcuda.dll'),
            ('h264_amf', 'AMD AMF', None),
            ('h264_qsv', 'Intel QuickSync', None),
        ]
        
        try:
            # First, get list of available encoders in FFmpeg
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'],
                capture_output=True,
                text=True,
                timeout=5
            )
            available_encoders = result.stdout
            
        except Exception as e:
            logger.warning(f"Could not query FFmpeg encoders: {e}, will use CPU")
            return None, None
        
        # Test each encoder in priority order
        for encoder, friendly_name, dll_hint in encoders_to_test:
            if encoder not in available_encoders:
                logger.debug(f"{friendly_name} encoder not found in FFmpeg")
                continue
            
            # Actually test if the encoder can initialize
            logger.info(f"Testing {friendly_name} availability...")
            test_cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'nullsrc=s=256x256:d=0.1',
                '-c:v', encoder, '-f', 'null', '-'
            ]
            
            try:
                test_result = subprocess.run(
                    test_cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if test_result.returncode == 0:
                    logger.info(f"✓ {friendly_name} GPU encoding available and working")
                    return encoder, friendly_name
                else:
                    # Check for specific error messages
                    stderr = test_result.stderr.lower()
                    if dll_hint and dll_hint.lower() in stderr:
                        logger.info(f"ℹ {friendly_name} found but drivers not available")
                    elif 'cannot load' in stderr or 'not found' in stderr:
                        logger.info(f"ℹ {friendly_name} found but cannot initialize")
                    else:
                        logger.debug(f"{friendly_name} test failed: {test_result.returncode}")
                    continue
                    
            except subprocess.TimeoutExpired:
                logger.warning(f"{friendly_name} test timed out")
                continue
            except Exception as e:
                logger.warning(f"Error testing {friendly_name}: {e}")
                continue
        
        # No GPU encoder worked, will use CPU
        logger.info("ℹ No GPU encoders available, will use CPU (libx264)")
        return None, None
    
    def create_highlight(self, start_time, end_time, output_name, label="highlight"):
        """
        Create a single vertical highlight clip.
        
        9:16 CONVERSION PROCESS:
        - Scales 16:9 source to 1920px height (becomes ~3413x1920)
        - Crops center 1080x1920 region for 9:16 aspect ratio
        - Preserves original audio from recording
        - Clean gameplay without blur effects
        
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
        
        # Scale to 1920px height, then crop center 1080x1920 for 9:16
        # Step 1: scale=-1:1920 scales to 1920px height (width auto-calculated)
        # Step 2: crop=1080:1920 takes center 1080x1920 region
        filter_complex = "[0:v]scale=-1:1920,crop=1080:1920:(iw-1080)/2:0[v]"
        
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
        cmd.extend(['-map', '[v]'])      # Use filtered video output
        cmd.extend(['-map', '0:a?'])     # Map audio stream if present
        
        # Encoder selection with vendor-specific optimizations
        if self.gpu_available:
            cmd.extend(['-c:v', self.gpu_encoder])
            
            # Vendor-specific encoding parameters
            if 'nvenc' in self.gpu_encoder:
                # NVIDIA NVENC settings
                cmd.extend([
                    '-preset', 'p4',              # Balanced preset (p1=fast, p7=slow)
                    '-rc', 'vbr',                 # Variable bitrate
                    '-cq', '23',                  # Quality (lower = better, 0-51)
                    '-b:v', '5M',                 # Target bitrate
                    '-maxrate', '8M',             # Max bitrate
                    '-bufsize', '10M',            # Buffer size
                ])
            elif 'amf' in self.gpu_encoder:
                # AMD AMF settings
                cmd.extend([
                    '-quality', 'balanced',       # Quality preset
                    '-rc', 'vbr_latency',         # Rate control
                    '-qp_i', '23',                # I-frame quality
                    '-qp_p', '23',                # P-frame quality
                    '-b:v', '5M',                 # Target bitrate
                    '-maxrate', '8M',             # Max bitrate
                ])
            elif 'qsv' in self.gpu_encoder:
                # Intel QuickSync settings
                cmd.extend([
                    '-preset', 'medium',          # Encoding speed
                    '-global_quality', '23',      # Quality
                    '-b:v', '5M',                 # Target bitrate
                    '-maxrate', '8M',             # Max bitrate
                    '-bufsize', '10M',            # Buffer size
                ])
        else:
            # CPU fallback - libx264
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
