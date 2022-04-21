# DL4media-ticker-extractor

**To run** download everything from the latest release, then start the docker with "docker compose up --build". The server accepts text and then returns images for the passed text.

# Use

Curl example:

curl -X POST \
  http://localhost:4000/extract-ticker \
  -H 'authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDc3MjU0NTYsImlhdCI6MTY0NzcyNTQ1Niwic3ViIjoiNjEzNjFlNDdhNGVjYTA5ZTQ2MzI2YWYyIn0.58m7G5MDAS_V3jS_wklsNqYabsr6NK3KHeYvus6VJi4' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: fe3ee7f4-b70b-414f-cb42-4fd07fc486aa' \
  -F 'file=<path_to_video_dir>\Video.mp4'
