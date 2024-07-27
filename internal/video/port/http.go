package port

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/DC00/meme-compiler/internal/video/app"
	"github.com/DC00/meme-compiler/internal/video/app/query"
)

type HttpServer struct {
	app app.Application
}

func NewHttpServer(application app.Application) HttpServer {
	return HttpServer{
		app: application,
	}
}

func (h HttpServer) GetV1Videos(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()

	// Create an instance of the query
	videos, err := h.app.Queries.ListVideos.Handle(ctx, query.ListVideosQuery{})
	if err != nil {
		http.Error(w, "Failed to list videos", http.StatusInternalServerError)
		return
	}

	if err := json.NewEncoder(w).Encode(videos); err != nil {
		http.Error(w, "Failed to encode response", http.StatusInternalServerError)
	}
}

// PostVideosV1Download handles the download video request
func (h HttpServer) PostV1Videos(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}
