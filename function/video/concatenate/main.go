package concatenate

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"time"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"google.golang.org/api/storage/v1"
)

const (
	normalizedVideoBucket = "videos-normalized-3ec32eeafcfe42f28cb86296afa48673"
	compilationsBucket    = "compilations-f714ffc72eaf414ea0f51b18f4678383"
)

func init() {
	functions.HTTP("ConcatenateVideos", concatenateVideos)
}

type ErrorResponse struct {
	Error string `json:"error"`
}

func writeErrorResponse(w http.ResponseWriter, message string, code int) {
	w.WriteHeader(code)
	errorResponse := ErrorResponse{Error: message}
	json.NewEncoder(w).Encode(errorResponse)
}

func concatenateVideos(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	storageService, err := storage.NewService(ctx)
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to create storage service: %v", err), http.StatusInternalServerError)
		return
	}

	// Get the minimum number of videos from the environment variable, or use default value of 30
	minVideosStr := os.Getenv("MIN_VIDEOS")
	minVideos := 30
	if minVideosStr != "" {
		minVideos, err = strconv.Atoi(minVideosStr)
		if err != nil {
			writeErrorResponse(w, fmt.Sprintf("Invalid MIN_VIDEOS environment variable: %v", err), http.StatusBadRequest)
			return
		}
	}

	// Count the number of videos in the "normalized" bucket
	objects, err := storageService.Objects.List(normalizedVideoBucket).Do()
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to list objects: %v", err), http.StatusInternalServerError)
		return
	}
	videoCount := len(objects.Items)

	if videoCount < minVideos {
		writeErrorResponse(w, fmt.Sprintf("Not enough videos to create a compilation. Found %d videos, need at least %d.", videoCount, minVideos), http.StatusNoContent)
		return
	}

	// Create a temporary directory to store the downloaded videos
	tempDir, err := os.MkdirTemp("", "normalized-videos")
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to create temporary directory: %v", err), http.StatusInternalServerError)
		return
	}
	defer os.RemoveAll(tempDir)

	// Download the videos from the "normalized" bucket
	var videoFiles []string
	for _, object := range objects.Items {
		videoFile := filepath.Join(tempDir, object.Name)
		file, err := os.Create(videoFile)
		if err != nil {
			writeErrorResponse(w, fmt.Sprintf("Failed to create file: %v", err), http.StatusInternalServerError)
			return
		}
		defer file.Close()

		res, err := storageService.Objects.Get(normalizedVideoBucket, object.Name).Download()
		if err != nil {
			writeErrorResponse(w, fmt.Sprintf("Failed to download object: %v", err), http.StatusInternalServerError)
			return
		}
		defer res.Body.Close()

		if _, err := io.Copy(file, res.Body); err != nil {
			writeErrorResponse(w, fmt.Sprintf("Failed to copy video: %v", err), http.StatusInternalServerError)
			return
		}

		videoFiles = append(videoFiles, videoFile)
	}

	// Create the video list file for ffmpeg
	videoListFile := filepath.Join(tempDir, "videos-for-ffmpeg.txt")
	file, err := os.Create(videoListFile)
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to create video list file: %v", err), http.StatusInternalServerError)
		return
	}
	defer file.Close()

	for _, videoFile := range videoFiles {
		fmt.Fprintf(file, "file '%s'\n", videoFile)
	}

	outputFile := filepath.Join(tempDir, "output.mp4")

	// Run ffmpeg command to concatenate the videos together
	cmd := exec.Command("ffmpeg", "-f", "concat", "-safe", "0", "-i", videoListFile, "-c", "copy", outputFile)
	if err := cmd.Run(); err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to run ffmpeg command: %v", err), http.StatusInternalServerError)
		return
	}

	timestamp := time.Now().Format("20060102150405") // Format: YYYYMMDDHHmmss

	// Upload the compilation video to the "compilation" bucket with the timestamp in the filename
	outputFileData, err := os.ReadFile(outputFile)
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to read output file: %v", err), http.StatusInternalServerError)
		return
	}
	object := &storage.Object{Name: fmt.Sprintf("compilation-%s.mp4", timestamp)}
	_, err = storageService.Objects.Insert(compilationsBucket, object).Media(bytes.NewReader(outputFileData)).Do()
	if err != nil {
		writeErrorResponse(w, fmt.Sprintf("Failed to upload compilation video: %v", err), http.StatusInternalServerError)
		return
	}

	// Delete the normalized videos from the "normalized" bucket
	for _, object := range objects.Items {
		err := storageService.Objects.Delete(normalizedVideoBucket, object.Name).Do()
		if err != nil {
			log.Printf("Failed to delete object %q: %v", object.Name, err)
		}
	}

	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintf(w, "Compilation video created and uploaded successfully.")
}
