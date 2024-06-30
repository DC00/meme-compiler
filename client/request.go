package client

type AddVideoRequest struct {
	URL string `json:"url"`
	Webhook string `json:"webhook,omitempty"`
}

type CreateCompilationRequest struct {
	Webhook string `json:"webhook,omitempty"`
}
