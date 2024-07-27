package service

import (
	"context"

	"github.com/DC00/meme-compiler/internal/video/adapter"
	"github.com/DC00/meme-compiler/internal/video/app"
	"github.com/DC00/meme-compiler/internal/video/app/query"
)

func NewApplication(ctx context.Context) app.Application {
	// Initialize the GCS repository
	videoRepo := adapter.NewGcsVideoRepository()

	return app.Application{
		Commands: app.Commands{},
		Queries: app.Queries{
			// Initialize ListVideosHandler with the GCS repository
			ListVideos: query.NewListVideosHandler(videoRepo),
		},
	}
}
