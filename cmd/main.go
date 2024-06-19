package main

import (
	"log"
	"os"

	"github.com/DC00/meme-compiler/queue"
	"github.com/DC00/meme-compiler/server"
)

func main() {
	projectID := os.Getenv("GOOGLE_CLOUD_PROJECT")
	locationID := "us-central1"
	queueID := "mc-queue"

	cloudTasksClient, err := queue.NewCloudTasksClient(projectID, locationID, queueID)
	if err != nil {
		log.Fatalf("Failed to create Cloud Tasks client: %v", err)
	}
	defer cloudTasksClient.client.Close()

	srv := server.NewServer(cloudTasksClient)
	srv.Start()
}
