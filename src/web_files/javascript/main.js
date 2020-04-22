var server_stats = {};
var last_brightness_value = .01;

var brightness_slider = document.getElementById("brightness_slider");
var power_div = document.getElementsByClassName("power_div")[0];
var brightness_label = document.getElementById("brightness_label");
var power_label = document.getElementById("power_label");
var stats_div = document.getElementById("stats_div");

var p =0;
//setInterval(handle_brightness, 500);
//TODO:make ui update with server

//update stats every 2 seconds
setInterval(update_stats_var, 2000);

function handle_brightness()
{
    let brightness_set_request = new XMLHttpRequest()

    server_stats["brightness"] = brightness_slider.value;
    update_ui();

    brightness_set_request.open("GET", "http://"+document.domain+"/api/set_brightness/"+brightness_slider.value);
    brightness_set_request.send();
}

function handle_power()
{
    let power_request = new XMLHttpRequest()

    const power_val = server_stats["led power"] ? 0 : 1;
    server_stats["led power"] = power_val;
    update_ui();

    power_request.open("GET", "http://"+document.domain+"/api/power/"+power_val);

    power_request.send();
}

function update_stats_var()
{
    let stats_request = new XMLHttpRequest();

    stats_request.open("GET", "http://"+document.domain+"/api/server_stats", true);
    
    stats_request.onload = function() {
        server_stats=JSON.parse(stats_request.responseText);
        update_ui();
    };

    stats_request.send();
}

function update_stats_ui()
{
    stats_div.innerHTML = ""

    for (const stat in server_stats) 
    {
        let h2node = document.createElement("h2");
        h2node.innerHTML = stat + ": " + server_stats[stat];
        stats_div.append(h2node);   
    }
}

function update_ui()
{
    setTimeout(update_stats_ui, 100);
    if(server_stats["led power"])
    {
        power_div.id = "on";
        power_label.innerHTML = "Power: ON";
    }
    else
    {
        power_div.id = "off";
        power_label.innerHTML = "Power: OFF";
    }
    brightness_label.innerHTML = "Brightness: "+ server_stats["brightness"];
    brightness_slider.value = server_stats["brightness"];
}