package queue

import (
	"context"
	"fmt"

	cloudtasks "cloud.google.com/go/cloudtasks/apiv2"
	taskspb "cloud.google.com/go/cloudtasks/apiv2/cloudtaskspb"
)

const (
	serviceAccountEmail = "meme-compiler@meme-compiler.iam.gserviceaccount.com"
)

type CloudTasksClient struct {
	client    *cloudtasks.Client
	projectID string
	location  string
	queue     string
}

func NewCloudTasksClient(projectID, location, queue string) (*CloudTasksClient, error) {
	ctx := context.Background()
	client, err := cloudtasks.NewClient(ctx)
	if err != nil {
		return nil, err
	}

	return &CloudTasksClient{
		client:    client,
		projectID: projectID,
		location:  location,
		queue:     queue,
	}, nil
}

func (c *CloudTasksClient) CreateTask(ctx context.Context, url string, payload []byte) error {
	parent := fmt.Sprintf("projects/%s/locations/%s/queues/%s", c.projectID, c.location, c.queue)
	req := &taskspb.CreateTaskRequest{
		Parent: parent,
		Task: &taskspb.Task{
			MessageType: &taskspb.Task_HttpRequest{
				HttpRequest: &taskspb.HttpRequest{
					HttpMethod: taskspb.HttpMethod_POST,
					Url:        url,
					Body:       payload,
					Headers: map[string]string{
						"Content-Type": "application/json",
					},
					AuthorizationHeader: &taskspb.HttpRequest_OidcToken{
						OidcToken: &taskspb.OidcToken{
							ServiceAccountEmail: serviceAccountEmail,
							Audience:            url,
						},
					},
				},
			},
		},
	}

	_, err := c.client.CreateTask(ctx, req)
	return err
}
