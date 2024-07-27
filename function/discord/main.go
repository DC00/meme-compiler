package function

import (
	"bytes"
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/DC00/meme-compiler/client"
	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/bwmarrin/discordgo"
)

var (
	identityToken = os.Getenv("IDENTITY_TOKEN")
	discordPubKey = os.Getenv("DISCORD_PUBLIC_KEY")
)

func init() {
	functions.HTTP("HandleRequest", handleRequest)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	if !verifyRequest(r) {
		log.Println("Invalid request signature")
		http.Error(w, "Invalid request signature", http.StatusUnauthorized)
		return
	}

	var interaction discordgo.Interaction
	if err := json.NewDecoder(r.Body).Decode(&interaction); err != nil {
		log.Printf("Failed to decode request body: %v", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	log.Printf("Interaction type: %v", interaction.Type)

	// Handle PING requests
	if interaction.Type == discordgo.InteractionPing {
		log.Println("Handling PING request")
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"type": 1,
		})
		log.Println("Returned PING response with type 1")
		return
	}

	response := handleInteraction(interaction)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
	log.Println("Returned response for interaction")
}

func verifyRequest(r *http.Request) bool {
	timestamp := r.Header.Get("X-Signature-Timestamp")
	signature := r.Header.Get("X-Signature-Ed25519")
	body, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("Failed to read request body: %v", err)
		return false
	}
	r.Body = io.NopCloser(bytes.NewBuffer(body)) // Reset the body reader

	decodedPubKey, err := hex.DecodeString(discordPubKey)
	if err != nil {
		log.Printf("Failed to decode public key: %v", err)
		return false
	}

	message := append([]byte(timestamp), body...)
	decodedSignature, err := hex.DecodeString(signature)
	if err != nil {
		log.Printf("Failed to decode signature: %v", err)
		return false
	}

	valid := ed25519.Verify(decodedPubKey, message, decodedSignature)
	if !valid {
		log.Println("Signature verification failed")
	}
	return valid
}

func handleInteraction(interaction discordgo.Interaction) *discordgo.InteractionResponse {
	if interaction.Type == discordgo.InteractionApplicationCommand {
		data := interaction.ApplicationCommandData()
		log.Printf("Handling command: %v", data.Name)
		switch data.Name {
		case "ping":
			return &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionResponseData{
					Content: "Pong!",
				},
			}
		case "addvideo":
			return handleAddVideo(data)
		case "createcompilation":
			return handleCreateCompilation()
		}
	}
	return nil
}

func handleAddVideo(data discordgo.ApplicationCommandInteractionData) *discordgo.InteractionResponse {
	var videoURL string
	for _, option := range data.Options {
		if option.Name == "url" {
			videoURL = option.StringValue()
			break
		}
	}

	if videoURL == "" {
		log.Println("No video URL provided")
		return &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: "Missing url field. Please submit a url to a video!",
			},
		}
	}

	c := client.NewClient(identityToken)

	ctx := context.Background()
	addResp, err := c.Videos.Add(ctx, &client.AddVideoRequest{
		URL: videoURL,
	})
	if err != nil {
		log.Printf("Error adding video: %v", err)
		errorMessage := "Error adding video"
		if addResp != nil {
			errorMessage = addResp.Message
		}
		return &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: fmt.Sprintf("Error adding video: %v", errorMessage),
			},
		}
	}

	log.Println("Successfully added video")
	return &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Content: addResp.Message,
		},
	}
}

func handleCreateCompilation() *discordgo.InteractionResponse {
	c := client.NewClient(identityToken)

	ctx := context.Background()
	compResp, err := c.Compilations.Create(ctx, &client.CreateCompilationRequest{})
	if err != nil {
		log.Printf("Error creating compilation: %v", err)
		return &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: fmt.Sprintf("Error creating compilation: %v", err),
			},
		}
	}

	log.Println("Requested compilation creation")
	return &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Content: compResp.Message,
		},
	}
}
