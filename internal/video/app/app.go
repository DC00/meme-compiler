package app

import (
	"github.com/DC00/meme-compiler/internal/video/app/query"
)

type Application struct {
	Commands Commands
	Queries  Queries
}

type Commands struct {
}

type Queries struct {
	ListVideos query.ListVideosHandler
}
