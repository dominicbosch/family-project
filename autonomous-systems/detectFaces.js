
let cv = require('opencv');

let spawn = require('child_process').spawn;


let args = [
	'-w', '2592',
	'-h', '1952',
	'-q', '85', // JPEG quality in %
	'-o', 'test.jpg',
	'-tl', '200', // every 200 ms
	'-t', '99999999', // run time
	'-th', '0:0:0', // no thumbnails?
];

// let procStills = spawn('raspistill', args);
let j = 0
function readImage() {
	let start = (new Date()).getTime();
	cv.readImage('test.jpg', function(err, im) {
		console.log('Reading took '+((new Date()).getTime()-start))
		
		im.detectObject(cv.FACE_CASCADE, {}, function(err, faces) {
			console.log(err, faces);
			for (var i=0;i<faces.length; i++){
				var x = faces[i];
				im.ellipse(x.x + x.width/2, x.y + x.height/2, x.width/2, x.height/2);
			}
			im.save('./out_'+(j++)+'.jpg');
			console.log('Detection took '+((new Date()).getTime()-start));
			readImage();
		});
	})
}
readImage();