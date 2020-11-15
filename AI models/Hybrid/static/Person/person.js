let personnet;
const webcam2 = new Webcam(document.getElementById('wc'));
let isPredicting2 = false;
var personPrediction = 'Single person';

async function loadPersonnet() {
    const personnet = await tf.loadLayersModel('http://127.0.0.1:5000/Person/model2.json');
    console.log("Model loaded 2");
    return personnet;
}

async function predict2() {
    console.log("predict person method");
  while (isPredicting2) {
    const predictedClass = tf.tidy(() => {
      const img = webcam2.capture();
      const prediction = personnet.predict(img);
      return prediction.as1D().argMax();
    });
    const classId = (await predictedClass.data())[0];
    var predictionText2 = "";
    switch(classId){
		case 1:
			predictionText2 = "Single person";
			personPrediction = predictionText2;
			break;
		case 0:
			predictionText2 = "Multiple person";
			personPrediction = predictionText2;
//			window.location.replace("complaint/id=".concat("stud1"))
			break;
	}
	document.getElementById("prediction2").innerText = predictionText2;
    predictedClass.dispose();
    await tf.nextFrame();
  }
}

function startPredicting2(){
	isPredicting2 = true;
	predict2();
}

function stopPredicting2(){
	isPredicting2 = false;
	predict2();
}

async function init(){
	await webcam2.setup();
	personnet = await loadPersonnet();
	tf.tidy(() => personnet.predict(webcam2.capture()));	
}

init();
