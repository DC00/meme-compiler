package main

import (
	"log"

	"github.com/DC00/meme-compiler/queue"
	"github.com/DC00/meme-compiler/server"
)

func main() {
	projectID := "meme-compiler"
	locationID := "us-central1"
	queueID := "mc-queue"

	cloudTasksClient, err := queue.NewCloudTasksClient(projectID, locationID, queueID)
	if err != nil {
		log.Fatalf("Failed to create Cloud Tasks client: %v", err)
	}

	srv := server.NewServer(cloudTasksClient)
	srv.Start()
}
