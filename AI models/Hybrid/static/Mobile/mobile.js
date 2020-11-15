let mobilenet;
const webcam = new Webcam(document.getElementById('wc'));
let isPredicting = false;
var mobilePrediction = 'Everything alright';

async function loadMobilenet() {
    console.log("Model function STEP 2");
    const mobilenet = await tf.loadLayersModel('http://127.0.0.1:5000/Mobile/model.json');
    console.log("Model loaded");
    return mobilenet;
}

async function predict() {
    console.log("predict mobile method");
  while (isPredicting) {
    const predictedClass = tf.tidy(() => {
      const img = webcam.capture();
      const prediction = mobilenet.predict(img);
      return prediction.as1D().argMax();
    });
    const classId = (await predictedClass.data())[0];
    var predictionText = "";
    switch(classId){
		case 0:
			predictionText = "Not present";
			mobilePrediction = predictionText;
			break;
		case 1:
			predictionText = "MOBILE detected";
			mobilePrediction = predictionText;
			break;
	}

	document.getElementById("prediction1").innerText = predictionText;
    
    predictedClass.dispose();
    await tf.nextFrame();
  }
}

function startPredicting(){
	isPredicting = true;
	predict();
}

function stopPredicting(){
	isPredicting = false;
	predict();
}

async function init(){
	await webcam.setup();
    console.log("STEP 1 SUCCESS");
	mobilenet = await loadMobilenet();
	tf.tidy(() => mobilenet.predict(webcam.capture()));	
}

init();
