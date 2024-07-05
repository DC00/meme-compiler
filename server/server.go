package server

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"net/url"
	"os"

	"github.com/DC00/meme-compiler/queue"
)

type Submission struct {
	URL     string `json:"url"`
	Webhook string `json:"webhook"`
}

type CompilationRequest struct {
	Webhook string `json:"webhook"`
}

type Response struct {
	Message string `json:"message"`
}

type Server struct {
	TasksClient *queue.CloudTasksClient
}

func NewServer(tasksClient *queue.CloudTasksClient) *Server {
	return &Server{
		TasksClient: tasksClient,
	}
}

func (s *Server) writeResponse(w http.ResponseWriter, statusCode int, message string) {
	w.WriteHeader(statusCode)
	response := Response{Message: message}
	json.NewEncoder(w).Encode(response)
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
		s.writeResponse(w, http.StatusBadRequest, "Could not parse the request. Please submit a different url.")
		return
	}

	// Get the value of the "url" field from the request body and validate
	if submission.URL == "" {
		s.writeResponse(w, http.StatusBadRequest, "Missing url field. Please submit a url to a video!")
		return
	}

	// Check if Reid submitted some weirdness
	_, err = url.ParseRequestURI(submission.URL)
	if err != nil {
		s.writeResponse(w, http.StatusBadRequest, "Invalid url field. Please submit a valid video link!")
		return
	}

	log.Printf("Received submission: URL=%s, Webhook=%s\n", submission.URL, submission.Webhook)

	payload, err := json.Marshal(submission)
	if err != nil {
		log.Println("Failed to marshal JSON payload:", err)
		s.writeResponse(w, http.StatusInternalServerError, "Internal Server Error. Could not create the payload.")
		return
	}

	taskURL := os.Getenv("DOWNLOAD_TASK_URL")
	if taskURL == "" {
		taskURL = "https://mcf-download-b473pkndcq-uk.a.run.app"
	}

	ctx := context.Background()
	err = s.TasksClient.CreateTask(ctx, taskURL, payload)
	if err != nil {
		log.Println("Failed to create task:", err)
		s.writeResponse(w, http.StatusInternalServerError, "Internal Server Error. Could not create task queue.")
		return
	}

	s.writeResponse(w, http.StatusCreated, "Adding video to MemeCompiler")
}

func (s *Server) CreateCompilationHandler(w http.ResponseWriter, r *http.Request) {
	var compilationRequest CompilationRequest
	err := json.NewDecoder(r.Body).Decode(&compilationRequest)
	if err != nil {
		s.writeResponse(w, http.StatusBadRequest, "Could not parse the request. Please submit a different link.")
		return
	}

	log.Printf("Received compilation request: Webhook=%s\n", compilationRequest.Webhook)

	payload, err := json.Marshal(compilationRequest)
	if err != nil {
		log.Println("Failed to marshal JSON payload:", err)
		s.writeResponse(w, http.StatusInternalServerError, "Internal Server Error. Could not create the payload.")
		return
	}

	taskURL := os.Getenv("COMPILATION_TASK_URL")
	if taskURL == "" {
		taskURL = "https://us-east4-meme-compiler.cloudfunctions.net/mcf-concatenate"
	}

	ctx := context.Background()
	err = s.TasksClient.CreateTask(ctx, taskURL, payload)
	if err != nil {
		log.Println("Failed to create task:", err)
		s.writeResponse(w, http.StatusInternalServerError, "Internal Server Error")
		return
	}

	s.writeResponse(w, http.StatusCreated, "Compilation creation requested")
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
