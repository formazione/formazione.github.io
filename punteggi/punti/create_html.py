template = """
<td>
<!-- Buttons [+] [-] -->
<button type="button" class="btn btn-warning btn-lg" onclick="dbRef1.set(--n1)"> - </button>
<button type="button" class="btn btn-info btn-lg" onclick="dbRef1.set(++n1)"> + </button>
<!-- name -->
Maiuri<td>
<!-- here goes the score -->
<i id="h1alunno1"></i>
</p><script>
// where you write the score
var h1alunno1 = document.getElementById("h1alunno1");
// get the reference to where the score is saved in the db
var dbRef1 = firebase.database().ref().child("5ce_2020").child("Maiuri");
// get the value and put it into where the score goes
// This displays the value
dbRef1.on("value", snap => h1alunno1.innerText = snap.val());
// This lets update the value
bdbRef1.on("value", snap => n1 = snap.val())
<script>
"""

names = "Maiuri Battagliese Borrelli Carracino Ciardi Donianni Fluri Liguori Maiese Mautone Merola Palladino Ricci Saja_A Saja_P Tierno"
names = names.split(" ");

html = """
<div id="div1" class="w3-main" style="margin-left:50px">
<table class="table-bordered">
<script type="text/javascript">
"""

for n, name in enumerate(names):
	temp = template
	html += temp.replace("Maiuri", name).replace("n1", "n" + str(n)).replace("h1alunno1", "h1alunno" + str(n));
	html += "<tr>"
	print(html);