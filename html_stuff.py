# Flexbox
# https://css-tricks.com/snippets/css/a-guide-to-flexbox/
# HTML + Flexbox + CSS
# https://www.w3schools.com/css/tryit.asp?filename=trycss3_flexbox_flex-wrap_nowrap8


"""
========================================================================
============================  BSSID DETAILS  ============================
========================================================================
"""


def _bssid_details_style(refresh_seconds):
	return f"""
		<head>
			<!-- <meta http-equiv=\"refresh\" content=\"{refresh_seconds}\"> -->
			<style>
				body {{
					margin: auto;
					width: 50%;
				}}
				li {{
					list-style: none;
					padding: 5px 4px 6px 7px;
					margin-bottom:7px;
					position:relative;
				}}
				li + li:before {{
					content:'';
					display:block; 
					height:1px;
					background: #eff0f1;
					position:absolute;
					top:-4px;
					left:0;
					right:0;
				}}
				li:hover {{
					background-color: #f7f8f8;
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


def render_bssid_details(ap, refresh_seconds):
	return f"""
		<html>
			{_bssid_details_style(refresh_seconds)}
			<title>
				{ap.ssid}
			</title>
			<body>
				{_render_map(ap)}
			</body>
		</html>
	"""


"""
========================================================================
============================  SSID DETAILS  ============================
========================================================================
"""


_ssid_details_header = f"""
	<html>
		<title>
			Check APs
		</title>
"""

_ssid_details_style = f"""
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


def _ssid_details_table_line(ap):
	return f"""
		<div class=\"row\"> 
			<div class=\"col\"> <a href=\"/{ap.ssid}/{ap.bssidf}\"> {ap.bssid} </a> </div>
			<div class=\"col\"> {ap.strength} </div>
			<div class=\"col\"> {ap.radio_type} </div>
			<div class=\"col\"> {ap.channel} </div>
		</div>
	"""


_ssid_details_table_header = f"""
	<header>
		<div class="col">BSSID</div>
		<div class="col">Signal</div>
		<div class="col">Radio type</div>
		<div class="col">Channel</div>
	</header>
"""


def _ssid_details_table(access_points):
	result = "<section class=\"MiTable\">" + _ssid_details_table_header
	for elem in access_points:
		result += _ssid_details_table_line(elem)
	result += " </section>\n"
	return result


def _ssid_details_body(ssid, access_points):
	return f"<body><div class=\"title2\">{ssid}</div>" + _ssid_details_table(access_points) + "</body>"


def render_ssid_details(ssid, aps):
	access_points = list(aps.values())

	return "<html>" + _ssid_details_style + _ssid_details_header + _ssid_details_body(ssid, access_points) + "</html>"


"""
=====================================================================
============================  MAIN PAGE  ============================
=====================================================================
"""


_main_header = f"""
	<html>
		<title>
			Check APs
		</title>
"""

_main_style = f"""
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


def _main_table_line(ap):
	return f"""
		<div class=\"row\"> 
			<div class=\"col\"> <a href=\"/{ap.ssid}\"> {ap.ssid} </a> </div>
			<div class=\"col\"> <a href=\"/{ap.ssid}/{ap.bssidf}\"> {ap.bssid} </a> </div>
			<div class=\"col\"> {ap.strength} </div>
			<div class=\"col\"> {ap.radio_type} </div>
			<div class=\"col\"> {ap.channel} </div>
		</div>
	"""


_main_table_header = f"""
	<header>
		<div class="col">SSID</div>
		<div class="col">BSSID</div>
		<div class="col">Signal</div>
		<div class="col">Radio type</div>
		<div class="col">Channel</div>
	</header>
"""


def _main_table(access_points):
	result = "<section class=\"MiTable\">" + _main_table_header
	for elem in access_points:
		result += _main_table_line(elem)
	result += " </section>\n"
	return result


def _main_body(access_points):
	return "<body><div class=\"title2\">Current Access Points near you</div>" + _main_table(access_points) + "</body>"


def render_main_page(available_aps):
	access_points = []
	for ssid in available_aps:
		for bssid in available_aps[ssid]:
			access_points.append(available_aps[ssid][bssid])

	return "<html>" + _main_style + _main_header + _main_body(access_points) + "</html>"
