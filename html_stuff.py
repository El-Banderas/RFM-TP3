
# Flexbox
# https://css-tricks.com/snippets/css/a-guide-to-flexbox/
# HTML + Flexbox + CSS
# https://www.w3schools.com/css/tryit.asp?filename=trycss3_flexbox_flex-wrap_nowrap8


def _root_ap_details_style(refresh_seconds):
	return f"""
		<head>
			<!-- <meta http-equiv=\"refresh\" content=\"{refresh_seconds}\"> -->
			<style>
				body {{
					margin: auto;
					width: 50%;
				}}
				li {{
					list-style-type: none;
					margin: 0;
					border: 1px solid black;
				}}
			</style>
		</head>
	"""


def _render_map(ap):
	result = "<ul>"
	for key in ap.__dict__():
		result += f"<li><b>{key} :</b> {ap.__dict__()[key]}</li>"
	result += " </ul>"
	return result


def render_ap_details(ap, refresh_seconds):
	return f"""
		<html>
			{_root_ap_details_style(refresh_seconds)}
			<title>
				{ap.ssid}
			</title>
			<body>
				{_render_map(ap)}
				{ap.raw}
			</body>
		</html>
	"""


header = f"""
	<html>
		<title>
			Check APs
		</title>
"""


style = f"""
	<head>
		<style>
			.title2 {{
				text-align: center;
				font-size: 30px;
				font-weight: bold;
				margin-top: 30px;
				margin-bottom: 30px;
			}}
			section {{
				display: table;
				margin: 25px 50px 75px 50px;
				width: 100%;
				border-style: solid;
			}}
			.MiTable {{
				margin: auto;
				width: 60%;
			}}
			section > * {{
				display: table-row;
			}}
			section .col {{
				display: table-cell;
			}}
		</style>
	</head>
"""


def ap_line(ap):
	return f"""
		<div class=\"row\"> 
			<div class=\"col\"> <a href=\"/{ap.ssid}\">{ap.ssid}</a></div>
			<div class=\"col\"> {ap.bssid}</div>
			<div class=\"col\"> {ap.strength}</div>
			<div class=\"col\"> {ap.band}</div>
			<div class=\"col\"> {ap.channel}</div>
		</div>
	"""


header_table = f"""
	<header>
		<div class="col">SSID</div>
		<div class="col">BSSID</div>
		<div class="col">Signal</div>
		<div class="col">Bandwith</div>
		<div class="col">Channel</div>
	</header>
"""


def ap_table(access_points):
	result = "<section class=\"MiTable\">" + header_table
	for elem in access_points:
		result += ap_line(elem)
	result += " </section>\n"
	return result


def body(access_points):
	return "<body><div class=\"title2\">Current Access Points near you</div>" + ap_table(access_points) + "</body>"


def render_main_page(access_points):
	return "<html>" + style + header + body(access_points) + "</html>"
