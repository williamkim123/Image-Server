# sample commands for running the application:
Start server
```sh
python image_server.py --host 'localhost' --port '50051'
```

Send request from client
```sh
python image_client.py --host 'localhost' --port '50051' --input 'sample-image.png' --output 'processed-sample-image.png' --rotate 'TWO_SEVENTY_DEG' --mean
```