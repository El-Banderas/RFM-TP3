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
.flex-container2 {
  display: flex;
  flex-direction: row;
  flex-flow: wrap;
flex-wrap: wrap
  }
.flex-container {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  flex-flow: column;
  background-color: DodgerBlue;
}

.flex-container > div {
  background-color: #f1f1f1;
  margin: 10px;
  text-align: center;
  font-size: 30px;
}
.lineInterior {
  background-color: cyan;
  margin: 10px;
  font-size: 30px;
}
</style>
</head>"""
def line_AP(AP : AcessPoint):
    return f""" <div class=\"flex-container2\"> <a href=\"/queijo\">
                <div class=\"lineInterior\"> {AP.ssid}</div>
                <div class=\"lineInterior\"> {AP.bssid}</div>
                <div class=\"lineInterior\"> {AP.signal}</div>
                <div class=\"lineInterior\"> {AP.band}</div>
                <div class=\"lineInterior\"> {AP.channel}</div>
    </div>"""

def table_APS(APs : list[AcessPoint]):
    result = "<div class=\"flex-container\">"
    for elem in APs:
        result += line_AP(elem)
    result += " </div>\n"
    return result

def body(APs : list[AcessPoint]):
     return "<body>Olá?" + table_APS(APs) + "</body>"

def render_main_page(APs : list[AcessPoint]):
    return "<html>" + _style() + header + body(APs) + "</html>"
    