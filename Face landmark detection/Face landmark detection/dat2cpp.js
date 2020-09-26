const fs = require("fs");

fs.readFile("shape_predictor_68_face_landmarks.dat", (err, data) => {
	if (err) {
		throw err;
	}

	for (let i = 0; i < data.length; i += 1) {
		console.log(data[i]);
	}
});