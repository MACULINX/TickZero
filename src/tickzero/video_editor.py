"""
Video Editor Module.

Handles video processing using FFmpeg.
Features:
- Converts 16:9 gameplay footage to 9:16 vertical format for social media.
- Uses complex filtergraphs for blurred background effect.
- Auto-detects hardware acceleration (NVIDIA/Intel/CPU).
"""
import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEditor:
    """
    Handles FFmpeg video processing tasks.
    """
    
    def __init__(self, output_dir: str = "highlights", use_gpu: bool = True):
        """
        Initialize Video Editor.
        
        Args:
            output_dir: Directory to save processed clips.
            use_gpu: Whether to attempt GPU acceleration.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_gpu = use_gpu
        self.hw_config = self.detect_hardware() if use_gpu else self._get_cpu_config()
        
    def detect_hardware(self) -> Dict[str, Any]:
        """
        Detect available hardware acceleration.
        
        Returns:
            Dict containing FFmpeg input/output flags for HW accel.
        """
        if not shutil.which('ffmpeg'):
            logger.error("FFmpeg not found! Please install FFmpeg.")
            return self._get_cpu_config()
            
        try:
            # Check encoders
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'], 
                capture_output=True, 
                text=True
            )
            output = result.stdout
            
            # NVIDIA NVENC
            if 'h264_nvenc' in output or 'hevc_nvenc' in output:
                logger.info("✓ NVIDIA GPU detected (NVENC enabled)")
                return {
                    'type': 'nvidia',
                    'hwaccel_args': ['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda'],
                    # Note: When using complex filters with nvenc, logic can be tricky.
                    # Usually better to decode in SW or CUDA, filter in SW (unless creating complex pure CUDA filter chain), then encode in NVENC.
                    # For stability with complex filters, we often omit global -hwaccel cuda or ensure filters are compatible.
                    # Approach: Use standard -hwaccel cuda but might need transfer to main memory for filters if not using scale_cuda.
                    # Safest generic approach for complex filters:
                    'input_args': ['-hwaccel', 'cuda'], 
                    'video_codec': 'h264_nvenc',
                    'extra_args': ['-preset', 'p4', '-tune', 'hq', '-rc', 'vbr']
                }
                
            # Intel QSV
            if 'h264_qsv' in output or 'hevc_qsv' in output:
                logger.info("✓ Intel GPU detected (QSV enabled)")
                return {
                    'type': 'intel',
                    'input_args': ['-hwaccel', 'qsv'],
                    'video_codec': 'h264_qsv',
                    'extra_args': ['-global_quality', '25', '-look_ahead', '1']
                }
                
        except Exception as e:
            logger.warning(f"Error checking hardware: {e}")
            
        logger.info("ℹ Using CPU encoding (libx264)")
        return self._get_cpu_config()
        
    def _get_cpu_config(self) -> Dict[str, Any]:
        """Return CPU fallback configuration."""
        return {
            'type': 'cpu',
            'input_args': [],
            'video_codec': 'libx264',
            'extra_args': ['-preset', 'fast', '-crf', '23']
        }

    def create_highlights_batch(self, highlights: List[Dict[str, Any]], source_video: str) -> List[str]:
        """
        Process a batch of highlights.
        
        Args:
            highlights: List of highlight dicts (start, end, label).
            source_video: Path to source video file.
            
        Returns:
            List of paths to generated clips.
        """
        created_clips = []
        if not Path(source_video).exists():
            logger.error(f"Source video not found: {source_video}")
            return []
            
        logger.info(f"Processing {len(highlights)} highlights...")
        
        for i, h in enumerate(highlights):
            try:
                # Construct output filename
                timestamp = int(h.get('start', 0))
                label = h.get('label', 'highlight').replace(' ', '_')
                output_name = f"clip_{i+1}_{label}_{timestamp}.mp4"
                output_path = self.output_dir / output_name
                
                logger.info(f"[{i+1}/{len(highlights)}] Creating {output_name} ({h.get('start')}s - {h.get('end')}s)...")
                
                success = self.create_vertical_clip(
                    source=source_video,
                    start_time=h.get('start'),
                    end_time=h.get('end'),
                    output_path=str(output_path)
                )
                
                if success:
                    created_clips.append(str(output_path))
                    
            except Exception as e:
                logger.error(f"Failed to create clip {i+1}: {e}")
                
        return created_clips

    def create_vertical_clip(self, source: str, start_time: float, end_time: float, output_path: str) -> bool:
        """
        Generate a vertical 9:16 clip from a 16:9 source using FFmpeg.
        
        Filtergraph:
        1. Split input into Background (bg) and Foreground (fg)
        2. BG: Scale to filling height (1080x1920), Crop, BoxBlur
        3. FG: Scale to width (1080x~608)
        4. Overlay FG onto BG at center
        """
        duration = end_time - start_time
        if duration <= 0:
            logger.error("Invalid clip duration")
            return False
            
        # Define complex filtergraph
        # Note: boxblur=20:10 -> luma_radius:luma_power[:chroma_radius:chroma_power]
        # setsar=1 ensures square pixels
        filtergraph = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10,setsar=1[bg_blurred];"
            "[fg]scale=1080:-1[fg_scaled];"
            "[bg_blurred][fg_scaled]overlay=(W-w)/2:(H-h)/2"
        )
        
        # Build command
        # using -ss before -i for fast seeking
        cmd = ['ffmpeg', '-y']
        
        # Add Input HW args if safe. 
        # Note: -hwaccel cuda with complex software filters usually requires 
        # explicit hwupload/hwdownload or auto-transfer. 
        # For simplicity and stability with complex filters, we might stick to software decoding 
        # OR let ffmpeg handle auto-negotiation. 
        # The prompt asked for -hwaccel cuda, so we include it. 
        # If filters fail, ffmpeg usually falls back (or errors).
        # To be safe with complex filters (which are often SW only), we might omit -hwaccel input 
        # but keep NVENC output. However, prompt requirement says: "usa -hwaccel cuda"
        
        cmd.extend(self.hw_config.get('input_args', []))
        
        cmd.extend(['-ss', str(start_time)])
        cmd.extend(['-t', str(duration)])
        cmd.extend(['-i', source])
        
        cmd.extend(['-filter_complex', filtergraph])
        
        # Output Codec options
        cmd.extend(['-c:v', self.hw_config['video_codec']])
        cmd.extend(self.hw_config.get('extra_args', []))
        
        # Build Audio
        cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
        
        # Output path
        cmd.append(output_path)
        
        try:
            # Run FFmpeg
            # Using Popen or run. Run is simpler.
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error creating clip: {e}")
            return False
