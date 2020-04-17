#define GREEN 11
#define RED 10
#define BLUE 9

int r = 0, g = 0, b = 0;
bool fading = true;
bool partying = false;
int fadeSpeed = 25;
int partySpeed = 25;

int colors[][3] = {
  {255, 0, 0},
  {0, 255, 0},
  {0, 0, 255},
  {213, 0, 255},
  {76, 0, 153}
};

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
  unsigned int ui = 0;
  String strIn, strIn2, strIn3, function;
  int i;
  char input[10];

  if (Serial.available())
  {
    function = Serial.readStringUntil(' ');

    if (function == "c")
    {
      if (fading == true || partying == true)
      {
        fading = false;
        partying = false;
        analogWrite(GREEN, 0);
        analogWrite(RED, 0);
        analogWrite(BLUE, 0);
      } 
      strIn = Serial.readStringUntil(' ');
      strIn2 = Serial.readString();
      i = atoi(strIn2.c_str());
      if (strIn == "g") analogWrite(GREEN, i);
      else if (strIn == "b") analogWrite(BLUE, i);
      else if (strIn == "r") analogWrite(RED, i);
    }

    else if (function == "applyColor")
    {
      partying = false;
      fading = false;
      strIn = Serial.readStringUntil(' ');
      strIn2 = Serial.readStringUntil(' ');
      strIn3 = Serial.readStringUntil(' ');
      analogWrite(RED, atoi(strIn.c_str()));
      analogWrite(GREEN, atoi(strIn2.c_str()));
      analogWrite(BLUE, atoi(strIn3.c_str()));
    }

    else if (function == "f")
    {
      partying = false;
      fading = true;
      strIn = Serial.readString();
      if (strIn != "") fadeSpeed = atoi(strIn.c_str());
    }
    else if (function == "p")
    {
      fading = false;
      partying = true;
      strIn = Serial.readString();
      if (strIn != "") partySpeed = atoi(strIn.c_str());
    }
    else if (function == "d")
    {
      partying = false;
      strIn = Serial.readString();
      if (strIn == "") Serial.println(fadeSpeed);
      else fadeSpeed = atoi(strIn.c_str());
    }

    else if (function == "0")
    {
      partying = false;
      fading = false;
      analogWrite(GREEN, 0);
      analogWrite(RED, 0);
      analogWrite(BLUE, 0);
    }
    else if (function == "w")
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

void party()
{
  setToColor(colors[random(0, sizeof(colors)/3)]);
  delay(partySpeed);
}

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