// define the pins for the rgb values
#define GREEN 11
#define RED 10
#define BLUE 9

int r = 0, g = 0, b = 0; // rgb values
bool fading = true; // when true colors fade
bool partying = false; // when true party mode active
int fadeSpeed = 25; // how fast
int partySpeed = 25; // how fast

// array of colors for the party mode
int colors[][3] = {
  {255, 0, 0},
  {0, 255, 0},
  {0, 0, 255},
  {213, 0, 255},
  {76, 0, 153}
};

// set pins to output and start the serial connection boudrate must be eaqual to python script
void setup()
{
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(1000);
}

void loop()
{
  String strIn, strIn2, strIn3, function;
  int i;
  char input[10];

  if (Serial.available())
  {
    function = Serial.readStringUntil(' '); // gets the main function in a string

    if (function == "c") // add color with certain strength
    {
      if (fading == true || partying == true)
      {
        fading = false;
        partying = false;
        analogWrite(GREEN, 0);
        analogWrite(RED, 0);
        analogWrite(BLUE, 0);
      } 
      strIn = Serial.readStringUntil(' '); // wich color
      strIn2 = Serial.readString(); // how intense
      i = atoi(strIn2.c_str()); // converts intensity to int
      if (strIn == "g") analogWrite(GREEN, i);
      else if (strIn == "b") analogWrite(BLUE, i);
      else if (strIn == "r") analogWrite(RED, i);
    }
    else if (function == "applyColor") // applys a certain color to strip
    {
      partying = false;
      fading = false;
      strIn = Serial.readStringUntil(' '); // red value
      strIn2 = Serial.readStringUntil(' ');// green value
      strIn3 = Serial.readStringUntil(' ');// blue value
      analogWrite(RED, atoi(strIn.c_str()));
      analogWrite(GREEN, atoi(strIn2.c_str()));
      analogWrite(BLUE, atoi(strIn3.c_str()));
    }
    else if (function == "f") // sets mode to fading and when given also to the speed
    {
      partying = false;
      fading = true;
      strIn = Serial.readString();
      if (strIn != "") fadeSpeed = atoi(strIn.c_str());
    }
    else if (function == "p") // sets mode to party and when given also to the speed
    {
      fading = false;
      partying = true;
      strIn = Serial.readString();
      if (strIn != "") partySpeed = atoi(strIn.c_str());
    }
    else if (function == "0") // turns stripe off
    {
      partying = false;
      fading = false;
      analogWrite(GREEN, 0);
      analogWrite(RED, 0);
      analogWrite(BLUE, 0);
    }
    else if (function == "w") // sets stripe to white color
    {
      partying = false;
      fading = false;
      analogWrite(GREEN, 255);
      analogWrite(RED, 255);
      analogWrite(BLUE, 255);
    }
    else
    {
      Serial.println("Wrong Syntax");
    }
  }
  if (fading) fade();
  else if (partying) party();
}

// pciks color from arry and sets stripe to it
void party()
{
  setToColor(colors[random(0, sizeof(colors)/3)]);
  delay(partySpeed);
}

// does the fading
void fade()
{
  if      (r < 255 && g == 0 && b == 0) r++; //red
  else if (r == 255 && g < 255 && b == 0) g++; //orange
  else if (r > 0 && g == 255 && b == 0) r--; //green
  else if (r == 0 && g == 255 && b < 255) b++; //turkise
  else if (r == 0 && g > 0 && b == 255) g--; //blue
  else if (r < 255 && g == 0 && b == 255) r++; //pink
  else if (r == 255 && g == 0 && b > 0) b--; //red

  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
  delay(fadeSpeed);
}

void setToColor(int color[])
{
  analogWrite(RED, color[0]);
  analogWrite(GREEN, color[1]);
  analogWrite(BLUE, color[2]);
}