package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	defaultBaseURL = "https://mc-api-b473pkndcq-uk.a.run.app"
	defaultTimeout = 10 * time.Second
)

type Client struct {
	baseURL    string
	httpClient *http.Client
	token      string

	Videos       *VideoService
	Compilations *CompilationService
}

type ClientOption func(*Client)

func NewClient(token string, options ...ClientOption) *Client {
	c := &Client{
		baseURL: defaultBaseURL,
		httpClient: &http.Client{
			Timeout: defaultTimeout,
		},
		token: token,
	}

	for _, option := range options {
		option(c)
	}

	c.Videos = &VideoService{client: c}
	c.Compilations = &CompilationService{client: c}

	return c
}

func WithBaseURL(url string) ClientOption {
	return func(c *Client) {
		c.baseURL = url
	}
}

func WithHTTPClient(httpClient *http.Client) ClientOption {
	return func(c *Client) {
		c.httpClient = httpClient
	}
}

func (c *Client) doRequest(ctx context.Context, method, path string, body interface{}) (*Response, error) {
	url := c.baseURL + path

	var buf io.ReadWriter
	if body != nil {
		buf = new(bytes.Buffer)
		err := json.NewEncoder(buf).Encode(body)
		if err != nil {
			return &Response{Message: "Encoding request body failed"}, fmt.Errorf("encoding request body: %w", err)
		}
	}

	req, err := http.NewRequestWithContext(ctx, method, url, buf)
	if err != nil {
		return &Response{Message: "Creating request failed"}, fmt.Errorf("creating request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.token)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return &Response{Message: "Making request failed"}, fmt.Errorf("making request: %w", err)
	}
	defer resp.Body.Close()

	var response Response
	err = json.NewDecoder(resp.Body).Decode(&response)
	if err != nil {
		return &Response{Message: "Decoding response failed"}, fmt.Errorf("decoding response: %w", err)
	}

	if resp.StatusCode != http.StatusCreated {
		return &response, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	return &response, nil
}
