# detectImage-linebot-service
Line Message API + API Gateway + Lambda + Google Cloud Vision API in Serverless Framework

## Description

detectImage-linebot-service is line bot service that detect image.


## Requirement

- serverless 1.4
- python 2.7
- AWS Account
- LINE@ Account
- Google Account

## Installation

### Clone

```bash
$ git clone https://github.com/tsuyopooon/detectImage-linebot-service.git ./detectImage-linebot-service
$ cd detectImage-linebot-service
```

### Set Environment

Set your own authentication information

```bash
$ cat ~/.aws/config
[profile default]
region = XXX
output = json

$ cat ~/.aws/credentials
[default]
aws_secret_access_key = XXX
aws_access_key_id = XXX

$ cat env-dev.yml
LINE_CHANNEL_SECRET: "XXX"
LINE_CHANNEL_ACCESS_TOKEN: "XXX"
GOOGLE_APPLICATION_CREDENTIALS: "{file path for download service account key}"
MICROSOFT_COMPUTER_VISION_KEY: "XXX"
DETECT_IMAGE_API: "cloud_vision"
```

### Deploy

```bash
$ serverless deploy
```

### Set Callback URL

Set "API Gateway Endpoints" to webhook url for LINE developer.

## Qiita

[Serverless Frameworkを試してみる(Line Message API + API Gateway + Lambda + Google Cloud Vision API編)](http://qiita.com/tsuyopooon/items/b595af42da906adb36fd)

## Author

[@tsuyopooon](https://github.com/tsuyopooon)

## License

[MIT](https://github.com/tsuyopooon/detectImage-linebot-service/blob/master/LICENSE)