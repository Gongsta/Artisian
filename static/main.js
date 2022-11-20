var canvas, ctx, flag = false,
		prevX = 0,
		currX = 0,
		prevY = 0,
		currY = 0,
		dot_flag = false;

var x = "black",
		y = 2;

// Advanced options (sliders)
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
	coll[i].addEventListener("click", function() {
		this.classList.toggle("active");
		var content = this.nextElementSibling;
		if (content.style.maxHeight){
		content.style.maxHeight = null;
		} else {
		content.style.maxHeight = content.scrollHeight + "px";
		}
	});
}
let thickness = 1

function init() {
		canvas = document.getElementById('can');
		ctx = canvas.getContext("2d");
		w = canvas.width;
		h = canvas.height;

		canvas.addEventListener("mousemove", function (e) {
				findxy('move', e, thickness)
		}, false);
		canvas.addEventListener("mousedown", function (e) {
				findxy('down', e, thickness)
		}, false);
		canvas.addEventListener("mouseup", function (e) {
				findxy('up', e, thickness)
		}, false);
		canvas.addEventListener("mouseout", function (e) {
				findxy('out', e, thickness)
		}, false);
}

function color(obj) {
		x = obj.id;
		if (x == "white") y = 14;
		else y = 2;

}

function draw(thickness) {
		ctx.beginPath();
		ctx.moveTo(prevX, prevY);
		ctx.lineTo(currX, currY);
		ctx.strokeStyle = x;
		ctx.lineWidth = y * thickness;
		ctx.stroke();
		ctx.closePath();
}

function erase() {
	ctx.clearRect(0, 0, w, h);
}

function save() {
		console.log("trying to save");
  	modal.style.display = "block";
		modal.appendChild(document.getElementById('modal-content-id'))
		var dataURL = canvas.toDataURL();
		$.ajax({
			type: "POST",
			url: "hook",
			data:{
				imageBase64: dataURL,
				prompt: document.getElementById('prompt_box').value,
				strength: 0.75,
				guidance_scale: 7.5,
				// strength: document.getElementById('strength').value,
				// guidance_scale: document.getElementById('guidance_scale').value,
			}
		}).done(function() {
			window.open("/new_image");
  		modal.style.display = "none";
		});
}

function findxy(res, e, thickness) {
		if (res == 'down') {
				prevX = currX;
				prevY = currY;
				currX = e.clientX - canvas.offsetLeft;
				currY = e.clientY - canvas.offsetTop;

				flag = true;
				dot_flag = true;
				if (dot_flag) {
						console.log('test')
						ctx.beginPath();
						ctx.fillStyle = x;
						ctx.fillRect(currX, currY, 2, 2);
						ctx.closePath();
						dot_flag = false;
				}
		}
		if (res == 'up' || res == "out") {
				flag = false;
		}
		if (res == 'move') {
				if (flag) {
						prevX = currX;
						prevY = currY;
						currX = e.clientX - canvas.offsetLeft;
						currY = e.clientY - canvas.offsetTop;
						draw(thickness);
				}
		}
}



// MODAL LOGIC
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var clear = document.getElementById("clear");

var thick_btn1 = document.getElementById("thickness1");
var thick_btn2 = document.getElementById("thickness2");
var thick_btn3 = document.getElementById("thickness3");

thick_btn1.addEventListener("click", () => {
	thickness = 1
})

thick_btn2.addEventListener("click", () => {
	thickness = 3
})

thick_btn3.addEventListener("click", () => {
	thickness = 5
})

//when the user clicks clear button
clear.addEventListener("click", () => {
	erase();
})

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}