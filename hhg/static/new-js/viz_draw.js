var timestep = 800;
var count = 0;

function random_vel(){
  return Math.random()*50.0 - 25.0;
}

var x_v = random_vel();
var y_v = random_vel();
var x = 49.0;
var y = 49.0;

function bounce(x,y){
  if(x+30.0>=339.0){
    x = 308.0;
    x_v *= -1.0;
  }else if(x-30.0<=15.0){
    x = 46.0;
    x_v *= -1.0;
  }
  if(y-30<=11.0){
    y = 41.0;
    y_v *= -0.9;
  }else if(y+30.0>=400.0){
    y = 370.0;
    count = 0;
    draw_text();
    if (y_v>190.0){
      y_v *= -0.95;
    }else if(y_v<=190.0 && y_v>=0.0){
      y_v *= -1.5;
    }
  }
}

function next_state(){
  y_v += 9.8;
  x += (timestep/300)*x_v;
  y += (timestep/300)*y_v;
}

function in_box(x,y){
  return (x> 11 && x < 339 && y-30 > 11 && y < 378);
}

function draw() {
  var canvas = document.getElementById("canvas");  
  var ctx = canvas.getContext("2d");
  ctx.globalCompositeOperation = 'destination-over';
  ctx.clearRect(11,11,337,399);
  ctx.save();
  ctx.strokeStyle = "#000";
  for(i=0;i<100;i++){
    ctx.moveTo(31+3*Math.random()*30*i,200);
    ctx.lineTo(31+3*i,200-Math.random()*60);
  }
  ctx.stroke();
  ctx.restore();
  setTimeout('draw()', timestep);
}

function draw2() {  
  var canvas = document.getElementById("slide_canvas"); 
  var ctx = canvas.getContext("2d");
  var b = 4+Math.random()*3;
  ctx.globalCompositeOperation = 'destination-over';
  ctx.fillStyle = "#000";
  ctx.clearRect(0,0,337,399);
  ctx.save();
  ctx.beginPath();
  ctx.strokeStyle = "#" + Math.floor(Math.random()*800).toString();
  for(i=0;i<61;i++){
    ctx.strokeWidth = "1pt";
    ctx.moveTo(11+4*i,80);
    var x = 80-Math.abs(Math.sin(i*b*10))*50;
    if (x>80){x=80;}
    ctx.lineTo(11+4*i,x);
    ctx.stroke();
  }
  ctx.restore();
  var r2 = r2+5;
  var g2 = g2+5;
  var b2 = b2+5;
 	 setTimeout('draw2()', timestep);
}

function path_rect(ctx,x1,y1,x2,y2){
  ctx.moveTo(x1,y1);
  ctx.lineTo(x1,y2);
  ctx.moveTo(x1,y1);
  ctx.lineTo(x2,y1);
  ctx.moveTo(x2,y2);
  ctx.lineTo(x2,y1);
  ctx.moveTo(x2,y2);
  ctx.lineTo(x1,y2);
}

function fnOnClick(e){
  var ax;
  var ay;
  if (e.pageX != undefined && e.pageY != undefined) {
    ax = e.pageX;
    ay = e.pageY;
  }
  ax -= canvas.offsetLeft;
  ay -= canvas.offsetTop;
  if(Math.abs(ax-x)<30 && Math.abs(ay-y)<30 && y_v>0){
    y_v =-140;
    x_v = -(ax-x);
    count += 1;
    draw_text();
  }
}

function draw_viz() { 
  setTimeout('draw2()',500); 
}

draw_viz();
