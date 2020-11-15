document.addEventListener('DOMContentLoaded', () => {
    var socket = io();
    socket.on('connect', function() {
    setInterval(function(){  socket.emit('predictionData', {data: [mobilePrediction, personPrediction, Date.now()]});}, 500);
});
});