

const csvUrl = "https://raw.githubusercontent.com/esteban-data-enthusiast/CUNY_DATA_608/master/module5/data/presidents.csv";

let parsedCSV;

function tabulateCSV() {

  d3.text(csvUrl, function(data) {
    
    parsedCSV = d3.csv.parseRows(data);

    //var container = d3.select("body")
    var container = d3.select("#question3")
        .append("table")

        .selectAll("tr")
            .data(parsedCSV).enter()
            .append("tr")

        .selectAll("td")
            .data(function(d) { return d; }).enter()
            .append("td")
            .text(function(d) { return d; });
  });

}


function getPresidentData() {

  table = document.getElementById("searchResult");
  table.rows[1].cells[0].innerText = "";
  table.rows[1].cells[1].innerText = "";
  table.rows[1].cells[2].innerText = "";

  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("NameInput");
  filter = input.value.toUpperCase();
  //console.log(filter);

  for (i = 0; i < parsedCSV.length; i++) {

    if (parsedCSV[i][0].toUpperCase() === filter) {

      table.rows[1].cells[0].innerText = parsedCSV[i][0];
      table.rows[1].cells[1].innerText = parsedCSV[i][1];
      table.rows[1].cells[2].innerText = parsedCSV[i][2];

    }
  
  }
}
        


tabulateCSV();




