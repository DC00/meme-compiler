package main

import (
	"context"
	"net/http"

	"github.com/DC00/meme-compiler/internal/common/server"
	"github.com/DC00/meme-compiler/internal/video/port"
	"github.com/DC00/meme-compiler/internal/video/service"
	"github.com/go-chi/chi/v5"
)

func main() {
	ctx := context.Background()

	application := service.NewApplication(ctx)

	server.RunHTTPServer(func(router chi.Router) http.Handler {
		return port.HandlerFromMux(
			port.NewHttpServer(application),
			router,
		)
	})
}
