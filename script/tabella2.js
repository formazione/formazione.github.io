    <script>
    function createTable(objectArray, fields, fieldTitles) {
      let body = document.getElementsByTagName('body')[0];
      let tbl = document.createElement('table');
      let thead = document.createElement('thead');
      let thr = document.createElement('tr');

      for (p in objectArray[0]){
        let th = document.createElement('th');
        th.appendChild(document.createTextNode(p));
        thr.appendChild(th);
        
      }
     
      thead.appendChild(thr);
      tbl.appendChild(thead);

      let tbdy = document.createElement('tbody');
      let tr = document.createElement('tr');
      objectArray.forEach((object) => {
        let n = 0;
        let tr = document.createElement('tr');
        for (p in objectArray[0]){
          var td = document.createElement('td');
          td.appendChild(document.createTextNode(object[p]));
          tr.appendChild(td);
          n++;
        };
        tbdy.appendChild(tr);    
      });
      tbl.appendChild(tbdy);
      body.appendChild(tbl)
      return tbl;
    }

// output of the example
// name    price
// Banana  3.04
// Orange  2.56
// Apple   1.45

  
dati = `
Banana 3.04
Orange 2.56
Apple 1.45
`.split("\n");
  
  
    createTable([
                  {name: 'Banana', price: '3.04'},
                  {name: 'Orange', price: '2.56'},
                  {name: 'Apple', price: '1.45'}
               ])
    </script>