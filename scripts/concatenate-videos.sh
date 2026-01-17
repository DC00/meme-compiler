#!/bin/bash

# Concatenate normalized MP4 videos into a single compilation
# Based on the Go concatenate function implementation
# Usage: ./concatenate-videos.sh <input_dir> [options]

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MIN_VIDEOS=30  # Default minimum videos required (from Go implementation)
OUTPUT_DIR="."
DELETE_SOURCE=false
SHUFFLE=false

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

print_progress() {
    echo -e "${BLUE}[PROGRESS]${NC} $1"
}

# Function to display usage
usage() {
    echo "Usage: $0 <input_dir> [options]"
    echo ""
    echo "Arguments:"
    echo "  input_dir           Directory containing normalized MP4 videos"
    echo ""
    echo "Options:"
    echo "  --min-videos NUM    Minimum videos required (default: 30)"
    echo "  --output-dir DIR    Output directory for compilation (default: current dir)"
    echo "  --shuffle           Randomize video order before concatenation"
    echo "  --delete-source     Delete source videos after successful concatenation"
    echo "  --help              Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 ./videos --min-videos 10 --output-dir ./compilations"
    exit 0
}

# Parse arguments
if [ $# -lt 1 ]; then
    usage
fi

INPUT_DIR=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --min-videos)
            MIN_VIDEOS="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --shuffle)
            SHUFFLE=true
            shift
            ;;
        --delete-source)
            DELETE_SOURCE=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            if [ -z "$INPUT_DIR" ]; then
                INPUT_DIR="$1"
            else
                print_error "Unknown option: $1"
                usage
            fi
            shift
            ;;
    esac
done

# Validate input directory
if [ -z "$INPUT_DIR" ]; then
    print_error "Input directory is required"
    usage
fi

if [ ! -d "$INPUT_DIR" ]; then
    print_error "Input directory does not exist: $INPUT_DIR"
    exit 1
fi

# Check for ffmpeg
command -v ffmpeg >/dev/null 2>&1 || { print_error "ffmpeg is required but not installed. Install it with: brew install ffmpeg"; exit 1; }

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Find all MP4 files in the input directory
print_info "Searching for MP4 videos in: $INPUT_DIR"

VIDEO_FILES=()
while IFS= read -r -d '' file; do
    VIDEO_FILES+=("$file")
done < <(find "$INPUT_DIR" -name "*.mp4" -type f -print0 | sort -z)

VIDEO_COUNT=${#VIDEO_FILES[@]}

# Check minimum video requirement (matching Go implementation)
if [ $VIDEO_COUNT -eq 0 ]; then
    print_error "No MP4 files found in $INPUT_DIR"
    exit 1
fi

if [ $VIDEO_COUNT -lt $MIN_VIDEOS ]; then
    print_error "Not enough videos to create a compilation. Found $VIDEO_COUNT videos, need at least $MIN_VIDEOS."
    exit 1
fi

print_success "Found $VIDEO_COUNT videos to concatenate"

# Shuffle if requested
if [ "$SHUFFLE" = true ]; then
    print_info "Shuffling video order..."
    # Convert array to shuffled array
    SHUFFLED=()
    while IFS= read -r line; do
        SHUFFLED+=("$line")
    done < <(printf '%s\n' "${VIDEO_FILES[@]}" | shuf)
    VIDEO_FILES=("${SHUFFLED[@]}")
fi

# Create temporary directory for processing
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

print_info "Creating temporary working directory: $TEMP_DIR"

# Create the video list file for ffmpeg (matching Go implementation format)
VIDEO_LIST_FILE="$TEMP_DIR/videos-for-ffmpeg.txt"
print_info "Creating video list file for ffmpeg..."

# Write file list in ffmpeg concat format (matching Go: fmt.Fprintf(file, "file '%s'\n", videoFile))
for video_file in "${VIDEO_FILES[@]}"; do
    # Get absolute path for ffmpeg
    abs_path=$(cd "$(dirname "$video_file")" && pwd)/$(basename "$video_file")
    echo "file '$abs_path'" >> "$VIDEO_LIST_FILE"
done

# Display first few entries for verification
print_info "First 5 videos in concatenation list:"
head -n 5 "$VIDEO_LIST_FILE" | sed 's/^/  /'

# Generate output filename with timestamp (matching Go: time.Now().Format("20060102150405"))
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/compilation-${TIMESTAMP}.mp4"

print_info "Output file will be: $OUTPUT_FILE"

# Calculate total input size
TOTAL_SIZE=0
for video_file in "${VIDEO_FILES[@]}"; do
    if [ -f "$video_file" ]; then
        FILE_SIZE=$(stat -f%z "$video_file" 2>/dev/null || stat -c%s "$video_file" 2>/dev/null || echo 0)
        TOTAL_SIZE=$((TOTAL_SIZE + FILE_SIZE))
    fi
done
TOTAL_SIZE_MB=$((TOTAL_SIZE / 1048576))

print_info "Total input size: ${TOTAL_SIZE_MB} MB"

# Check available disk space
if command -v df >/dev/null 2>&1; then
    AVAILABLE_SPACE=$(df "$OUTPUT_DIR" | awk 'NR==2 {print $4}')
    # Convert to MB (assumes KB output from df)
    AVAILABLE_MB=$((AVAILABLE_SPACE / 1024))
    
    if [ $AVAILABLE_MB -lt $TOTAL_SIZE_MB ]; then
        print_error "Insufficient disk space. Need ${TOTAL_SIZE_MB} MB, have ${AVAILABLE_MB} MB"
        exit 1
    fi
fi

# Run ffmpeg command to concatenate (exactly matching Go implementation)
print_progress "Starting video concatenation..."
echo "This may take a while depending on the number and size of videos..."

# Using exact same ffmpeg command from Go: 
# exec.Command("ffmpeg", "-f", "concat", "-safe", "0", "-i", videoListFile, "-c", "copy", outputFile)
if ffmpeg -f concat -safe 0 -i "$VIDEO_LIST_FILE" -c copy "$OUTPUT_FILE" -loglevel error -stats 2>&1; then
    print_success "Video concatenation completed successfully!"
else
    print_error "FFmpeg concatenation failed"
    exit 1
fi

# Verify output file was created
if [ ! -f "$OUTPUT_FILE" ]; then
    print_error "Output file was not created"
    exit 1
fi

# Get output file size
OUTPUT_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo 0)
OUTPUT_SIZE_MB=$((OUTPUT_SIZE / 1048576))

# Get video duration if ffprobe is available
if command -v ffprobe >/dev/null 2>&1; then
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_FILE" 2>/dev/null || echo "0")
    DURATION_MIN=$(echo "$DURATION / 60" | bc 2>/dev/null || echo "unknown")
    DURATION_SEC=$(echo "$DURATION % 60" | bc 2>/dev/null || echo "")
    
    if [ ! -z "$DURATION_SEC" ]; then
        DURATION_STR="${DURATION_MIN}m ${DURATION_SEC}s"
    else
        DURATION_STR="unknown"
    fi
else
    DURATION_STR="unknown"
fi

# Delete source videos if requested (matching Go behavior after successful upload)
if [ "$DELETE_SOURCE" = true ]; then
    print_info "Deleting source videos..."
    for video_file in "${VIDEO_FILES[@]}"; do
        rm -f "$video_file"
    done
    print_success "Source videos deleted"
fi

# Summary report
echo
echo "========================================="
echo "     VIDEO CONCATENATION COMPLETE"
echo "========================================="
print_info "Summary:"
echo "  Input videos:        $VIDEO_COUNT"
echo "  Input size:          ${TOTAL_SIZE_MB} MB"
echo "  Output file:         $OUTPUT_FILE"
echo "  Output size:         ${OUTPUT_SIZE_MB} MB"
if [ "$DURATION_STR" != "unknown" ]; then
    echo "  Total duration:      $DURATION_STR"
fi
echo "  Videos shuffled:     $SHUFFLE"
echo "  Source deleted:      $DELETE_SOURCE"
echo "========================================="

print_success "Compilation video created successfully: $(basename "$OUTPUT_FILE")"

# Optional: Create a log file with the list of videos included
LOG_FILE="$OUTPUT_DIR/compilation-${TIMESTAMP}.log"
{
    echo "Compilation created at: $(date)"
    echo "Number of videos: $VIDEO_COUNT"
    echo "Videos included:"
    for video_file in "${VIDEO_FILES[@]}"; do
        echo "  - $(basename "$video_file")"
    done
} > "$LOG_FILE"
print_info "Video list saved to: $LOG_FILE"

exit 0