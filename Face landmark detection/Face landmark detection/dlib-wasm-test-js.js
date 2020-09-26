const webcamVideo = document.getElementById("webcam-video");

const inputCanvas = document.getElementById("input-canvas");
inputCanvas.width = 640;
inputCanvas.height = 480;

const overlayCanvas = document.getElementById("overlay-canvas");
overlayCanvas.width = 640;
overlayCanvas.height = 480;

const inputCanvasCtx = inputCanvas.getContext("2d");
const overlayCanvasCtx = overlayCanvas.getContext("2d");

const donnyBaseball = document.getElementById("donny-baseball");

function mainLoop() {
	inputCanvasCtx.drawImage(webcamVideo, 0, 0, 640, 480);

	const inputImgData = inputCanvasCtx.getImageData(0, 0, 640, 480);
	const inputBufImg = Module._malloc(inputImgData.data.length);
	
	Module.HEAP8.set(inputImgData.data, inputBufImg);

	const ptr = Module.ccall("detect", "number", "number", [inputBufImg]) / Uint16Array.BYTES_PER_ELEMENT;
	
	const len = Module.HEAPU16[ptr];
	const landmarks = [];
	for (let i = 1; i < len; i += 2) {
		const l = [Module.HEAPU16[ptr + i], Module.HEAPU16[ptr + i + 1]];
		landmarks.push(l);
	}

	overlayCanvasCtx.clearRect(0, 0, 640, 480);

	overlayCanvasCtx.fillStyle = "rgb(130, 255, 50)";
	overlayCanvasCtx.font = "6px Arial";

	for (let i = 1; i < landmarks.length; i += 1) {
		overlayCanvasCtx.fillText(i, landmarks[i][0], landmarks[i][1]);
	}
	
	Module._free(ptr);
	Module._free(inputBufImg);

	requestAnimationFrame(mainLoop);
}

window.onload = () => {
	navigator.mediaDevices.getUserMedia({video: true}).then(stream => {
		webcamVideo.srcObject = stream;
		webcamVideo.style.display = "none";
	}).catch(err => {
		alert(err);
	});


	console.log("Detecting in 2 seconds...");

	setTimeout(() => {
		const req = new XMLHttpRequest();
		req.open("GET", "/shape_predictor_68_face_landmarks.dat", true);
		req.responseType = "arraybuffer";

		req.onload = (e) => {
			const payload = req.response;

			if (payload) {
				const model = new Uint8Array(payload);
					
				const inputBufModel = Module._malloc(model.length);
				Module.HEAPU8.set(model, inputBufModel);
				Module.ccall("init_shape_predictor", null, ["number", "number"], [inputBufModel, model.length]);
				
				requestAnimationFrame(mainLoop);
			}
		}

		req.send(null);
	}, 2000);
}