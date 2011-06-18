from  PyQt4 import QtCore, QtGui
from cgame_auto import *
import sys
from catGames import *

lex = [
		"Araba", "Bebek", "Kitap", "Baba", "Anne", "Kelebek", "Su", "Mama",
		"Yemek", "Adda", "Dede", "Puf", "Da", "Sabun", "Tren", "Nine",
		"Bebe", "Gece", "Sabah", "Masa", "Sehpa", "Sopa", "Kolpa", "Dolap",
		"Sokak", "Ev", "Deli", "Okul", "Koku", "Lavabo", "Kedi", "Veli",
		"Sokak", "Solak", "Manyak", "Salak", "Saat", "Vade", "Saka",
		"Sirk", "Firt", "Bot", "Kot", "Yat", "Bat", "Sat", "Kat", "Hat",
		"Bat", "Mat", "Pay", "Kar", "Hala", "Teyze", "Amca", "Proje",
		"Daire", "Yuvarlak", "Kare", "Sark", "Park", "Ben", "Erkek",
		"Adam", "Kiz", "Hiz", "Gaz", "Saz", "Kaz", "Hala", "Kola", "Balo",
		"Kart", "Sarp", "Harp", "Kan", "Kafa", "Bina", "Taban", "Saban",
		"Kaban", "Yaban", "Tavan", "Yavan", "Savan", "Hayvan", "Satan",
		"Sakal", "Bakkal", "Market", "Bilgi", "Ajan", "Bay", "Bayan",
		"Hatun", "Adam", "Saman", "Hakan", "Onur", "Bodur", "Korner",
		"Gol", "Manav", "Karpuz", "Kavun", "Karton", "Tok", "Yok", "Kil",
		"Sil", "Bil", "Pil", "Dil", "Dingil", "Silgi", "Kalem", "Motor",
		"Kart", "Nart", "Abart", "Sakat", "Tart", "Yat", "Mat", "Mart",
		"Dart", "Guatr", "Grip", "Nezle", "Sebze", "Meyve", "Mor", "Siyah",
		"Beyaz", "Lacivert", "Beyin", "Zihin", "Aroma", "Zamir", "Fiil",
		"Eylemsi", "Zarf", "Mektup", "Kasa", "Kazan", "Sazan", "Tarzan",
		"Hazan", "Murat", "Can", "Cem", "Cam", "Kan", "Tan", "Yan", "Ban",
		"Han", "Zan", "An", "Tren", "Yen", "Sen", "Ben", "O", "Bu", "Can",
		"Hasan", "Kem", "Cem", "Yem", "Dem", "Gen", "Bulut", "Park",
		"Bina", "Apartman", "Konut", "Emlak", "Velet"  "Kaba",
		"Seda", "Kadir", "Sinkaf", "Arif", "Tarif", "Sahip", "Tayyip",
		"Rahip", "Cazip", "Katip", "Kamil", "Samil"
		]

class MainWindow(QtGui.QMainWindow):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		# We instantiate a QApplication passing the arguments of the script to it:
		self.MainWindow = QtGui.QMainWindow()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		QtCore.QObject.connect(self.ui.btnStart, QtCore.SIGNAL('clicked()'), self.start_sim)

	def start_sim(self):
		self.x = 0
		#ui.setupUi(MainWindow)
		cmbGameIdx = self.ui.cmbGameType.currentIndex()
		cmbPlotIdx = self.ui.cmbPlot.currentIndex()
		noOfAgents = self.ui.spBNoOfAgents.value()
		beliefIdx = self.ui.cmbBelief.currentIndex()
		dictSize = self.ui.spBDictSize.value()
		draw2D = self.ui.chkDraw2D.isChecked()
		draw3D = self.ui.chkDraw3D.isChecked()

		cgcrbu = CGame()
		cgcrbu.setLexicon(lex)
		cgcrbu.setMaxDictSize(int(dictSize))
		cgcrbu.initAgents(int(noOfAgents), beliefIdx)
		cgcrbu.playGames()
		self.printBasicReport(cgcrbu)

		beliefs = transposed(cgcrbu.getBeliefs())
		initialWords = cgcrbu.getInitialWords()
		self.x += 1

		if (cmbPlotIdx == 0):
			plotBeliefs(beliefs, initialWords, cgcrbu.getConvergedWord(), 1)
		elif (cmbPlotIdx == 1):
			plotCategories(cgcrbu.getCategories(), 1)
		elif (cmbPlotIdx == 2):
			plotSuccessRates(cgcrbu.getSuccesses(), 1)
		elif (cmbPlotIdx == 3):
			plotSuccessvsFails(cgcrbu.getSuccesses(), 1)

	def printBasicReport(self, cgc):
		beliefs = transposed(cgc.getBeliefs())
		initialWords = cgc.getInitialWords()
		noOfIterations = cgc.getNoOfIterations()
		noOfSuccess = cgc.getNoOfSuccesses()
		noOfFailures = cgc.getNoOfFailures()

		print "Iterations " + str(noOfIterations)
		print "No of Successes " + str(noOfSuccess)
		print "No of Failures " + str(noOfFailures)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	cgApp = MainWindow()
	cgApp.show()
	# Now we can start it.
	sys.exit(app.exec_())
