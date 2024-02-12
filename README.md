# Scale Closed Captioning

Scale Closed Captioning is a mobile application built using Apache Cordova and Bootstrap. It provides a convenient way to display closed captions on browsers or mobile devices. This application is designed to enhance accessibility for individuals with hearing impairments by providing real-time captioning for various media content.

## Installation

1. Install [Node.js](https://nodejs.org/en/download/)
2. Install Cordova: `npm install -g cordova`
3. Clone this repository: `git clone https://github.com/Secret-Asian-Man/ScaleCC_Cordova.git`
4. Navigate into the project directory: `cd scale-av-cc-cordova`
5. Add the platform: `cordova platform add browser`
6. Install dependencies: `npm install`

7. Create virtual environment: `python3 -m venv venv`  
8. Start virtual environment: `source ./venv/bin/activate`
9. Install requirements: `pip install -r requirements.txt`

## Usage

1. Start virtual environment: `source ./venv/bin/activate`
2. Start application: `flask --app scale_av_cc.app run`
3. Open a browser and navigate to `http://localhost:5000`

## Testing

1. On a separate terminal, start virtual environment: `source ./venv/bin/activate`
2. Run test application: `python -m scale_av_cc.testZmq`
3. In the browser, navigate to `http://localhost:5000` and select a room.
4. In the terminal input selected room, replacing spaces with _underscores (i.e. `ballroom_a`), then input test message.

## License

[MIT](https://choosealicense.com/licenses/mit/)