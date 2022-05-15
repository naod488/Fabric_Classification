var http = require('http'),
	express = require('express'),
    path = require('path'),
    fs = require('fs'),
	formidable = require('formidable');
	

const {spawn} = require('child_process');

var app = express();

app.use(express.static("public"));

app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, 'public/form.html'));
});

app.post('/fileupload', function(req, res) {
    var form = new formidable.IncomingForm();
	
	form.parse(req, function (err, fields, files) {
		var oldpath = files.filetoupload.filepath;
		filename = files.filetoupload.originalFilename;
		newpath = path.join(__dirname, 'images/' + filename);
			
		fs.rename(oldpath, newpath, function (err) {
			if (err) throw err;
			res.write('<h1>File uploaded!</h1>');
			res.write('<h2><a href="/py/?imagename='+filename+'">Evaluate</a></h2>');
			res.end();
		});
	});
});

app.get('/py', function(req, res) {
    var dataToSend;
	var imageName = req.query.imagename;
	imageName = 'images/' + imageName
	console.log(imageName);
	
	// spawn a child process to call the python script
	const python = spawn('python', ['fabric_app.py ', imageName]);
	
	// output from python file
	python.stdout.on('data', function (data) {
		console.log('Pipe data from python script ...');
		dataToSend = data.toString();
		console.log(dataToSend);
	});
		
	// when the python script finished execution
	python.on('close', (code) => {
		console.log('child process close all stdio with code ${code}');
		// send the html response
		res.write(dataToSend);
		res.end();
	});
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;
	console.log(host);
    console.log('Example app listening at http://%s:%s', host, port);
});