package server

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"

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

func (s *Server) CreateSubmissionHandler(w http.ResponseWriter, r *http.Request) {
	var submission Submission
	err := json.NewDecoder(r.Body).Decode(&submission)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if submission.URL == "" {
		http.Error(w, `{"error": "URL is required"}`, http.StatusBadRequest)
		return
	}

	url := submission.URL
	log.Printf("Received submission: %s\n", url)

	payload := RequestPayload{URL: url}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		log.Println("Failed to marshal JSON payload:", err)
		http.Error(w, `{"error": "Internal Server Error"}`, http.StatusInternalServerError)
		return
	}

	taskURL := os.Getenv("DOWNLOAD_TASK_URL")
	if taskURL == "" {
		taskURL = "https://mcf-download-b473pkndcq-uk.a.run.app"
	}

	ctx := context.Background()
	err = s.TasksClient.CreateTask(ctx, taskURL, jsonPayload)
	if err != nil {
		log.Println("Failed to create task:", err)
		http.Error(w, `{"error": "Internal Server Error"}`, http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(`{"message": "Adding video to MemeCompiler"}`))
}

func (s *Server) CreateCompilationHandler(w http.ResponseWriter, r *http.Request) {
	payload := "{}"
	taskURL := os.Getenv("COMPILATION_TASK_URL")
	if taskURL == "" {
		taskURL = "https://us-east4-meme-compiler.cloudfunctions.net/mcf-concatenate"
	}

	ctx := context.Background()
	err := s.TasksClient.CreateTask(ctx, taskURL, []byte(payload))
	if err != nil {
		log.Println("Failed to create task:", err)
		http.Error(w, `{"error": "Internal Server Error"}`, http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(`{"message": "Creating compilation. This may take a few minutes."}`))
}

func (s *Server) Start() {
	http.HandleFunc("/", s.IndexHandler)
	http.HandleFunc("/api/videos/v1/add", s.CreateSubmissionHandler)
	http.HandleFunc("/api/compilations/v1/create", s.CreateCompilationHandler)

	// Determine port for HTTP service.
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("defaulting to port %s", port)
	}

	// Start HTTP server.
	log.Printf("listening on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}
