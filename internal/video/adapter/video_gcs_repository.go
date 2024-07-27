package adapter

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"cloud.google.com/go/storage"
	"google.golang.org/api/iterator"

	"github.com/DC00/meme-compiler/internal/video/domain/video"
)

type GcsVideoRepository struct {
	client *storage.Client
	bucket string
}

func NewGcsVideoRepository() *GcsVideoRepository {
	ctx := context.Background()
	client, err := storage.NewClient(ctx)
	if err != nil {
		log.Printf("Failed to create GCS client: %v", err)
	}

	return &GcsVideoRepository{
		client: client,
		bucket: os.Getenv("DOWNLOAD_BUCKET"),
	}
}

// ListVideos implements the ListVideosReadModel interface
func (r *GcsVideoRepository) ListVideos(ctx context.Context) ([]*video.Video, error) {
	defer r.client.Close()
	ctx, cancel := context.WithTimeout(ctx, time.Second*10)
	defer cancel()

	videos := []*video.Video{}

	it := r.client.Bucket(r.bucket).Objects(ctx, nil)
	for {
		attrs, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("Bucket(%q).Objects: %w", r.bucket, err)
		}
		v := &video.Video{
			Url: attrs.Name,
		}

		videos = append(videos, v)

	}
	return videos, nil
}
