#!/bin/bash

# Download and normalize video script
# Usage: ./download-and-normalize.sh <video_url> [output_dir]

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Check if URL is provided
if [ $# -lt 1 ]; then
    print_error "Usage: $0 <video_url> [output_dir]"
    exit 1
fi

VIDEO_URL="$1"
OUTPUT_DIR="${2:-.}"  # Default to current directory if not specified

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Check for required commands
command -v yt-dlp >/dev/null 2>&1 || { print_error "yt-dlp is required but not installed. Install it with: pip install yt-dlp"; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { print_error "ffmpeg is required but not installed. Install it with: brew install ffmpeg"; exit 1; }

# Set up temporary directory for downloads
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT  # Clean up temp directory on exit

print_info "Starting video download and normalization process..."
print_info "URL: $VIDEO_URL"
print_info "Output directory: $OUTPUT_DIR"
print_info "Temporary directory: $TEMP_DIR"

# Step 1: Download video using yt-dlp
print_info "Downloading video..."

# yt-dlp configuration based on Go implementation
YT_DLP_FORMAT="bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
YT_DLP_OUTPUT_TEMPLATE="$TEMP_DIR/%(extractor)s-%(id)s.%(ext)s"

# Check for proxy environment variables (optional)
YT_DLP_ARGS=""
if [ ! -z "${PROXY_URL:-}" ] && [ ! -z "${PROXY_USER:-}" ] && [ ! -z "${PROXY_PASSWORD:-}" ]; then
    print_info "Using proxy configuration"
    YT_DLP_ARGS="--proxy http://${PROXY_USER}:${PROXY_PASSWORD}@${PROXY_URL}"
fi

# Download the video
if ! yt-dlp $YT_DLP_ARGS \
    --format "$YT_DLP_FORMAT" \
    -o "$YT_DLP_OUTPUT_TEMPLATE" \
    --restrict-filenames \
    --no-check-certificates \
    "$VIDEO_URL"; then
    print_error "Failed to download video"
    exit 1
fi

# Find the downloaded video file
DOWNLOADED_FILE=$(find "$TEMP_DIR" -name "*.mp4" -type f | head -1)

if [ -z "$DOWNLOADED_FILE" ]; then
    print_error "No MP4 file found after download"
    exit 1
fi

print_success "Video downloaded: $(basename "$DOWNLOADED_FILE")"

# Step 2: Normalize video using ffmpeg
print_info "Normalizing video..."

# Generate output filename
BASENAME=$(basename "$DOWNLOADED_FILE" .mp4)
NORMALIZED_FILE="$OUTPUT_DIR/normalized-${BASENAME}.mp4"

# FFmpeg normalization based on Go implementation
# Video: Scale to 720p, add padding, set 30fps
# Audio: Normalize loudness, stereo output, AAC 384k
if ! ffmpeg -i "$DOWNLOADED_FILE" \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30" \
    -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary,aformat=channel_layouts=stereo" \
    -c:v libx264 \
    -preset veryslow \
    -crf 21 \
    -pix_fmt yuv420p \
    -c:a aac \
    -ar 48000 \
    -b:a 384k \
    -y \
    "$NORMALIZED_FILE" \
    -loglevel error \
    -stats; then
    print_error "Failed to normalize video"
    exit 1
fi

print_success "Video normalized successfully!"

# Print file information
if command -v ffprobe >/dev/null 2>&1; then
    print_info "Normalized video information:"
    ffprobe -v quiet -print_format json -show_streams "$NORMALIZED_FILE" | \
        grep -E '"(codec_name|width|height|r_frame_rate|bit_rate)"' | \
        sed 's/^[[:space:]]*/  /'
fi

# Calculate file sizes
ORIGINAL_SIZE=$(du -h "$DOWNLOADED_FILE" | cut -f1)
NORMALIZED_SIZE=$(du -h "$NORMALIZED_FILE" | cut -f1)

print_info "Original file size: $ORIGINAL_SIZE"
print_info "Normalized file size: $NORMALIZED_SIZE"
print_success "Output saved to: $NORMALIZED_FILE"

print_success "Process completed successfully!"