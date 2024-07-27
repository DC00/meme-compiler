package video

type Video struct {
	Url string
}

func NewVideo(url string) *Video {
	return &Video{
		Url: url,
	}
}
