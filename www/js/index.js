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
var roomSelection = '';

document.getElementById('fontSizeList').addEventListener('change', changeSize, false);
document.getElementById('roomList').addEventListener('change', changeRoom, false);

function changeSize() {
    var fontSize = document.getElementById('fontSizeList').value;
    if (fontSize == '') return;

    document.getElementById('closedCaptions').style.fontSize = fontSize;
}

function changeRoom() {
    roomSelection = document.getElementById('roomList').value;
    if (roomSelection == '') return;

    getClosedCaptions();
}

function getClosedCaptions() {
    var url = 'https://RESTAPI.com/data/' + roomSelection + '/texttospeech';
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            document.getElementById('closedCaptions').innerHTML = data.text;
        }
    };
    request.send();
}