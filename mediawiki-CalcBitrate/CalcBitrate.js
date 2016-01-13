function calculate(){
var size = parseInt(window.document.bitrate.size.value);
var h = parseInt(window.document.bitrate.hour.value);
var min = parseInt(window.document.bitrate.minute.value);
var sec = parseInt(window.document.bitrate.seconde.value);
var audio1 = parseInt(window.document.bitrate.audio1.value);
var audio2 = parseInt(window.document.bitrate.audio2.value);
var audio3 = parseInt(window.document.bitrate.audio3.value);
var audio4 = parseInt(window.document.bitrate.audio4.value);
var audio = audio1 + audio2 + audio3 + audio4;
var subtitle = parseInt(window.document.bitrate.subtitle.value) * 2;
var duration = (h*3600)+(min*60)+sec;
var bitrate = Math.round(((size-audio-subtitle)  * Math.pow(2, 23) * Math.pow(10, -3)) / duration);
window.document.bitrate.answer.value=bitrate;
}
