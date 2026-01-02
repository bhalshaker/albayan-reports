```sh
curl -X POST http://localhost:3000/reports \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/home/devnation/Documents/test.odt" \
  -F "template_file_type=odf"
```

```sh
curl -X POST http://localhost:3000/reports \
  -F "template_file_type=odf"
```

```sh
curl -X GET http://localhost:3000/reports
```

```sh
curl -X GET http://localhost:3000/reports/1cf2fce8-a98a-4d8e-8171-e21c633f4114
```

```sh
curl -X PATCH http://localhost:3000/reports/1cf2fce8-a98a-4d8e-8171-e21c633f4114 \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/home/devnation/Documents/test.odt" \
  -F "template_file_type=odf"
```

```sh
curl -X DELETE http://localhost:3000/reports/1cf2fce8-a98a-4d8e-8171-e21c633f4114
```

> Tip: The API also accepts a JSON string in a `body` form field (e.g. `-F 'body={"template_file_type":"odf"}'`) — the server will parse it automatically.
