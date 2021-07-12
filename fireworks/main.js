var fireworks = []
var gravity

function setup(){
	createCanvas(window.innerWidth, window.innerHeight)
	gravity = createVector(0, .2)
	stroke(255)
	strokeWeight(4)
	fireworks.push(new Firework())
	background(0, 0, 0)
	textSize(64)
}

function draw(){
	colorMode(RGB)
	fill('red')
	background(0, 0, 0, 25)
	t = 'Happy Birthday :3'
	text(t, width/2-textWidth(t)/2, 100)

	if (random(1) < .03 || fireworks.length < 2) {
		fireworks.push(new Firework())
	}
	for (var i = fireworks.length - 1; i >= 0; i--){
		fireworks[i].update()
		fireworks[i].show()

		if (fireworks[i].done()){
			fireworks.splice(i, 1)
		}

	}
}
