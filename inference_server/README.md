# Inference server
## Dependencies
Library dependencies for the python code.  You need to install these with
`pip install -r requirements.txt` before you can run this.
## How to run it
### Download model
The model to perform document classification has been hosted in Google Drive. You can download it from: https://drive.google.com/file/d/1wJUnkFiqmwok1gJ2sKHPvJIaNjfT4pk6/view?usp=sharing
Please, move the downloaded file **model.hdf5** to the **inference_server** folder.
### Environment variables
Set the following environment variables:

| Parameter         | Environment Variable | Default Value           |
|-------------------|----------------------|-------------------------|
| number of workers | MODEL_SERVER_WORKERS | the number of CPU cores |
| timeout           | MODEL_SERVER_TIMEOUT | 120 seconds             |
| nginx config path | NGINX_CONF_PATH      | /etc/nginx/nginx.conf   |

Example:
```bash
export MODEL_SERVER_WORKERS=1
export MODEL_SERVER_TIMEOUT=120
export NGINX_CONF_PATH=/home/user/UiPath_Document_Classification/inference_server/nginx.conf
```
### Run the inference server
By default, this server uses the port 1234. Run it with the following command:
```bash
sudo -E ./serve
```
### Time to try it!
Send a file to the server using curl:
```bash
curl -X POST -F "file=@PATH_TO_YOUR_FILE" "http://localhost:1234/document_classification"
```
Result:
```json
{
    "prediction": {
        "confidence": "1.0",
        "class": "invoice"
    },
    "confidences": {
        "invoice": "1.000",
        "passport": "0.000",
        "id_card_2": "0.000",
        "driving_licence": "0.000",
        "id_card_3": "0.000"
    }
}
```
