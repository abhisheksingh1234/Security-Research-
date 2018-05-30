var esprima = require('esprima');
var args = process.argv.slice(2);

var fs = require('fs');
var fileContents;
fs.readFile(args[0], function (err, data) {
    if (err) throw err;
    fileContents = data;
    console.log(JSON.stringify(esprima.parse(fileContents), null, 4));
});

