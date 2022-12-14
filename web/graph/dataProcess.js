var lines = [];
var rows = [];
class Graph{
    getPieChart(describe){
      this.chart = new google.visualization.PieChart(document.getElementById(describe.id));
      this.data = google.visualization.arrayToDataTable(describe.data);
      this.options = {
        title: describe.title,
        width: describe.width,
        height: describe.height
      }
    }
    getBarChart(describe){
      this.chart = new google.visualization.BarChart(document.getElementById(describe.id));
      this.data = google.visualization.arrayToDataTable(describe.data);
      this.options = {
        title: describe.title,
        width: describe.width,
        height: describe.height
      }
    }
    getLineChart(describe){
      this.chart = new google.visualization.LineChart(document.getElementById(describe.id));
      this.data = google.visualization.arrayToDataTable(describe.data);
      this.options = {
        title: describe.title,
        width: describe.width,
        height: describe.height
      }
    }
    draw(){
      this.chart.draw(this.data, this.options)
    }
} 
let loadedText = false;
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(wait4load);//call the function when the google module is loaded

function preload() { //waits until the text file is loaded
    lines = loadStrings('datas.txt');
}

function setup() { //is called immediately before the preload() function
    noCanvas();
    process();
}
function process(){
    rows.push(['time', 'temp']);
    lines.forEach(line=>{
        if(line != ['']){
            let words = line.split(';');
            let day = words[0];
            let hour = words[1];
            let temp = parseFloat(words[2].replace(',', '.'));
            rows.push([day+' '+hour, temp]);
        }
    })
    loadedText = true;
}
function wait4load(){ //wait until the rows are loaded
    let waiting = setInterval(function(){
        if(loadedText == 1){
            clearInterval(waiting);
            main();
        }
    }, 1000);
}
function main(){
    let lineChart = new Graph();
    lineChart.getLineChart({
        // we make an object with chart specifications
          id: 'linechart',
          data: rows,
          title: 'Recordings of temperature',
          width: 1300,
          height: 500
        })
    lineChart.draw();
    //console.log(rows);
}
