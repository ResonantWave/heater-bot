#include <ESP8266WiFi.h>
 
const char* ssid = ""; // replace with your SSID
const char* password = ""; // replace with your password

WiFiServer server(82); // server port
String header;

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(5, OUTPUT); // set relay as output
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // uncomment this block if you want to specify a static IP address
  /*IPAddress ip(192, 168, 0, 4);
  IPAddress gateway(192, 168, 0, 1);
  IPAddress subnet(255, 255, 255, 0);

  WiFi.config(ip, gateway, subnet);*/
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());

  server.begin();
}
 
void loop(){
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        header += c;
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            
            if (header.indexOf("GET /on") >= 0) {
              digitalWrite(5, 1); // turn on relay
              client.println("ok");
            } else if(header.indexOf("GET /off") >= 0) {
              digitalWrite(5, 0); // turn off relay
              client.println("ok");
            } else if(header.indexOf("GET /status") >= 0) {
              client.println(digitalRead(5)); // get relay status
            }
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = "";
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}

 
