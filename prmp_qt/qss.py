RADIUS = 20
PrmpWindowQss = f"""
#window_frame {{
  background-color: palette(Window);
}}

#round_frame {{
  border-radius: 10px;
  background-color: palette(Window);
}}

#left_round_frame {{
  background-color: palette(Window);
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}}

#titleBar, #statusBar {{
  border: 0px none palette(base);
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  background-color: palette(Window);
  height: {RADIUS+10}px;
}}

#btnClose, #btnMaximize, #btnMinimize {{
  min-width: {RADIUS}px;
  min-height: {RADIUS}px;
  max-width: {RADIUS}px;
  max-height: {RADIUS}px;
  border-radius: {RADIUS/2}px;
  margin: 4px;
}}

#btnMinimize {{
  background-color: hsv(38, 218, 253);
}}

#btnMinimize::hover {{
  background-color: hsv(38, 218, 203);
}}

#btnMinimize::pressed {{
  background-color: hsv(38, 218, 153);
}}

#btnMaximize {{
  background-color: hsv(123, 204, 198);
}}

#btnMaximize::hover {{
  background-color: hsv(123, 204, 148);
}}

#btnMaximize::pressed {{
  background-color: hsv(123, 204, 98);
}}

#btnClose {{
  background-color: hsv(0, 182, 252);
}}

#btnClose::hover {{
  background-color: hsv(0, 182, 202);
}}

#btnClose::pressed {{
  background-color: hsv(0, 182, 152);
}}

#btnClose::disabled, #btnRestore::disabled, #btnMaximize::disabled, #btnMinimize::disabled {{
  background-color: palette(midlight);
}}

QLabel#bold {{
    font-size: 14px;
    font-weight: bold;
}}

#required {{
    color: red;
    text-align: top center;
}}

ColorfulTag {{
    border-radius: 8px;
    padding: 2px;
    font-weight: bold;
    font-size: 13px;
    max-height: 15px;
    min-height: 15px;
}}

ColorfulTag#green {{
    color: green;
    background-color: #e5fff2;
}}

ColorfulTag#blue {{
    color: #57a7d3;
    background-color: #f1faff;
}}

ColorfulTag#red {{
    background-color: #f7deec;
    color: #f75a77;
}}

QScrollBar:vertical {{
    background: white;
    width: 8px;
}}

QScrollBar::handle:vertical {{	
    margin-left: 2px;
    margin-right: 1px;
}}
QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {{
    height: 0px;
    background: none;
}}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

TextButton, LinkButton {{
    /*font-family: Segoe UI Black;*/
    border: 1px;
    border-radius: 5px;
    text-align: center;
    min-height: 20px;
    padding: 5px;
}}

LinkButton#blue_link {{
    color: blue;
}}

LinkButton#blue_link:hover {{
    color: #005583;
}}

LinkButton#blue_link:pressed {{
    color: black;
}}

IconButton, IconTextButton {{
    background-repeat: no-repeat;
    border: none;
    border-radius: 5px;
    max-height: 25px;
    padding: 5px;
}}

#no_border {{
    border: none;
}}

IconButton:hover {{
    background-color: #d6e7ef;
}}

IconButton:pressed {{
    background-color: #c5d5dc;
}}

IconTextButton {{
    background-position: left;
    text-align: left;
    font-family: Roboto;
    font-weight: bold;
}}

LinkButton:hover, IconTextButton:hover {{
    color: #005583;
    background-color: #d6e7ef;
}}

LinkButton:pressed, IconTextButton:pressed {{
    color: #00334f;
}}

LinkButton#left {{
    text-align: left;
    font-family: Roboto Medium;
    font-weight: bold;
}}
IconTextButton#blue, TextButton {{
    font-family: Roboto;
    font-weight: bold;
    color: white;
    padding: 5px;
    padding-left: 15px;
    padding-right: 15px;
    background-color: blue;
}}

LinkIconButton {{
    font-size: 15px;
    font-family: Roboto;
    font-weight: bold;
    padding-right: 30px;
    background-repeat: no-repeat;
    color: #30aff2;
}}

IconTextButton#blue:hover, TextButton:hover {{
    background-color: #0089d3;
}}

IconTextButton#blue:pressed, TextButton:pressed {{
    background-color: #006da7;
}}

IconTextButton#red, TextButton#red {{
    background-color: #d8214d;
}}

IconTextButton#red:hover, TextButton#red:hover {{
    background-color: #b01b40;
}}

IconTextButton#red:pressed, TextButton#red:pressed {{
    background-color: #6a1027;
}}

TextButton#cancel {{
    background-color: #c6efe8;
    color: blue;
}}

TextButton#cancel:hover {{
    background-color: #bde5de;
}}

TextButton#cancel:pressed {{
    background-color: #617572;
    color: white;
}}

TextButton#cancel_red {{
    background-color: #eccfdb;
    color: #ca5f7f;
}}

TextButton#cancel_red:hover {{
    background-color: #cc708c;
}}

TextButton#cancel_red:pressed {{
    background-color: #9c566b;
    color: white;
}}

TextButton {{
    min-width: 50px;
    max-width: 50px;
}}

TextIcon#delete {{
    min-height: 40px;
    max-height: 40px;
    min-width: 40px;
    max-width: 40px;
    border-radius: 20px;
    font-family: Roboto Bold;
    font-size: 30px;
    background-color: #ffda8f;
    color: orange;
}}


TextIcon {{
    min-height: 80px;
    max-height: 80px;
    min-width: 80px;
    max-width: 80px;
    border-radius: 30px;
    font-family: Roboto Bold;
    font-size: 20px;
}}


#submit_button {{
    min-width: 120px;
    min-height: 40px;
    max-height: 40px;
    font-size: 17px;
    border-radius: 10px;
    font-weight: normal;
    font-weight: 600;
    padding: 2px;
}}

"""
