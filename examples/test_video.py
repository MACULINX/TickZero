"""
Example: Test video conversion filter.
Creates a sample vertical clip from a source video.
"""
from video_editor import VideoEditor
import sys

def test_video_conversion(source_video):
    """Test FFmpeg conversion on a sample segment."""
    
    print("=" * 60)
    print("VIDEO CONVERSION TEST")
    print("=" * 60)
    
    # Create video editor
    editor = VideoEditor(
        source_video=source_video,
        output_dir="test_output",
        use_gpu=True
    )
    
    # Get video info
    print("\n[1] Analyzing source video...")
    info = editor.get_video_info()
    
    if info:
        duration = float(info.get('format', {}).get('duration', 0))
        print(f"   ✓ Video duration: {duration:.1f}s")
        
        video_stream = next(
            (s for s in info.get('streams', []) if s.get('codec_type') == 'video'),
            None
        )
        
        if video_stream:
            width = video_stream.get('width', 0)
            height = video_stream.get('height', 0)
            print(f"   ✓ Resolution: {width}x{height}")
    
    # Create a test clip (first 10 seconds)
    print("\n[2] Creating test vertical clip...")
    print("   Converting first 10 seconds to 9:16 format...")
    
    result = editor.create_highlight(
        start_time=0,
        end_time=10,
        output_name="test_vertical_clip",
        label="test"
    )
    
    if result:
        print("\n" + "=" * 60)
        print("✓ TEST COMPLETE")
        print("=" * 60)
        print(f"\n✓ Test clip created: {result}")
        print("\nOpen the file to verify:")
        print("  - Resolution is 1080x1920 (vertical)")
        print("  - Background is blurred")
        print("  - Gameplay is centered")
        print("=" * 60)
    else:
        print("\n❌ Test failed. Check FFmpeg installation and source video path.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_video.py <source_video_path>")
        print("Example: python test_video.py C:\\Videos\\cs2_gameplay.mp4")
        sys.exit(1)
    
    source = sys.argv[1]
    test_video_conversion(source)
