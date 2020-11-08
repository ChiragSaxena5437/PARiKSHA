let mobilenet;
let model;
const webcam = new Webcam(document.getElementById('wc'));
let isPredicting = false;

async function loadMobilenet() {
    const mobilenet = await tf.loadLayersModel('http://127.0.0.1:5000/model.json');
//  const outputl = mobilenet.getOutputAt('sequential_19');
    return mobilenet;
//  return tf.model({inputs: mobilenet.inputs, outputs: outputl.output});
}

async function predict() {
  while (isPredicting) {
    const predictedClass = tf.tidy(() => {
      const img = webcam.capture();
      const prediction = mobilenet.predict(img);
//      const predictions = model.predict(activation);
      return prediction.as1D().argMax();
    });
    const classId = (await predictedClass.data())[0];
    var predictionText = "";
    switch(classId){
		case 0:
			predictionText = "I SEE";
			break;
		case 1:
			predictionText = "I see MOBILE";
			break;
	}
	document.getElementById("prediction").innerText = predictionText;
			
    
    predictedClass.dispose();
    await tf.nextFrame();
  }
}

function startPredicting(){
    window.alert("Called");
	isPredicting = true;
	predict();
}

function stopPredicting(){
	isPredicting = false;
	predict();
}

async function init(){
	await webcam.setup();
	mobilenet = await loadMobilenet();
	tf.tidy(() => mobilenet.predict(webcam.capture()));
		
}

init();
