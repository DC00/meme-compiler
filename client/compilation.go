package client

import (
	"context"
	"net/http"
)

type CompilationService struct {
	client *Client
}

func (s *CompilationService) Create(ctx context.Context, req *CreateCompilationRequest) (*Response, error) {
	return s.client.doRequest(ctx, http.MethodPost, "/api/compilations/v1/create", req)
}
