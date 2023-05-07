from AcessPoint import AcessPoint
# Flexbox
# https://css-tricks.com/snippets/css/a-guide-to-flexbox/
# HTML + Flexbox + CSS
# https://www.w3schools.com/css/tryit.asp?filename=trycss3_flexbox_flex-wrap_nowrap8
header = """<html>
			<title>Check AP's</title>
		""" 

def _style():
	return """<head>
			<style>
.title2{
text-align: center;
font-size: 30px;
  font-weight: bold;
   margin-top: 30px;
  margin-bottom: 30px;
}
section {
  display: table;
   margin: 25px 50px 75px 50px;
  width: 100%;
  border-style: solid;
}
.MiTable {
 margin: auto;
  width: 60%;
}
section > * {
  display: table-row;
}

section .col {
  display: table-cell;
}
</style>
</head>"""
def line_AP(AP : AcessPoint):
    return f""" <div class=\"row\"> 
                    <div class=\"col\"> <a href=\"/queijo\">{AP.ssid}</a></div>
                    <div class=\"col\"> {AP.bssid}</div>
                    <div class=\"col\"> {AP.signal}</div>
                    <div class=\"col\"> {AP.band}</div>
                    <div class=\"col\"> {AP.channel}</div>
                </div>"""
def header_table():
     return f"""
           <header>
                    <div class="col">SSID</div>
                    <div class="col">BSSID</div>
                    <div class="col">Signal</div>
                    <div class="col">Bandwith</div>
                    <div class="col">Channel</div>
            </header>
        """

def table_APS(APs : list[AcessPoint]):
    result = "<section class=\"MiTable\">" + header_table()
    for elem in APs:
        result += line_AP(elem)
    result += " </section>\n"
    return result

def body(APs : list[AcessPoint]):
     return "<body><div class=\"title2\">Current Access Points near you</div>" + table_APS(APs) + "</body>"

def render_main_page(APs : list[AcessPoint]):
    return "<html>" + _style() + header + body(APs) + "</html>"
    