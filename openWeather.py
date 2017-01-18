#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyowm
import math
import sys 
from PyQt4.QtGui import *
import openWeatherGUI
#openWeatherGUI est le fichier .py genere par pyuic4

class MainDialog(QDialog,openWeatherGUI.Ui_Dialog):
	def __init__(self,parent=None):
		super(MainDialog,self).__init__(parent)
		self.setupUi(self)
		#self.cbCities.insertItem(0,"aaa")
		cities=open('cities.txt','r')
		cityList=cities.readlines()
		cities.close()
		self.cbCities.insertItems(0,sorted(cityList))
		self.owm = pyowm.OWM('Mettre ici votre API key openweathermap')  

	def goToWikiRefroidissementEolien(self):
		self.lblTempRessLink.setOpenExternalLinks(True)

	def goToWikiIndiceChaleur(self):
		self.lblHiLink.setOpenExternalLinks(True)

	def pbModifier(self):
		observation = self.owm.weather_at_place(str(self.cbCities.currentText()))  
		w = observation.get_weather()  
		temperature = w.get_temperature('celsius')
		tc=temperature["temp"]
		humidity=w.get_humidity()
		now = w.get_reference_time(timeformat='iso')  
		wind = w.get_wind()
		windS = wind["speed"]*3.6
		windD = wind["deg"]
		pressure=w.get_pressure() 
		cloud=w.get_clouds()
		rain=w.get_rain().get('3h')
		snow=w.get_snow().get('3h')
		humidex=w.get_humidex()
		heatIndex=w.get_heat_index()
		
		self.lblLocalisation.setText(str(self.cbCities.currentText()).translate(None,'\n')+" - "+now)
		self.lblVent.setText(str(windS)+" km/h")
		self.lblDir.setText(str(windD)+u" °")
		self.lblTemp.setText(str(tc)+u" °C")  
		self.lblHum.setText(str(humidity)+" %")
		self.lblPress.setText(str(pressure["press"])+" hPa")
		self.lblNuages.setText(str(cloud)+" %")
		if (rain==None ):
			self.lblPluie.setText("0 mm")
		else:
			self.lblPluie.setText(str(rain)+" mm")
		if (snow==None ):
			self.lblNeige.setText("0 mm")
		else:
			self.lblNeige.setText(str(snow)+" mm")
		
		# Nuage
		if (cloud>0 and cloud<50):
			self.lblSymbole.setPixmap(QPixmap("eclaircies.png"))
		else:
			if (cloud>50):
				self.lblSymbole.setPixmap(QPixmap("nuageux.png"))
			else:
				self.lblSymbole.setPixmap(QPixmap("soleil.png"))
		
		# Pluie
		if (rain!=None ):
			if (cloud<50):
				self.lblSymbole.setPixmap(QPixmap("averses.png"))
			else:
				self.lblSymbole.setPixmap(QPixmap("pluie.png"))
		
		# Neige
		if (snow!=None ):
			self.lblSymbole.setPixmap(QPixmap("neige.png"))

		# Calcul Temperature ressentie
		tempRessentie=0.0
		if(tc>=-50 and tc<=10):	
			if (windS>4.8 and windS<177):
				tempRessentie = 13.12+0.6215*tc+(0.3975*tc-11.36)*math.pow(windS,0.16)
			else:
				if (windS<=4.8):
					tempRessentie = tc+0.2*(0.1345*tc-1.59)*windS
			self.lblTempRessentie.setText(str(round(tempRessentie,2))+u" °C")
		else:
			self.lblTempRessentie.setText(" Sans objet")

		# Calcul Indice de chaleur
		# HI = -42.379 + 2.04901523T + 10.14333127R - 0.22475541TR - 6.83783x10 -3T2- 5.481717x10-2R2 + 1.22874x10-3T2R + 8.5282x10-4TR2 - 1.99x10-6T2R2
		# T : Temperature en Fahrenheit => Tc = (Tf-32)/1.8
		# R : Humidite relative
		R = humidity
		T = 1.8*tc + 32
		if(tc>=27 and tc<=43):	
			HIf = -42.379+2.04901523*T+10.14333127*R-0.22475541*T*R-6.83783e-3*math.pow(T,2)-5.481717e-2*math.pow(R,2)+1.22874e-3*math.pow(T,2)*R+8.5282e-4*T*math.pow(R,2)-1.99e-6*math.pow(T,2)*math.pow(R,2)
			HIc = (HIf -32)/1.8
			self.lblHI.setText(str(round(HIc,2))+u" °C")
		else:
			self.lblHI.setText(" Sans objet")
app=QApplication(sys.argv) 
form=MainDialog()
form.show()
app.exec_()
