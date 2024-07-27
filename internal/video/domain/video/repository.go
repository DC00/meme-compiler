package video

import (
	"context"
)

type Repository interface {
	ListVideos(ctx context.Context) (*Video, error)
}
