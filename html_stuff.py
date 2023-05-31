# Flexbox
# https://css-tricks.com/snippets/css/a-guide-to-flexbox/
# HTML + Flexbox + CSS
# https://www.w3schools.com/css/tryit.asp?filename=trycss3_flexbox_flex-wrap_nowrap8


"""
========================================================================
============================  BSSID DETAILS  ============================
========================================================================
"""

from collections import OrderedDict
from collections import Counter

def _bssid_details_style(refresh_seconds):
	return f"""
		<head>
			<!-- <meta http-equiv=\"refresh\" content=\"{refresh_seconds}\"> -->
			<style>
				body {{

					right: 50%;
					bottom: 50%;
					transform: translate(20%,30%);
					position: absolute;
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
			.title3 {{
				text-align: center;
				font-size: 25px;
				font-weight: 600;
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
			.rowRed {{
				background: rgb(250, 0, 0, 0.5);
			}}
			.rowGreen {{
				background: rgb(0, 250, 0, 0.5);
			}}
			.rowYellow {{
				background: rgb(255, 255, 0, 0.5);
			}}
			
		</style>
	</head>
"""


def _ssid_details_table_line(ap):
	color = translate_strength_color(int(ap.strength[:-1]))
	return f"""
		<div class=\"{color}\"> 
			<div class=\"col\"> <a href=\"/{ap.ssid}/{ap.bssidf}\"> {ap.bssid} </a> </div>
			<div class=\"col\"> {ap.strength} </div>
			<div class=\"col\"> {ap.radio_type} </div>
			<div class=\"col\"> {ap.channel} </div>
		</div>
	"""


_ssid_details_table_header = f"""
	<header>
		<h1 class="col">BSSID</h1>
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
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>

	<head>
		<style>
			.title2 {{
				text-align: center;
				font-size: 30px;
				font-weight: bold;
				margin-top: 30px;
				margin-bottom: 30px;
			}}
			.title3 {{
				text-align: center;
				font-size: 30px;
				font-weight: 600;
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
			.myGraph {{
				margin: auto;
				width: 50%;
			}}
			.rowRed {{
				background: rgb(250, 0, 0, 0.5);
			}}
			.rowGreen {{
				background: rgb(0, 250, 0, 0.5);
			}}
			.rowYellow {{
				background: rgb(255, 255, 0, 0.5);
			}}
			.row{{
			}}
		</style>
	</head>
"""


def translate_strength_color(strength):
	color = ""
	strength = int(strength)
	if strength < 40:
		color = "rowRed"
	elif strength < 70:
		color = "rowYellow"
	else:
		color = "rowGreen"
	return color



def _main_table_line(ap):
	value = "0%"
	if  hasattr(ap, 'strength'): 
		color = translate_strength_color(int(ap.strength[:-1]))
		value = int(ap.strength[:-1])
	else:
		ssid = ap["SSID"]
		bssid = ap["BSSID"]
		value = ap["Signal"]
		radio_type = ap["Radio type"]
		channel = ap["Channel"]
		color = translate_strength_color(int(value[:-1]))
		return f"""
		<div class=\"{color}\"> 
			<div class=\"col\"> <a href=\"/{ssid}\"> {ssid} </a> </div>
			<div class=\"col\"> <a href=\"/{bssid}/{bssid}\"> {bssid} </a> </div>
			<div class=\"col\"> {value} </div>
			<div class=\"col\"> {radio_type} </div>
			<div class=\"col\"> {channel} </div>
		</div>
	"""
	return f"""
		<div class=\"{color}\"> 
			<div class=\"col\"> <a href=\"/{ap.ssid}\"> {ap.ssid} </a> </div>
			<div class=\"col\"> <a href=\"/{ap.ssid}/{ap.bssidf}\"> {ap.bssid} </a> </div>
			<div class=\"col\"> {value} </div>
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

# Count the frequency of utilization of channels
def CountFrequency(my_list):
 
    # Creating an empty dictionary
	freq = {}
	for item in my_list:
		if (item in freq):
			freq[item] += 1
		else:
			freq[item] = 1
	'''
	channels = list(freq.keys())
	channels.sort()
	print("1")
	print(channels)
	print("---")
	sorted_dict = {i: freq[i] for i in channels}
	'''
	sorted_dict = OrderedDict(sorted(freq.items())) 
	res2_4 = []
	res_5 = []
	for key, value in sorted_dict.items():
		if int(key) <= 13:
			res2_4.append({"x": int(key), "y": value})
		else:
			res_5.append({"x": int(key), "y": value})

	#res = (list(sorted_dict.keys()), list(sorted_dict.values()))
        
	return res2_4, res_5

def _main_graph_APS(access_points):
	used_channels = []
	if  hasattr(access_points[0], 'strength'): 
		used_channels = map(lambda ap: ap.channel,  access_points)
	else:
		used_channels = map(lambda ap: ap["Signal"][:-1],  access_points)
	freq2_4, freq_5 = CountFrequency(used_channels)
		
	return f"""
	<div class=\"myGraph\">
				<div class=\"title3\">Channel utilization:</div>
				<canvas id="myChart" style="width:100%;max-width:700px"></canvas>


		<script>

		new Chart(\"myChart\", {{
		type: \"scatter\",
		data: {{
			datasets: [{{
				label: \'Freq 2.4GHz\',
			pointRadius: 4,
			pointBackgroundColor: \"rgb(0,0,255)\",
			backgroundColor: \"rgb(0,0,255)\",
			data: {freq2_4},
			}},
		{{
				label: \'Freq 5GHz\',
			pointRadius: 4,
			pointBackgroundColor: \"rgb(255,0,255)\",
			backgroundColor: \"rgb(255,0,255)\",
			data: {freq_5},
			}},

			]
		}},
		options: {{
			legend: {{display: true}},

			scales: {{
				yAxes: [{{
					ticks: {{
						beginAtZero: true
					}}
				}}]
			}}
		}}
		}});
		</script>

	</div>"""

"""
============================  Opinions about AP's and channels  ============================
"""

def _more_than_one_AP_in_Channel(used_channels):
	freq_dict = Counter(used_channels)
	more_than_one_AP = list(filter(lambda ele: freq_dict[ele] > 1, freq_dict))
	more_than_one_AP.sort()
	if len(more_than_one_AP) < 1:
		return ""
	result = "Channels shared with two or more AP's:<ul>"
	more_than_one_AP.sort()
	for elem in more_than_one_AP:
		#result += _main_table_line(elem)
		result += f"<li>{elem}</li>"
	result += " </ul>\n"
	return result



def _interference_Channels(used_channels):
	channels = sorted(set(list(used_channels)))
	channels_with_interference = list(filter(lambda channel: ((channel+1) in channels) or ((channel-1) in channels), channels)) 

	if len(channels_with_interference) < 1:
		return ""
	result = "Channels with close neibourghs (the could interfere with each other):<ul>"
	for elem in channels_with_interference:
		#result += _main_table_line(elem)
		result += f"<li>{elem}</li>"
	result += " </ul>\n"
	return result

def _comments(access_points):
	used_channels = []
	if (len(access_points)) > 0:
		if  hasattr(access_points[0], 'channel'): 
			print("1")
			used_channels = list(map(lambda ap: int(ap.channel),  access_points))
			#used_channels_copy = map(lambda ap: int(ap.channel[:-1]),  access_points)
			
		else:
			print("2")
			used_channels = list(map(lambda ap: int(ap["Signal"][:-1]),  access_points))
			#used_channels_copy = map(lambda ap: int(ap["Signal"][:-1]),  access_points)
		
	else:
		used_channels = []
	result = "<div  class=\"MiTable\">" + _more_than_one_AP_in_Channel(used_channels) + _interference_Channels(used_channels)+ "</div>"
	return result

def _main_body(access_points):
	return "<body><div class=\"title2\">Current Access Points near you</div>" + _main_table(access_points) + _main_graph_APS(access_points.copy())+ _comments(access_points) +"</body>"


def render_main_page(available_aps):
	access_points = []
	for ssid in available_aps:
		for bssid in available_aps[ssid]:
			access_points.append(available_aps[ssid][bssid])

	return "<html>" + _main_style + _main_header + _main_body(access_points) + "</html>"
