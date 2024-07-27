package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"

	"cloud.google.com/go/storage"
)

const (
	bucketName = "videos-quarantine-2486aa1dcdb442fda0c2f090761b4479"
)

type Submission struct {
	URL     string `json:"url"`
	Webhook string `json:"webhook"`
}

func main() {
	log.Print("Starting server...")
	http.HandleFunc("/", handler)

	// Determine port for HTTP service.
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("Defaulting to port %s", port)
	}

	// Start HTTP server.
	log.Printf("Listening on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	log.Print("Handler invoked")
	// Request is validated in Meme Compiler API. Parse and use URL directly.
	var submission Submission
	err := json.NewDecoder(r.Body).Decode(&submission)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		log.Printf("Failed to decode request body: %v", err)
		return
	}
	log.Printf("Received submission: %+v", submission)

	// Set the path to the "yt-dlp" binary
	ytdlpPath := "/usr/local/bin/yt-dlp"
	log.Printf("Using yt-dlp binary at: %s", ytdlpPath)

	// Set the additional flags for "yt-dlp"
	format := "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
	outputTemplate := "%(extractor)s-%(id)s.%(ext)s"
	targetDir := "/tmp"
	videoFileTemplate := filepath.Join(targetDir, outputTemplate)
	log.Printf("yt-dlp output template: %s", videoFileTemplate)

	// Fetch proxy credentials from environment variables
	proxyUser := os.Getenv("PROXY_USER")
	proxyPassword := os.Getenv("PROXY_PASSWORD")
	proxyURL := os.Getenv("PROXY_URL")

	if proxyUser == "" || proxyPassword == "" || proxyURL == "" {
		http.Error(w, "Proxy credentials or URL are not set", http.StatusInternalServerError)
		log.Print("Proxy credentials or URL are not set")
		return
	}

	proxy := fmt.Sprintf("http://%s:%s@%s", proxyUser, proxyPassword, proxyURL)

	// Create the "yt-dlp" command with the specified flags
	cmd := exec.Command(ytdlpPath, "--proxy", proxy, "--format", format, "-o", videoFileTemplate, "--restrict-filenames", "--no-check-certificates", submission.URL)

	// Execute the "yt-dlp" command to download the video
	output, err := cmd.CombinedOutput()
	if err != nil {
		http.Error(w, fmt.Sprintf("Error downloading video: %s", string(output)), http.StatusInternalServerError)
		log.Printf("yt-dlp error: %s", string(output))
		return
	}
	log.Printf("yt-dlp output: %s", string(output))

	// Find the downloaded MP4 file in the "/tmp" directory
	files, err := filepath.Glob("/tmp/*.mp4")
	if err != nil {
		http.Error(w, "Failed to search for downloaded video file", http.StatusInternalServerError)
		log.Printf("Error searching for downloaded video file: %v", err)
		return
	}

	if len(files) == 0 {
		http.Error(w, "No downloaded video file found", http.StatusInternalServerError)
		log.Print("No downloaded video file found")
		return
	}

	videoFilePath := files[0]
	log.Printf("Downloaded video file found: %s", videoFilePath)

	// Create a new Cloud Storage client
	ctx := context.Background()
	client, err := storage.NewClient(ctx)
	if err != nil {
		http.Error(w, "Failed to create Cloud Storage client", http.StatusInternalServerError)
		log.Printf("Error creating Cloud Storage client: %v", err)
		return
	}
	defer client.Close()

	// Create a new object handle in the bucket
	obj := client.Bucket(bucketName).Object(filepath.Base(videoFilePath))
	log.Printf("Created Cloud Storage object handle for: %s", obj.ObjectName())

	// Check if the video file already exists in the bucket
	exists, err := obj.Attrs(ctx)
	if err == nil && exists != nil {
		// Video file already exists in the bucket
		log.Printf("Video file already exists in the bucket: %s", obj.ObjectName())

		// Delete the temporary video file from the container
		err = os.Remove(videoFilePath)
		if err != nil {
			log.Printf("Failed to delete temporary video file: %s", err)
		}

		return
	}

	// Open the downloaded video file
	videoFile, err := os.Open(videoFilePath)
	if err != nil {
		http.Error(w, "Failed to open video file", http.StatusInternalServerError)
		log.Printf("Error opening video file: %v", err)
		return
	}
	defer videoFile.Close()

	// Upload the video file to Cloud Storage
	writer := obj.NewWriter(ctx)
	if _, err := io.Copy(writer, videoFile); err != nil {
		http.Error(w, "Failed to upload video to Cloud Storage", http.StatusInternalServerError)
		log.Printf("Error uploading video to Cloud Storage: %v", err)
		return
	}
	if err := writer.Close(); err != nil {
		http.Error(w, "Failed to close Cloud Storage writer", http.StatusInternalServerError)
		log.Printf("Error closing Cloud Storage writer: %v", err)
		return
	}

	// Delete the temporary video file from the container
	err = os.Remove(videoFilePath)
	if err != nil {
		log.Printf("Failed to delete temporary video file: %s", err)
	}

	// Send a response back to the client
	log.Printf("Video downloaded and uploaded to Cloud Storage bucket: %s", bucketName)
}
