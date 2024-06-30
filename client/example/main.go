package main

import (
	"context"
	"fmt"
	"log"

	"github.com/DC00/meme-compiler/client"
)

func main() {
	c := client.NewClient("identityToken")

	ctx := context.Background()

	// Add a video
	addResp, err := c.Videos.Add(ctx, &client.AddVideoRequest{
		URL: "https://example.com/video.mp4",
		Webhook: "https://example.com/webhook",
	})
	if err != nil {
		log.Fatalf("Error adding video: %v", err)
	}
	fmt.Println("Add video response:", addResp.Message)

	// Create a compilation
	createResp, err := c.Compilations.Create(ctx, &client.CreateCompilationRequest{
		Webhook: "https://example.com/webhook",
	})
	if err != nil {
		log.Fatalf("Error creating compilation: %v", err)
	}
	fmt.Println("Create compilation response:", createResp.Message)
}
