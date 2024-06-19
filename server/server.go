// server/server.go

package server

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/DC00/meme-compiler/queue"
)

type Submission struct {
	URL string `json:"url"`
}

type RequestPayload struct {
	URL string `json:"url"`
}

type Server struct {
	TasksClient *queue.CloudTasksClient
}

func NewServer(tasksClient *queue.CloudTasksClient) *Server {
	return &Server{
		TasksClient: tasksClient,
	}
}

func (s *Server) IndexHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(`<!DOCTYPE html>
	<html>
	<head>
		<title>Meme Compiler</title>
	</head>
	<body>
		<h1>Meme Compiler</h1>
	</body>
	</html>`))
}

func (server *Server) CreateSubmissionHandler(w http.ResponseWriter, r *http.Request) {
	var submission Submission
	err := json.NewDecoder(r.Body).Decode(&submission)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	url := submission.URL
	fmt.Printf("Received submission: %s\n", url)

	payload := RequestPayload{URL: url}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		log.Println("Failed to marshal JSON payload:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	taskURL := "https://mcf-download-b473pkndcq-uk.a.run.app"

	ctx := context.Background()
	err = server.TasksClient.CreateTask(ctx, taskURL, jsonPayload)
	if err != nil {
		log.Println("Failed to create task:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Write([]byte("Task created"))
}

func (s *Server) CreateCompilationHandler(w http.ResponseWriter, r *http.Request) {
	// Your implementation here
}

func (s *Server) Start() {
	http.HandleFunc("/", s.IndexHandler)
	http.HandleFunc("/api/videos/v1/add", s.CreateSubmissionHandler)
	http.HandleFunc("/api/compilations/v1/create", s.CreateCompilationHandler)

	addr := ":8080"
	fmt.Printf("Server listening on %s\n", addr)

	log.Fatal(http.ListenAndServe(addr, nil))
}
