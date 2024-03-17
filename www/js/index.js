/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * 'License'); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
let intervalId = null;
let dataHistory = [];

document.getElementById('fontSizeList').addEventListener('change', changeSize, false);
document.getElementById('roomList').addEventListener('change', changeRoom, false);

function changeSize() {
    let fontSize = document.getElementById('fontSizeList').value;
    if (fontSize == '') return;

    document.getElementById('closedCaptions').style.fontSize = fontSize;
}

function changeRoom() {
    let roomSelection = document.getElementById('roomList').value;

    startClosedCaptioning(roomSelection);
}

function getClosedCaptions(roomSelection) {
    roomSelection = roomSelection.replace(/ /g, '-').toLowerCase();
    let url = '/room/' + roomSelection + '/latest';
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            data = JSON.parse(request.responseText);
            if (data.text != dataHistory[dataHistory.length-1]) {
                dataHistory.push(data.text);
            }

            if (dataHistory.length > 5) {
                dataHistory.shift();
            }
            
            drawCaptions();
        }
        else {
            document.getElementById('closedCaptions').innerHTML = 'An error occured.';
        }
    };
    request.send();
}

function drawCaptions() {
    for (let i = 0; i < dataHistory.length; i++) {
        dataText = dataHistory[i];

        // highlight last element
        if (i == dataHistory.length - 1) {
            dataText = '<b>' + dataText + '</b>';
        }
        document.getElementById('closedCaptions').innerHTML = dataText;
        document.getElementById('closedCaptions').innerHTML += '<br>';
    }
}

function startClosedCaptioning(roomSelection) {
    if (intervalId != null) {
        clearInterval(intervalId);
        intervalId = null;
    }

    if (roomSelection == '') return;

    getClosedCaptions(roomSelection);
    intervalId = setInterval(getClosedCaptions.bind(undefined,roomSelection), 3000);
}