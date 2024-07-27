package query

import (
	"context"
	"github.com/DC00/meme-compiler/internal/video/domain/video"
)

// ListVideosQuery represents the input for the ListVideos query.
type ListVideosQuery struct {
	// Add any filtering or pagination options here if needed
}

// ListVideosHandler is responsible for handling the ListVideos query.
type ListVideosHandler struct {
	readModel ListVideosReadModel
}

// ListVideosReadModel is an interface that defines the data access for the query.
type ListVideosReadModel interface {
	ListVideos(ctx context.Context) ([]*video.Video, error)
}

// NewListVideosHandler creates a new ListVideosHandler.
func NewListVideosHandler(readModel ListVideosReadModel) ListVideosHandler {
	return ListVideosHandler{
		readModel: readModel,
	}
}

// Handle processes the ListVideos query and returns a list of videos.
func (h ListVideosHandler) Handle(ctx context.Context, query ListVideosQuery) ([]*video.Video, error) {
	return h.readModel.ListVideos(ctx)
}
