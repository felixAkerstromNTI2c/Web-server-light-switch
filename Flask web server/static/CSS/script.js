const setState = async (ledState) => {
    const fetchSettings = { method: 'POST' };
    const url = "/ledStrip/" + ledState; // Skapa en URL med ledstate värde beroende på vilken knapp som tryckts på

    const fetchResponse = await fetch(url, fetchSettings); // Skicka url till Python och vänta på return
    console.log(url) //Logga URL i konsollen för lättare felsökning

    // Switchcaset lägger till och tar bort bakgrunden på knapparna när raspberry pi tagit emot en request och genomfört den successfully  
    if (fetchResponse.ok){ // If satsen körs om pythonfunktionen setLedStrip(state) skickar tillbaka 204
        switch (url){
            case "/ledStrip/0":
                document.getElementById("onBtnStrip").style = "background: #60A917;";
                document.getElementById("offBtnStrip").style = "background: none;";
                document.getElementById("autoBtnStrip").style = "background: none;";
                lastResponse = 0;
                break;
            case "/ledStrip/1":
                document.getElementById("offBtnStrip").style = "background: #E51400;";
                document.getElementById("onBtnStrip").style = "background: none;";
                document.getElementById("autoBtnStrip").style = "background: none";
                lastResponse = 1;
                break;
            case "/ledStrip/2":
                document.getElementById("autoBtnStrip").style = "background: #172aa9;";
                document.getElementById("onBtnStrip").style = "background: none";
                document.getElementById("offBtnStrip").style = "background: none";
                lastResponse = 2;
                break;
            case "/ledStrip/3":
                document.getElementById("onBtnWhiteLed").style = "background: #60A917;";
                document.getElementById("offBtnWhiteLed").style = "background: none";
                document.getElementById("autoBtnWhiteLed").style = "background: none";
                break;
            case "/ledStrip/4":
                document.getElementById("offBtnWhiteLed").style = "background: #E51400;";
                document.getElementById("onBtnWhiteLed").style = "background: none;";
                document.getElementById("autoBtnWhiteLed").style = "background: none";
                break;
            case "/ledStrip/5":
                document.getElementById("autoBtnWhiteLed").style = "background: #172aa9;";
                document.getElementById("offBtnWhiteLed").style = "background: none;";
                document.getElementById("onBtnWhiteLed").style = "background: none;";
                break;
            case "/ledStrip/6":
                document.getElementById("onBtnHeating").style = "background: #60A917;";
                document.getElementById("offBtnHeating").style = "background: none";
                document.getElementById("autoBtnHeating").style = "background: none";
                break;
            case "/ledStrip/7":
                document.getElementById("offBtnHeating").style = "background: #E51400;";
                document.getElementById("onBtnHeating").style = "background: none";
                document.getElementById("autoBtnHeating").style = "background: none";
                break;
            case "/ledStrip/8":
                document.getElementById("autoBtnHeating").style = "background: #172aa9;";
                document.getElementById("onBtnHeating").style = "background: none";
                document.getElementById("offBtnHeating").style = "background: none";
                break;
        } 
  
    // Meddela i webbläsaren om pythonfunktionen inte genomförts successfully
     } else {
        alert("Command not executed by Raspberry Pi..."); 
     } 
}

