package normalize

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"

	"cloud.google.com/go/storage"
	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/cloudevents/sdk-go/v2/event"
)

const (
	normalizedBucketName = "videos-normalized-3ec32eeafcfe42f28cb86296afa48673"
)

func init() {
	functions.CloudEvent("NormalizeVideo", normalizeVideo)
}

type StorageObjectData struct {
	Bucket string `json:"bucket,omitempty"`
	Name   string `json:"name,omitempty"`
}

func normalizeVideo(ctx context.Context, e event.Event) error {
	var data StorageObjectData
	if err := e.DataAs(&data); err != nil {
		log.Printf("Error parsing CloudEvent data: %v", err)
		return fmt.Errorf("event.DataAs: %v", err)
	}

	client, err := storage.NewClient(ctx)
	if err != nil {
		log.Printf("Error creating storage client: %v", err)
		return fmt.Errorf("storage.NewClient: %v", err)
	}
	defer client.Close()

	inputBucket := client.Bucket(data.Bucket)
	inputObject := inputBucket.Object(data.Name)

	inputFilePath := fmt.Sprintf("/tmp/%s", data.Name)
	outputFilePath := fmt.Sprintf("/tmp/normalized-%s", data.Name)

	// Download the input file from Cloud Storage
	// Note: gsutil is not available in the Cloud Functions runtime
	inputFile, err := os.Create(inputFilePath)
	if err != nil {
		log.Printf("Error creating input file: %v", err)
		return fmt.Errorf("os.Create: %v", err)
	}
	defer inputFile.Close()

	reader, err := inputObject.NewReader(ctx)
	if err != nil {
		log.Printf("Error reading input object: %v", err)
		return fmt.Errorf("inputObject.NewReader: %v", err)
	}
	defer reader.Close()

	if _, err := io.Copy(inputFile, reader); err != nil {
		log.Printf("Error downloading input file: %v", err)
		return fmt.Errorf("io.Copy: %v", err)
	}

	// Normalize the video using FFmpeg
	cmd := exec.Command("ffmpeg", "-i", inputFilePath,
		"-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
		"-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary,aformat=channel_layouts=stereo",
		"-c:v", "libx264", "-preset", "veryslow", "-crf", "21", "-pix_fmt", "yuv420p",
		"-c:a", "aac", "-ar", "48000", "-b:a", "384k",
		outputFilePath)

	if err := cmd.Run(); err != nil {
		log.Printf("Error running FFmpeg: %v", err)
		return fmt.Errorf("cmd.Run: %v", err)
	}

	// Upload the normalized video to the new bucket
	outputBucket := client.Bucket(normalizedBucketName)
	outputObject := outputBucket.Object(data.Name)

	outputFile, err := os.Open(outputFilePath)
	if err != nil {
		log.Printf("Error opening output file: %v", err)
		return fmt.Errorf("os.Open: %v", err)
	}
	defer outputFile.Close()

	writer := outputObject.NewWriter(ctx)
	if _, err := io.Copy(writer, outputFile); err != nil {
		log.Printf("Error uploading normalized video: %v", err)
		return fmt.Errorf("io.Copy: %v", err)
	}
	if err := writer.Close(); err != nil {
		log.Printf("Error closing output object writer: %v", err)
		return fmt.Errorf("writer.Close: %v", err)
	}

	// Delete the original video file
	if err := inputObject.Delete(ctx); err != nil {
		log.Printf("Error deleting original video: %v", err)
		return fmt.Errorf("inputObject.Delete: %v", err)
	}

	// Clean up temporary files
	os.Remove(inputFilePath)
	os.Remove(outputFilePath)

	log.Printf("Video normalized and uploaded to bucket: %s", normalizedBucketName)
	return nil
}
