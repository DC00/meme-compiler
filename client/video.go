package client

import (
	"context"
	"net/http"
)

type VideoService struct {
	client *Client
}

func (s *VideoService) Add(ctx context.Context, req *AddVideoRequest) (*Response, error) {
	return s.client.doRequest(ctx, http.MethodPost, "/api/videos/v1/add", req)
}
