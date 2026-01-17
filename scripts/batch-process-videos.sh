#!/bin/bash

# Batch process videos from CSV file
# Usage: ./batch-process-videos.sh <csv_file> [output_dir]

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DOWNLOAD_SCRIPT="$SCRIPT_DIR/download-and-normalize.sh"

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
    echo "Usage: $0 <csv_file> [output_dir]"
    echo "  csv_file    - CSV file containing video URLs (one per line)"
    echo "  output_dir  - Directory to save videos and logs (default: current directory)"
    exit 1
}

# Check arguments
if [ $# -lt 1 ]; then
    usage
fi

CSV_FILE="$1"
OUTPUT_DIR="${2:-.}"  # Default to current directory if not specified

# Validate CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    print_error "CSV file not found: $CSV_FILE"
    exit 1
fi

# Validate download script exists
if [ ! -f "$DOWNLOAD_SCRIPT" ]; then
    print_error "Download script not found: $DOWNLOAD_SCRIPT"
    exit 1
fi

if [ ! -x "$DOWNLOAD_SCRIPT" ]; then
    print_error "Download script is not executable: $DOWNLOAD_SCRIPT"
    print_info "Run: chmod +x $DOWNLOAD_SCRIPT"
    exit 1
fi

# Create output directory structure
VIDEOS_DIR="$OUTPUT_DIR/videos"
LOGS_DIR="$OUTPUT_DIR/logs"
mkdir -p "$VIDEOS_DIR" "$LOGS_DIR"

# Create timestamp for this session
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SESSION_LOG="$LOGS_DIR/batch_${TIMESTAMP}.log"
SUCCESS_FILE="$OUTPUT_DIR/success_urls.txt"
FAILED_FILE="$OUTPUT_DIR/failed_urls.txt"

# Initialize or create tracking files
touch "$SUCCESS_FILE" "$FAILED_FILE"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$SESSION_LOG"
}

# Trap for cleanup on script exit
cleanup() {
    log_message "Script interrupted. Cleaning up..."
    print_info "Progress saved. Check logs at: $LOGS_DIR"
    exit 1
}

trap cleanup INT TERM

# Start logging
log_message "=== Batch Video Processing Started ==="
log_message "CSV File: $CSV_FILE"
log_message "Output Directory: $OUTPUT_DIR"

# Read URLs from CSV, filtering out empty lines and comments
print_info "Reading URLs from CSV..."
URLS=()
while IFS= read -r line; do
    # Skip comments and empty lines
    if [[ ! "$line" =~ ^# ]] && [[ -n "$(echo "$line" | sed 's/[[:space:]]//g')" ]]; then
        # Trim whitespace
        line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        URLS+=("$line")
    fi
done < "$CSV_FILE"

TOTAL_URLS=${#URLS[@]}

if [ $TOTAL_URLS -eq 0 ]; then
    print_error "No valid URLs found in CSV file"
    exit 1
fi

print_success "Found $TOTAL_URLS URLs to process"
log_message "Total URLs to process: $TOTAL_URLS"

# Shuffle URLs
print_info "Shuffling URLs randomly..."
SHUFFLED_URLS=($(printf '%s\n' "${URLS[@]}" | shuf))

# Statistics
SUCCESS_COUNT=0
FAILED_COUNT=0
SKIPPED_COUNT=0
START_TIME=$(date +%s)

# Process each URL
print_info "Starting batch processing..."
echo

for i in "${!SHUFFLED_URLS[@]}"; do
    URL="${SHUFFLED_URLS[$i]}"
    CURRENT_NUM=$((i + 1))
    
    # Progress indicator
    print_progress "Processing $CURRENT_NUM of $TOTAL_URLS"
    echo "URL: $URL"
    log_message "Processing [$CURRENT_NUM/$TOTAL_URLS]: $URL"
    
    # Check if URL was already successfully processed
    if grep -Fxq "$URL" "$SUCCESS_FILE" 2>/dev/null; then
        print_info "Already processed successfully, skipping..."
        log_message "Skipped (already processed): $URL"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        echo
        continue
    fi
    
    # Create a temporary log file for this download
    TEMP_LOG=$(mktemp)
    
    # Run download-and-normalize script
    # Redirect stdin to /dev/null to prevent the script from reading input
    if "$DOWNLOAD_SCRIPT" "$URL" "$VIDEOS_DIR" < /dev/null > "$TEMP_LOG" 2>&1; then
        print_success "Successfully processed video"
        log_message "Success: $URL"
        echo "$URL" >> "$SUCCESS_FILE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        
        # Extract normalized filename from log if possible
        NORMALIZED_FILE=$(grep "Output saved to:" "$TEMP_LOG" | sed 's/.*Output saved to: //' || echo "")
        if [ ! -z "$NORMALIZED_FILE" ]; then
            log_message "  Saved as: $(basename "$NORMALIZED_FILE")"
        fi
    else
        print_error "Failed to process video"
        log_message "Failed: $URL"
        echo "$URL" >> "$FAILED_FILE"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        
        # Log error details
        ERROR_MSG=$(tail -n 5 "$TEMP_LOG" | tr '\n' ' ')
        log_message "  Error: $ERROR_MSG"
    fi
    
    # Append download log to session log
    echo "--- Download log for $URL ---" >> "$SESSION_LOG"
    cat "$TEMP_LOG" >> "$SESSION_LOG"
    echo "--- End of download log ---" >> "$SESSION_LOG"
    
    # Clean up temp log
    rm -f "$TEMP_LOG"
    
    echo  # Empty line for readability
    
    # Optional: Add delay to avoid rate limiting
    # Uncomment the following line to add a 2-second delay between downloads
    # sleep 2
done

# Calculate elapsed time
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
ELAPSED_MIN=$((ELAPSED / 60))
ELAPSED_SEC=$((ELAPSED % 60))

# Summary report
echo
echo "========================================="
echo "          BATCH PROCESSING COMPLETE"
echo "========================================="
print_info "Summary:"
echo "  Total URLs:      $TOTAL_URLS"
echo "  Successful:      $SUCCESS_COUNT"
echo "  Failed:          $FAILED_COUNT"
echo "  Skipped:         $SKIPPED_COUNT"
echo "  Time elapsed:    ${ELAPSED_MIN}m ${ELAPSED_SEC}s"
echo
print_info "Output locations:"
echo "  Videos:          $VIDEOS_DIR"
echo "  Session log:     $SESSION_LOG"
echo "  Success list:    $SUCCESS_FILE"
echo "  Failed list:     $FAILED_FILE"
echo "========================================="

# Log summary
log_message "=== Batch Processing Complete ==="
log_message "Successful: $SUCCESS_COUNT, Failed: $FAILED_COUNT, Skipped: $SKIPPED_COUNT"
log_message "Time elapsed: ${ELAPSED_MIN}m ${ELAPSED_SEC}s"

# Exit with appropriate code
if [ $FAILED_COUNT -eq 0 ]; then
    print_success "All videos processed successfully!"
    exit 0
else
    print_info "Some videos failed to process. Check failed_urls.txt for details."
    exit 1
fi