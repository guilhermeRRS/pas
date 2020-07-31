from tkinter import *
from tkinter import ttk
from mip import *
import os, time

##################################################################################################
'''

	Conjunto de funções responsáveis pela coleta, leitura, adaptação dos dados e, por fim, seu retorno na forma desejada

'''
##################################################################################################			Importando 'os' e 'io', necessários para a coleta de dados

#import os, io

##################################################################################################			Constantes

CONSTANTE_BIMESTRE = 1000000	#Obsoleta
CONSTANTE_DOUBLE_1 = "!"
CONSTANTE_DOUBLE_2 = "@"	#essas constantes já abrangem as necessárias para os tipos especificos, sendo assim, cortamos duas condicionais de <self.verifiqueEspeciais>

class pacotePadraoClass():

##################################################################################################			Grupo "betters", 

								#função responável pro transformar um intevalo de minutos em um texto
	def minuto_paraHorario(self, e_intervalo, dia = 0, bimestre = 0):
		intervalo = e_intervalo
		inicio_escrito = ["",0,0,0]
		fim_escrito = ["",0,0,0]
		inicio_consts = [0,0,0]
		fim_consts = [0,0,0]
		escrito = [inicio_escrito, fim_escrito]
		consts = [inicio_consts, fim_consts]
		for i in range(0, 2):
			if(intervalo[i] >= CONSTANTE_BIMESTRE):
				consts[i][0] = CONSTANTE_BIMESTRE
				if(bimestre):
					escrito[i][0] = "(2°):"
			else:
				if(bimestre):
					escrito[i][0] = "(1°):"
			while(intervalo[i] - consts[i][0] - 24*60*(consts[i][1] + 1) >= 0):
				escrito[i][1] += 1
				consts[i][1] += 1
			if(dia):
				if(escrito[i][1] == 0):
					escrito[i][1] = "Segunda"
				elif(escrito[i][1] == 1):
					escrito[i][1] = "Terça"
				elif(escrito[i][1] == 2):
					escrito[i][1] = "Quarta"
				elif(escrito[i][1] == 3):
					escrito[i][1] = "Quinta"
				elif(escrito[i][1] == 4):
					escrito[i][1] = "Sexta"
				elif(escrito[i][1] == 5):
					escrito[i][1] = "Sábado"
				else:
					escrito[i][1] = "Domingo"
				escrito[i][1] = escrito[i][1] + ":"
			else:
				escrito[i][1] = ""
			while(intervalo[i] - consts[i][0] - 24*60*consts[i][1] - 60*(consts[i][2] + 1) >= 0):
				escrito[i][2] += 1
				consts[i][2] += 1
			escrito[i][3] = intervalo[i] - consts[i][0] - 24*60*consts[i][1] - 60*consts[i][2]
			if(escrito[i][2] == 0):
				escrito[i][2] = "00"
			if(escrito[i][3] == 0):
				escrito[i][3] = "00"
		retorno = inicio_escrito[0]+inicio_escrito[1]+str(inicio_escrito[2])+":"+str(inicio_escrito[3])+"-"
		if(inicio_escrito[1] != fim_escrito[1]):
			retorno = retorno+fim_escrito[1]
		retorno = retorno+str(fim_escrito[2])+":"+str(fim_escrito[3])
		return retorno
								#função reduz o intevalo ao seu valor em segundos
	def minuto_irredutivel(self, e_intervalo):
		intervalo = e_intervalo
		for i in range(0, 2):		
			if(intervalo[i] >= CONSTANTE_BIMESTRE):
				intervalo[i] -= CONSTANTE_BIMESTRE
			while(intervalo[i] - 24*60 >= 0):
				intervalo[i] -= 24*60
		return intervalo
								#função tenta escapar caracteres especiais como acentos, espaço e tab
	def better_string(self, e_texto):
		texto = e_texto
		texto = str(texto).strip().upper()
		texto = texto.replace("À","A")
		texto = texto.replace("Á","A")
		texto = texto.replace("Â","A")
		texto = texto.replace("Ã","A")
		texto = texto.replace("Ä","A")
		texto = texto.replace("È","E")
		texto = texto.replace("É","E")
		texto = texto.replace("Ê","E")
		texto = texto.replace("Ë","E")
		texto = texto.replace("Ì","I")
		texto = texto.replace("Í","I")
		texto = texto.replace("Î","I")
		texto = texto.replace("Ï","I")
		texto = texto.replace("Ò","O")
		texto = texto.replace("Ó","O")
		texto = texto.replace("Ô","O")
		texto = texto.replace("Õ","O")
		texto = texto.replace("Ö","O")
		texto = texto.replace("Ù","U")
		texto = texto.replace("Ú","U")
		texto = texto.replace("Û","U")
		texto = texto.replace("Ü","U")
		texto = texto.replace("Ç","C")
		texto = texto.replace("°","º")
		keep = 0
		cutbegin = 0
		aux = ""
		for i in range(len(texto)):
			if(texto[i] == " " or texto[i] == "	"):
				if(keep == 0):
					keep = 1
					cutbegin = i
			else:
				if(keep == 1):
					
					aux = texto[0:cutbegin]+" "
				aux = aux+texto[i]
				keep = 0
		texto = aux
		return texto
								#função que indica uso de caracteres considerados especiais no sistema
	def verifiqueEspeciais(self, e_texto, erro):
		texto = e_texto
		c = 1
		mensagem = ""
		if(CONSTANTE_DOUBLE_1 in texto):
			mensagem = '"'+CONSTANTE_DOUBLE_1+'"'
		if(CONSTANTE_DOUBLE_2 in texto):
			if(mensagem != ""):
				mensagem = mensagem+', "'+CONSTANTE_DOUBLE_2+'"'
			else:
				mensagem = '"'+CONSTANTE_DOUBLE_2+'"'
		if(":" in texto):
			if(mensagem != ""):
				mensagem = mensagem+', ":"'
			else:
				mensagem = '":"'
		if(";" in texto):
			if(mensagem != ""):
				mensagem = mensagem+', ";"'
			else:
				mensagem = '";"'
		if(mensagem != ""):
			c = 0
			erro.append("O texto ["+texto+"] não é válido por conter os seguinter caracteres reservados: "+mensagem)
		return c, erro
								#função que realiza o tratamento dos dados
	def better_valor(self, e_valor, e_tipo, separadorTempo = "-"):
		certo = 1
		erro = []
		aviso = []
		out1 = out2 = 0
		tipo = self.better_string(e_tipo)
		valor = str(e_valor).strip()
		if(tipo == "TEXTO"):
			valor = self.better_string(valor)
			(c, erro) = self.verifiqueEspeciais(valor, erro)
		elif(tipo == "DOUBLEINFOTEXTO"):
			if(len(valor) > 1):
				if(valor[0] == CONSTANTE_DOUBLE_1):
					out2 = 1
					valor = valor[1:]
				elif(valor[0] == CONSTANTE_DOUBLE_2):
					out2 = 2
					valor = valor[1:]
			elif(len(valor) == 1 and (valor == CONSTANTE_DOUBLE_1 or valor == CONSTANTE_DOUBLE_2)):
				certo = 0
				erro.append("Não deveria haver somente um ("+CONSTANTE_DOUBLE_1+") ou ("+CONSTANTE_DOUBLE_2+") como dado, é necessário um texto após ele")
			valor = self.better_string(valor)
			(c, erro) = self.verifiqueEspeciais(valor, erro)
		elif(tipo == "INTERVALOD" or tipo == "INTERVALODB"):
			intervalo = valor.split(separadorTempo)
			intervaloNumerico = [[1,1],[0,0],[0,0]]
			addBimestre = 0
			intervaloMinuto = [0,0]
			intervaloNome = ["inicial", "final"]
			if(len(intervalo) == 2 or len(intervalo) == 3):
				if(len(intervalo) == 3):
					if(tipo == "INTERVALODB"):
						if(intervalo[0].strip() == "2" or intervalo[0].strip() == "S" or intervalo[0].strip() == "SEGUNDO"):
							addBimestre = CONSTANTE_BIMESTRE
						else:
							aviso.append("{Aviso} O horário será considerado do PRIMEIRO semestre, se quisesse que fosse do segundo, escreve-se 2, S ou SEGUNDO")
					intervalo = intervalo[1:]
				inicio = intervalo[0]
				fim = intervalo[1]
				intervalo = [inicio, fim]
				for i in range(0, 2):
					intervalo[i] = intervalo[i].split(":")
					if(len(intervalo[i]) == 3):
						ajuste = 1
						dia = str(intervalo[i][0]).strip()
						if(dia.isnumeric()):
							dia = int(dia)
							if(not (dia > 0 and dia < 8)):
								certo = 0
								erro.append("O dia do horário "+intervaloNome[i]+" não é válido (deveria estar entre 1 e 7)")
							else:
								intervaloNumerico[0][i] = dia
								if(i == 0):
									intervaloNumerico[0][1] = intervaloNumerico[0][0]
						else:
							dia = self.better_string(dia)
							if(dia == "D" or dia == "DO" or dia == "DOMINGO"):
								intervaloNumerico[0][i] = 7
							elif(dia == "T" or dia == "TE" or dia == "TERCA"):
								intervaloNumerico[0][i] = 2
							elif(dia == "SA" or dia == "SAB" or dia == "SABADO"):
								intervaloNumerico[0][i] = 6
							elif(dia == "SEG" or dia == "SEGUNDA"):
								intervaloNumerico[0][i] = 1
							elif(dia == "SEX" or dia == "SEXTA"):
								intervaloNumerico[0][i] = 5
							elif(dia == "QUA" or dia == "QUARTA"):
								intervaloNumerico[0][i] = 3
							elif(dia == "QUI" or dia == "QUINTA"):
								intervaloNumerico[0][i] = 4
							else:
								certo = 0
								erro.append("O dia do horário "+str(intervaloNome[i])+" não é válido (verificar documentação, escrever os dias por inteiro [sem o '-feira'] ou utilizar o número equivalente entre 1 e 7, SENDO 1 A SEGUNDA-FEIRA | "+dia)
							if(certo):
								if(i == 0):
									intervaloNumerico[0][1] = intervaloNumerico[0][0]
						intervalo[i] = intervalo[i][1:]
					if(len(intervalo[i]) == 2):
						hora = str(intervalo[i][0]).strip()
						minuto = str(intervalo[i][1]).strip()
						if(hora.isnumeric()):
							if(minuto.isnumeric()):
								hora = int(hora)
								minuto = int(minuto)
								if(hora >= 0 and hora < 24):
									if(minuto >= 0 and minuto < 60):
										intervaloNumerico[1][i] = hora
										intervaloNumerico[2][i] = minuto
										intervaloMinuto[i] = (intervaloNumerico[0][i] - 1)*60*24 + intervaloNumerico[1][i]*60 + intervaloNumerico[2][i] + addBimestre
									else:
										certo = 0									
										erro.append("O minuto do horário "+intervaloNome[i]+" não é válido (deveria estar entre 0 e 59)")
								else:
									certo = 0								
									erro.append("A hora do horário "+intervaloNome[i]+" não é válido (deveria estar entre 0 e 23)")
							else:
								certo = 0							
								erro.append("O minuto do horário "+intervaloNome[i]+" não é válido (deveria ser um número)")
						else:
							certo = 0						
							erro.append("A hora do horário "+intervaloNome[i]+" não é válido (deveria ser um número)")
					else:
						certo = 0					
						erro.append("O horário "+intervaloNome[i]+" deveria contar um ou dois ':', não "+str(len(intervalo[i]) - 1))
				if(certo):
					if((intervaloNumerico[0][0] != 7 and intervaloNumerico[0][0] < intervaloNumerico[0][1] - 1) and (intervaloNumerico[0][0] == 7 and (intervaloNumerico[0][1] != 7 and intervaloNumerico[0][1] != 1))):
						certo = 0
						erro.append("O horário "+intervaloNome[1]+" não pode 'pular um dia' em relação a "+intervaloNome[0])
					else:
						if(intervaloNumerico[0][0] <= intervaloNumerico[0][1] and intervaloMinuto[0] >= intervaloMinuto[1]):
							certo = 0					
							erro.append("O horário "+intervaloNome[1]+" deveria ser pelo menos um minuto maior do que "+intervaloNome[0])
			else:
				certo = 0		
				erro.append("O intervalo deveria conter um '"+separadorTempo+"' ao invés de "+str(len(intervalo) - 1))
			out1 = intervaloMinuto
		elif(tipo == "TEXTOINTERVALO"):
			valor = valor.split(":")
			if(len(intervalo[i]) == 2):
				dia = str(valor[0]).strip()
				out1 = valor[1:]
				if(dia.isnumeric()):
					dia = int(dia)
					if(not (dia > 0 and dia < 8)):
						certo = 0
						erro.append("O dia do horário "+intervaloNome[i]+" não é válido (deveria estar entre 1 e 7)")
					else:
						intervaloNumerico[0][i] = dia
				else:
					dia = self.better_valor(dia, "texto")
					if(dia == "D" or dia == "DO" or dia == "DOMINGO"):
						intervaloNumerico[0][i] = 7
					elif(dia == "T" or dia == "TE" or dia == "TERCA"):
						intervaloNumerico[0][i] = 2
					elif(dia == "SA" or dia == "SAB" or dia == "SABADO"):
						intervaloNumerico[0][i] = 6
					elif(dia == "SEG" or dia == "SEGUNDA"):
						intervaloNumerico[0][i] = 1
					elif(dia == "SEX" or dia == "SEXTA"):
						intervaloNumerico[0][i] = 5
					elif(dia == "QUA" or dia == "QUARTA"):
						intervaloNumerico[0][i] = 3
					elif(dia == "QUI" or dia == "QUINTA"):
						intervaloNumerico[0][i] = 4
					else:
						certo = 0
						erro.append("O dia do horário "+str(intervaloNome[i])+" não é válido (verificar documentação, escrever os dias por inteiro [sem o '-feira'] ou utilizar o número equivalente entre 1 e 7, SENDO 1 A SEGUNDA-FEIRA")
				out2 = dia
			else:
				out2 = 1
		elif(tipo == "PASTA"):
			if(not os.path.isdir(valor)):
				certo = 0
				erro.append("A pasta ["+valor+"] não existe")
		elif(tipo == "ARQUIVO"):
			if(not os.path.exists(valor)):
				certo = 0
				erro.append("O arquivo ["+valor+"] não existe")
		elif(tipo != "TEXTO" and tipo != "DOUBLEINFOTEXTO" and tipo != "INTERVALOD" and tipo != "INTERVALODB" and tipo != "FREE" and tipo != "PASTA" and tipo != "ARQUIVO" and tipo != "TEXTOINTERVALO"):
			if(valor != ""):
				valor = self.better_string(valor)
				if(valor.replace(".","").strip().isnumeric()):
					out1 = int(float(valor))
					if(tipo == "BIN"):
						if(out1 != 0 and out1 != 1):
							certo = 0					
							erro.append("O valor deveria ser 0/1 ou N/S; NA/SI; NAO/SIM; A/B, mas foi ["+valor+"]")
					elif(tipo == "TRI"):
						if(out1 != 0 and out1 != 1 and out1 != 2):
							certo = 0					
							erro.append("O valor deveria ser 0/1/2 ou A/B/C, mas foi ["+valor+"]")
					elif(tipo == "QUA"):
						if(out1 != 0 and out1 != 1 and out1 != 2 and out1 != 3):
							certo = 0					
							erro.append("O valor deveria ser 0/1/2/3 ou A/B/C/D, mas foi ["+valor+"]")
				else:
					if(tipo == "NUMERICO"):
						certo = 0
						erro.append("O valor deveria ser um número, mas foi ["+valor+"]")
					elif(tipo == "BIN"):
						if(valor == "S" or valor == "SI" or valor == "SIM" or valor == "B"):
							out1 = 1
						elif(valor == "N" or valor == "NA" or valor == "NAO" or valor == "A"):
							out1 = 0
						else:
							certo = 0							
							erro.append("O valor deveria ser N/S; NA/SI; NAO/SIM; A/B ou 0/1, mas foi ["+valor+"]")
					elif(tipo == "TRI"):
						if(valor == "A"):
							out1 = 0
						elif(valor == "B"):
							out1 = 1
						elif(valor == "C"):
							out1 = 2
						else:
							certo = 0							
							erro.append("O valor deveria ser A/B/C ou 0/1/2, mas foi ["+valor+"]")
					elif(tipo == "QUA"):
						if(valor == "A"):
							out1 = 0
						elif(valor == "B"):
							out1 = 1
						elif(valor == "C"):
							out1 = 2
						elif(valor == "D"):
							out1 = 3
						else:
							certo = 0							
							erro.append("O valor deveria ser A/B/C ou 0/1/2, mas foi ["+valor+"]")
					elif(tipo == "RESTWEIGHT"):
						if(valor == "!"):
							out1 = 0
							out2 = 1
						else:
							certo = 0							
							erro.append("O valor deveria ser ("+CONSTANTE_DOUBLE_1+") ou um número, mas foi ["+valor+"]")
					elif(tipo == "VALUEWEIGHT"):
						if(valor[0] == "!"):
							out2 = 1
							valor = valor[1:]
							out1 = 0
							if(valor.isnumeric()):
								out1 = int(valor)
							elif(valor != ""):
								certo = 0							
								erro.append("O valor após ("+CONSTANTE_DOUBLE_1+") deveria ser um número, mas foi ["+valor+"]")
							if(certo and not out1):
								aviso.append("{Aviso} Recomenda-se que o valor após ("+CONSTANTE_DOUBLE_1+") seja diferente de zero, mas foi ["+valor+"]")
						else:
							certo = 0							
							erro.append("Deveria haver um número ou um ("+CONSTANTE_DOUBLE_1+") e um número, mas foi ["+valor+"]")
					elif(tipo == "COMPLEX_VALUEWEIGHT"):
						if(valor != CONSTANTE_DOUBLE_2):
							if(valor[0] == CONSTANTE_DOUBLE_1):
								out2 = 1
								valor = valor[1:]
								out1 = 0
								if(valor.isnumeric()):
									out1 = int(valor)
								elif(valor != ""):
									certo = 0							
									erro.append("O valor após ("+CONSTANTE_DOUBLE_1+") deveria ser um número, mas foi ["+valor+"]")
								if(certo and not out1):
									aviso.append("{Aviso} Recomenda-se que o valor após ("+CONSTANTE_DOUBLE_1+") seja diferente de zero, mas foi ["+valor+"]")
							else:
								certo = 0
								erro.append("Deveria haver ("+CONSTANTE_DOUBLE_2+"), um número, ou um ("+CONSTANTE_DOUBLE_1+") e um número, mas foi ["+valor+"]")
						else:
							out2 = 2
		if(tipo == "TEXTO" or tipo == "DOUBLEINFOTEXTO" or tipo == "FREE" or tipo == "PASTA" or tipo == "ARQUIVO"):
			out1 = valor
		return certo, erro, aviso, out1, out2

	##################################################################################################			Grupo "essenciais", responsáveis por facilitar o desenvolvimento, retorno de erros e encontro de informações, envolvem a maioria, se não todas as áreas da aplicação

								#função responsável por transpor matrizes
	def func_transpor(self, matriz, right = 0, down = 0):
		if(right):
			lenright = len(right)
		else:
			lenright = len(matriz[0])
		if(down):
			lendown = len(down)
		else:
			lendown = len(matriz)
		matrizLinha = []
		for i in range(0, lenright):
			matrizLinha.append([])
			for j in range(0, lendown):
				matrizLinha[-1].append(matriz[j][i])
		return matrizLinha
								#função que iguala uma lista a outra
	def makeIgualOutroList(self, lista):
		listaLinha = []
		for i in range(0, len(lista)):
			listaLinha.append(lista[i])
		return listaLinha
								#função que adiciona mais elementos a lista
	def addToList(self, e_lista, add):
		lista = self.makeIgualOutroList(e_lista)
		for i in range(0, len(add)):
			lista.append(add[i])
		return lista
								#função que adiciona "descrição" a cada elemento de uma lista
	def addToWarning(self, e_warning, tipo, local):
		warning = self.makeIgualOutroList(e_warning)
		if(tipo != ""):
			tipo = tipo+": "
		for i in range(0, len(warning)):
			warning[i] = "[Na "+local+"]: "+tipo+warning[i]
		return warning
								#função que emite lista
	def imprimeArray(self, erro, imprime = 1):
		if(imprime):
			for i in range(0, len(erro)):
				self.errosLeituraDados = self.errosLeituraDados+erro[i]+"\n"
								#função similar a self.addToWarning, porém com "descrição" diferente
	def addToMessage(self, before, e_messages):
		messages = self.makeIgualOutroList(e_messages)
		for i in range(0, len(messages)):
			messages[i] = before+" "+messages[i]
		return messages
								#função une duas lista em uma outra bidimencional (dLista1+dLista2)
	def colide(self, lista1, lista2):
		lista = []
		for i in range(0, len(lista1)):
			lista.append([lista1[i], lista2[i]])
		return lista
								#função que percorre lista procurando um valor
	def getValue(self, lista, colisor, fill = 0, place = 1):
		colisor = self.better_string(colisor)
		for i in range(0, len(lista)):
			if(self.better_string(lista[i][0]) == colisor):
				fill = lista[i][place]
		return fill
								#função que retorna uma determinada dimensão (ou conjunto) de uma lista
	def getAllValues(self, lista, place = 1):
		retorno = []
		for i in range(0, len(lista)):
			retorno.append(lista[i][place])
		return retorno
								#função que define valor de um dado elemento da lista e, caso não exista, o adiciona
	def setValue(self, e_lista, colisor, valor, place = 1):
		c = 0
		lista = []
		colisor = self.better_string(colisor)
		for i in range(0, len(e_lista)):
			lista.append([e_lista[i][0], e_lista[i][1]])
			if(self.better_string(lista[i][0]) == colisor):
				c = 1
				lista[i][place] = valor
		if(not c):
			lista.append([colisor,valor])
		return lista

	##################################################################################################			Grupo "files", analisa extensão e coleta de cada linha

								#função responsável por abrir o arquivo e coletar cada uma das linhas
	def readFile(self, caminho):
	
		certo = 1
		erro = []
		arquivo = []	
		try:	
			with open(caminho, "r", encoding="utf-8") as file:
				nLinha = 1
				for linha in file:		
					linha = str(linha).strip()
					arquivo.append(linha)		
					nLinha += 1		
				if(nLinha == 1):
					certo = 0
					erro.append("Erro: O arquivo"+plus+" está vazio")				
		except:
			certo = 0
			erro.append("Erro: Não foi possível abrir o arquivo ["+caminho+"]")		
		return certo, erro, arquivo
								#função	detectora de extensão
	def fileTipe(self, caminho):
		caminho = caminho.split(".")
		if(caminho[-1].strip().upper() == "CSV"):
			iscsv = 1
		else:
			iscsv = 0
		if(len(caminho) > 2):
			ismorethantwo = 1
		else:
			ismorethantwo = 0
		return iscsv, ismorethantwo

	##################################################################################################			Grupo que trata a estrutura matrizes

								#função de quebra
	def break_matriz(self, r_arquivo, separador):
		arquivo = []
		for i in range(0, len(r_arquivo)):
			if(r_arquivo[i].strip() != ""):
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador)
				for j in range(0, len(r_arquivo[i])):
					arquivo[-1].append([i, j, r_arquivo[i][j].strip()])
			else:
				arquivo.append(0)
		return arquivo
								#função de limpeza
	def clean_matriz(self, arquivo, plus):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		toBeRemembered = [0]
		if(len(arquivo) > 1):
			for i in range(0, len(arquivo)):
				if(i > 0):
					if(arquivo[i] == 0):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
						linesToBeErased.append(i)
					else:
						if(len(arquivo[i]) == 1):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente uma coluna)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][0][2] == ""):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (elemento da primeria coluna zerado)")
								linesToBeErased.append(i)
							else:
								if(arquivo[i][0][2][0] == "#"):
									a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
									linesToBeErased.append(i)
				else:
					if(arquivo[i] == 0):
						c = 0
						e.append("Erro: A linha "+str(i + 1)+" do arquivo"+plus+" deve ser preenchida")
					else:
						if(len(arquivo[i]) == 1):
							c = 0
							e.append("Erro: A linha "+str(i + 1)+" do arquivo"+plus+" deve possuir mais de uma coluna")
							linesToBeErased.append(i)
						else:
							controle = 1
							if(arquivo[i][0][2] != ""):
								if(arquivo[i][0][2][0] == "#"):
									controle = 0
									c = 0
									e.append("A linha "+str(i + 1)+" do arquivo"+plus+" não pode ser um comentário")
									linesToBeErased.append(i)
							if(controle):
								for j in range(1, len(arquivo[i])):
									if(arquivo[i][j][2] == ""):
										a.append("A coluna "+str(j + 1)+" do arquivo"+plus+" será pulada (em branco)")
									else:
										if(arquivo[i][j][2][0] == "#"):
											a.append("A coluna "+str(j + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
										else:
											toBeRemembered.append(j)
		elif(len(arquivo) == 1):
			c = 0
			e.append("Erro: O arquivo"+plus+" deve ter mais linhas além do cabeçalho")
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		i = len(arquivo) - 1
		while(i >= 0):
			j = len(arquivo[i]) - 1
			while(j >= 0):
				controle = 0
				for k in range(0, len(toBeRemembered)):
					if(arquivo[i][j][1] == toBeRemembered[k]):
						controle = 1
				if(not controle):
					del arquivo[i][j]
				j -= 1
			i -= 1
		if(len(toBeRemembered) == 1 and len(arquivo) > 1):
			c = 0
			e.append("Erro: Todas as colunas do arquivo"+plus+" foram puladas")
		if(len(arquivo) == 1 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo"+plus+" teve todas as linhas após o cabeçalho puladas")
		return c, e, a, arquivo
								#função de conversão de dado do eixo right
	def eixo_matrizRight(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(1, len(arquivo[0])):
			(c, e, a, o1, o2) = self.better_valor(arquivo[0][i][2], tipo)
			a = self.addToMessage("No elemento da linha 1, coluna "+str(arquivo[0][i][1] + 1)+":", a)
			e = self.addToMessage("Erro no elemento da linha 1, coluna "+str(arquivo[0][i][1] + 1)+":", e)
			if(c):
				arquivo[0][i][2] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função de conversão de dado do eixo down
	def eixo_matrizDown(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(1, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][0][2], tipo)
			a = self.addToMessage("No elemento da linha "+str(arquivo[i][0][0] + 1)+", coluna 1:", a)
			e = self.addToMessage("Erro no elemento da linha "+str(arquivo[i][0][0] + 1)+", coluna 1:", e)
			if(c):
				arquivo[i][0][2] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função de conversão de dados internos da matriz
	def losdados_matriz(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(1, len(arquivo)):
			for j in range(1, len(arquivo[i])):
				(c, e, a, o1, o2) = self.better_valor(arquivo[i][j][2], tipo)
				a = self.addToMessage("No elemento da linha "+str(arquivo[i][j][0] + 1)+", coluna "+str(arquivo[i][j][1])+":", a)
				e = self.addToMessage("Erro no elemento da linha "+str(arquivo[i][j][0] + 1)+", coluna "+str(arquivo[i][j][1])+":", e)
				if(c):
					arquivo[i][j][2] = [o1, o2]
					aviso = self.addToList(aviso, a)
				else:
					certo = 0
					erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados no eixo right
	def dontrepete_matrizRight(self, arquivo):
		certo = 1
		erro = []
		dados = []
		colunas = []
		colunasRepetidas = []
		repetidos = []
		for i in range(1, len(arquivo[0])):
			dados.append(arquivo[0][i][2][0])
			colunas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					colunasRepetidas.append([colunas[i]])
				else:
					colunasRepetidas[repetidos.index(dados[i])].append(colunas[i])
		if(len(colunasRepetidas) > 0):
			certo = 0	
			for i in range(0, len(colunasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[0][colunasRepetidas[i][0]][2][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes colunas: "
				for j in range(0, len(colunasRepetidas[i])):
					if(j != 0):
						if(j < len(colunasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[0][colunasRepetidas[i][j]][1] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função que impede repetição de dados no eixo down
	def dontrepete_matrizDown(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(1, len(arquivo)):
			dados.append(arquivo[i][0][2][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][0][2][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes linhas: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função que verifica a coerência com dados externos do eixo right
	def isthere_matrizRight(self, arquivo, colisor, interEntry, noticeLack):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		if(not interEntry):
			for i in range(0, len(colisor)):
				colisor[i] = self.better_string(colisor[i])
				mensagem = mensagem+"\n"+colisor[i]
		else:
			for i in range(0, len(colisor)):
			
				(c, e, a, colisor[i], g) = self.better_valor(colisor[i], interEntry)
				colisor[i] = self.minuto_irredutivel(colisor[i])
				mensagem = mensagem+"\n"+self.minuto_paraHorario(colisor[i])
		dados = []
		colunas = []
		colunasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(1, len(arquivo[0])):
			if(not interEntry):
				dados.append(arquivo[0][i][2][0])
			else:
				dados.append(self.minuto_irredutivel(arquivo[0][i][2][0]))
			colunas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				colunasDesconhecidas.append(colunas[i])
		if(len(colunasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(colunasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[0][colunasDesconhecidas[i]][2][0])+"] mencionado na coluna "+str(arquivo[0][colunasDesconhecidas[i]][1] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência com dados externos do eixo down
	def isthere_matrizDown(self, arquivo, colisor, interEntry, noticeLack):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		if(not interEntry):
			for i in range(0, len(colisor)):
				colisor[i] = self.better_string(colisor[i])
				mensagem = mensagem+"\n"+colisor[i]
		else:
			for i in range(0, len(colisor)):
				(c, e, a, colisor[i], g) = self.better_valor(colisor[i], interEntry)
				colisor[i] = self.minuto_irredutivel(colisor[i])
				mensagem = mensagem+"\n"+self.minuto_paraHorario(colisor[i])
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(1, len(arquivo)):
			if(not interEntry):
				dados.append(arquivo[i][0][2][0])
			else:
				dados.append(self.minuto_irredutivel(arquivo[i][0][2][0]))
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				if(interEntry):
					arquivo[linhasDesconhecidas[i]][0][2][0] = self.minuto_paraHorario(arquivo[linhasDesconhecidas[i]][0][2][0])
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][0][2][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(interEntry):
						colisor[i] = self.minuto_paraHorario(colisor[i])
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_matriz(self, arquivo, expected_down, zero1, zero2):
		transpor = 0
		if(self.better_string(arquivo[0][0][2]) == self.better_string(expected_down)):
			transpor = 1
		right = []
		down = []
		dadosDim1 = []
		dadosDim2 = []
		for i in range(0, len(arquivo)):
			if(i == 0):
				for j in range(1, len(arquivo[i])):
					right.append(arquivo[0][j][2][0])
			else:
				dadosDim1.append([])
				dadosDim2.append([])
				down.append(arquivo[i][0][2][0])
				for j in range(1, len(arquivo[i])):
					dadosDim1[-1].append(arquivo[i][j][2][0])
					dadosDim2[-1].append(arquivo[i][j][2][1])
		for i in range(0, len(down)):
			for j in range(len(dadosDim1[i]), len(right)):
				dadosDim1[i].append(zero1)
				dadosDim2[i].append(zero2)
		if(transpor):
			dadosDim1 = self.func_transpor(dadosDim1, right, down)
			dadosDim2 = self.func_transpor(dadosDim2, right, down)
			aux = right
			right = down
			down = aux
		return right, down, dadosDim1, dadosDim2
								#função que preenche os dados que o programa que chamou receberá
	def fill_matriz(self, entradaDim1, entradaDim2, currentRight, currentDown, expectedRight, expectedDown, zero1, zero2):
		matrizDim1 = []
		matrizDim2 = []
		if(expectedRight != 0):
			rightLen = len(expectedRight)
			for i in range(0, rightLen):
				expectedRight[i] = self.better_string(expectedRight[i])
		else:
			rightLen = len(currentRight)
		if(expectedDown != 0):
			downLen = len(expectedDown)
			for i in range(0, downLen):
				expectedDown[i] = self.better_string(expectedDown[i])
		else:
			downLen = len(currentDown)
		for i in range(0, downLen):
			matrizDim1.append([])
			matrizDim2.append([])
			for j in range(0, rightLen):
				matrizDim1[-1].append(zero1)
				matrizDim2[-1].append(zero2)
		for i in range(0, len(currentDown)):
			for j in range(0, len(currentRight)):
				m = i
				n = j
				if(expectedDown):
					m = expectedDown.index(currentDown[i])
				if(expectedRight):
					n = expectedRight.index(currentRight[j])
				matrizDim1[m][n] = entradaDim1[i][j]
				matrizDim2[m][n] = entradaDim2[i][j]
		return matrizDim1, matrizDim2

	##################################################################################################			Grupo que trata a estrutura simple

								#função de quebra
	def break_simple(self, r_arquivo, separador1, separador2):
		arquivo = []
		for i in range(0, len(r_arquivo)):	
			if(r_arquivo[i].strip() != ""):		
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador1)			
				if(len(r_arquivo[i]) > 1):			
					aux = r_arquivo[i][0]				
					del r_arquivo[i][0]			
					arquivo[-1].append([i, aux.strip()])
					arquivo[-1].append(separador1.join(r_arquivo[i]))
					arquivo[-1][-1] = arquivo[i][1].split(separador2)
					for j in range(0, len(arquivo[-1][-1])):
						arquivo[-1][-1][j] = [i, j, arquivo[-1][-1][j].strip()]
				else:
					arquivo[-1].append(0)
			else:
				arquivo.append(0)			
		return arquivo
								#função de limpeza
	def clean_simple(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][0][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][0][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
							else:
								elementsToBeErased = []
								for j in range(0, len(arquivo[i][1])):
									if(arquivo[i][1][j][2] == ""):
										elementsToBeErased.append(j)
										a.append("O "+str(j + 1)+"º elemento após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado (em branco)")
									else:
										if(arquivo[i][1][j][2][0] == "#"):
											elementsToBeErased.append(j)
											a.append("O "+str(j + 1)+"º elemento após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado (é um comentário)")
								j = len(elementsToBeErased) - 1
								while(j >= 0):
									del arquivo[i][1][elementsToBeErased[j]]
									j -=1
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		linesToBeErased = []
		for i in range(0, len(arquivo)):
			if(len(arquivo[i][1]) == 0):
				a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (todos os seus elementos foram pulados)")
				linesToBeErased.append(i)
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dado do eixo up
	def eixo_simpleUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][0][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", e)
			if(c):
				arquivo[i][0][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados do eixo up
	def dontrepete_simpleUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][0][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][0][1][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes linhas: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função de conversão de dados além dos do eixo up
	def losdados_simple(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i][1])):
				(c, e, a, o1, o2) = self.better_valor(arquivo[i][1][j][2], tipo)
				a = self.addToMessage("No "+str(arquivo[i][1][j][1] + 1)+"° elemento da linha "+str(arquivo[i][1][j][0] + 1)+", após o dado inicial:", a)
				e = self.addToMessage("Erro no "+str(arquivo[i][1][j][1] + 1)+"° elemento da linha "+str(arquivo[i][1][j][0] + 1)+", após o dado inicial:", e)
				if(c):
					arquivo[i][1][j][2] = [o1, o2]
					aviso = self.addToList(aviso, a)
				else:
					certo = 0
					erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados além dos do eixo up na mesma linha
	def dontrepete_simpleDados(self, arquivo):
		certo = 1
		erro = []
		for i in range(0, len(arquivo)):
			dados = []
			posicoeselementos = []
			posicoeselementosRepetidas = []
			repetidos = []
			for j in range(0, len(arquivo[i][1])):
				dados.append(arquivo[i][1][j][2][0])
				posicoeselementos.append(j)
			for j in range(0, len(dados)):
				if(dados.count(dados[j]) > 1):
					if(repetidos.count(dados[j]) == 0):
						repetidos.append(dados[j])
						posicoeselementosRepetidas.append([posicoeselementos[j]])
					else:
						posicoeselementosRepetidas[repetidos.index(dados[j])].append(posicoeselementos[j])
			if(len(posicoeselementosRepetidas) > 0):
				certo = 0
				for j in range(0, len(posicoeselementosRepetidas)):
					mensagem = "Erro, na linha "+str(arquivo[i][0][0] + 1)+" o mesmo dado ["+str(arquivo[i][1][posicoeselementosRepetidas[j][0]][2][0])+"] foi mencionado mais de uma vez nessa linha, manter em somente uma das seguintes posições: "
					for k in range(0, len(posicoeselementosRepetidas[j])):
						if(k != 0):
							if(k < len(posicoeselementosRepetidas[j]) - 1):
								mensagem = mensagem+", "
							else:
								mensagem = mensagem+" e "
						mensagem = mensagem+str(arquivo[i][1][posicoeselementosRepetidas[j][k]][1] + 1)
					erro.append(mensagem+", após o dado inicial")
		return certo, erro, arquivo
								#função que verifica a coerência com dados do eixo up
	def isthere_simpleUp(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][0][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][0][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência com dados externos além dos do eixo up
	def isthere_simpleDados(self, arquivo, colisor):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		for i in range(0, len(arquivo)):
			dados = []
			elementos = []
			elementosDesconhecidos = []
			colisoresIgnorados = []
			for j in range(0, len(arquivo[i][1])):
				dados.append(arquivo[i][1][j][2][0])
				elementos.append(j)
			for j in range(0, len(dados)):
				if(colisor.count(dados[j]) == 0):
					elementosDesconhecidos.append(elementos[j])
			if(len(elementosDesconhecidos) > 0):
				if(certo):
					erro.append(mensagem)
				certo = 0	
				for j in range(0, len(elementosDesconhecidos)):
					mensagem = "Erro o dado ["+str(arquivo[i][1][elementosDesconhecidos[j]][2][0])+"] "+str(arquivo[i][1][elementosDesconhecidos[j]][1] + 1)+"º elemento da linha "+str(arquivo[i][1][elementosDesconhecidos[j]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
					erro.append(mensagem)
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_simple(self, arquivo, zero1 = 0, one1 = 1, zero2 = 0):
		up = []
		down = []
		dadosDim1 = []
		dadosDim2 = []
		for i in range(0, len(arquivo)):
			up.append(arquivo[i][0][1][0])
			for j in range(0, len(arquivo[i][1])):
				if(down.count(arquivo[i][1][j][2][0]) == 0):
					down.append(arquivo[i][1][j][2][0])
		for i in range(0, len(up)):
			dadosDim1.append([])
			dadosDim2.append([])
			for j in range(0, len(down)):
				dadosDim1[-1].append(zero1)
				dadosDim2[-1].append(zero2)
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i][1])):
				dadosDim1[i][down.index(arquivo[i][1][j][2][0])] = one1
				dadosDim2[i][down.index(arquivo[i][1][j][2][0])] = arquivo[i][1][j][2][1]
		return up, down, dadosDim1, dadosDim2
								#função que preenche os dados que o programa que chamou receberá
	def fill_simple(self, entradaDim1, entradaDim2, currentUp, currentDados, expectedUp = 0, expectedDados = 0, zero1 = 0, zero2 = 0):
		matrizDim1 = []
		matrizDim2 = []
		if(expectedUp != 0):
			upLen = len(expectedUp)
			for i in range(0, upLen):
				expectedUp[i] = self.better_string(expectedUp[i])
		else:
			upLen = len(currentUp)
		if(expectedDados != 0):
			dadosLen = len(expectedDados)
			for i in range(0, dadosLen):
				expectedDados[i] = self.better_string(expectedDados[i])
		else:
			dadosLen = len(currentDados)
		for i in range(0, upLen):
			matrizDim1.append([])
			matrizDim2.append([])
			for j in range(0, dadosLen):
				matrizDim1[-1].append(zero1)
				matrizDim2[-1].append(zero2)
		for i in range(0, len(currentUp)):
			for j in range(0, len(currentDados)):
				m = i
				n = j
				if(expectedUp):
					m = expectedUp.index(currentUp[i])
				if(expectedDados):
					n = expectedDados.index(currentDados[j])
				matrizDim1[m][n] = entradaDim1[i][j]
				matrizDim2[m][n] = entradaDim2[i][j]
		return matrizDim1, matrizDim2

	##################################################################################################			Grupo que trata a estrutura complex

								#função de quebra
	def break_complex(self, r_arquivo, separador1, separador2, separador3):
		arquivo = []
		for i in range(0, len(r_arquivo)):	
			if(r_arquivo[i].strip() != ""):
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador1)			
				if(len(r_arquivo[i]) > 1):			
					aux = r_arquivo[i][0]				
					del r_arquivo[i][0]				
					arquivo[-1].append([i, aux.strip()])
					arquivo[-1].append(separador1.join(r_arquivo[i]))
					arquivo[-1][-1] = arquivo[-1][-1].split(separador2)
					for j in range(0, len(arquivo[-1][-1])):
						arquivo[-1][-1][j] = arquivo[-1][-1][j].split(separador3)
						for k in range(0, len(arquivo[-1][-1][j])):
							arquivo[-1][-1][j][k] = [i, j, k, arquivo[-1][-1][j][k].strip()]
				else:
					arquivo[-1].append(0)
			else:
				arquivo.append(0)
		return arquivo
								#função de limpeza
	def clean_complex(self, arquivo, lim, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][0][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][0][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
							else:
								conjuntosToBeErased = []
								for j in range(0, len(arquivo[i][1])):
									plus2 = ""
									plus3 = "1º elemento "
									if(len(arquivo[i][1][j]) > 0):
										plus2 = " único"
										plus3 = ""
									if(arquivo[i][1][j][0][3] == ""):
										conjuntosToBeErased.append(j)
										a.append("O "+str(j + 1)+"º conjunto"+plus2+" após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado ("+plus3+"em branco)")
									else:
										if(arquivo[i][1][j][0][3][0] == "#"):
											conjuntosToBeErased.append(j)
											a.append("O "+str(j + 1)+"º conjunto"+plus2+" após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado ("+plus3+"é um comentário)")
									elementsToBeErased = []
									for k in range(1, len(arquivo[i][1][j])):
										if(k < lim):
											if(arquivo[i][1][j][k][3] == ""):
												elementsToBeErased.append(k)
												a.append("O "+str(k + 1)+"º elemento do "+str(j + 1)+"º conjunto após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado (em branco)")
											else:
												if(arquivo[i][1][j][k][3][0] == "#"):
													elementsToBeErased.append(k)
													a.append("O "+str(k + 1)+"º elemento do "+str(j + 1)+"º conjunto após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", será pulado (é um comentário)")
										elif(k == lim):
											elementsToBeErased.append(k)
											a.append("Os elementos após "+str(k + 1)+"º, incluindo este, do "+str(j + 1)+"º conjunto após o dado inicial, na linha "+str(i + 1)+" do arquivo"+plus+", serão pulados (desnecessários)")
										else:
											elementsToBeErased.append(k)
											
									k = len(elementsToBeErased) - 1
									while(k >= 0):
										del arquivo[i][1][j][elementsToBeErased[k]]
										k -=1
								j = len(conjuntosToBeErased) - 1
								while(j >= 0):
									del arquivo[i][1][conjuntosToBeErased[j]]
									j -=1
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		linesToBeErased = []
		for i in range(0, len(arquivo)):
			if(len(arquivo[i][1]) == 0):
				a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (todos os seus elementos foram pulados)")
				linesToBeErased.append(i)
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_complexUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][0][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", e)
			if(c):
				arquivo[i][0][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados do eixo up
	def dontrepete_complexUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][0][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][0][1][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes linhas: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função de conversão de dados além dos do eixo up
	def losdados_complex(self, arquivo, tipos):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i][1])):
				for k in range(0, len(arquivo[i][1][j])):
					(c, e, a, o1, o2) = self.better_valor(arquivo[i][1][j][k][3], tipos[k])
					a = self.addToMessage("No "+str(arquivo[i][1][j][k][2] + 1)+"° elemento do "+str(arquivo[i][1][j][k][1] + 1)+"° conjunto da linha "+str(arquivo[i][1][j][k][0] + 1)+":", a)
					e = self.addToMessage("Erro no "+str(arquivo[i][1][j][k][2] + 1)+"° elemento do "+str(arquivo[i][1][j][k][1] + 1)+"° conjunto da linha "+str(arquivo[i][1][j][k][0] + 1)+":", e)
					if(c):
						arquivo[i][1][j][k][3] = [o1, o2]
						aviso = self.addToList(aviso, a)
					else:
						certo = 0
						erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados além dos do eixo up na mesma linha
	def dontrepete_complexDados(self, arquivo):
		certo = 1
		erro = []
		for i in range(0, len(arquivo)):
			dados = []
			posicoesconjuntos = []
			posicoesconjuntosRepetidas = []
			repetidos = []
			for j in range(0, len(arquivo[i][1])):
				dados.append(arquivo[i][1][j][0][3][0])
				posicoesconjuntos.append(j)
			for j in range(0, len(dados)):
				if(dados.count(dados[j]) > 1):
					if(repetidos.count(dados[j]) == 0):
						repetidos.append(dados[j])
						posicoesconjuntosRepetidas.append(posicoesconjuntos[j])
					else:
						posicoesconjuntosRepetidas.append(posicoesconjuntos[j])
			if(len(posicoesconjuntosRepetidas) > 0):
				certo = 0
				mensagem = "Erro, na linha "+str(arquivo[i][0][0] + 1)+" o mesmo dado ["+str(arquivo[i][1][posicoesconjuntosRepetidas[0]][0][3][0])+"] foi mencionado mais de uma vez o primeiro elemento dos seguintes conjuntos: "
				for j in range(0, len(posicoesconjuntosRepetidas)):
					if(j != 0):
						if(j < len(posicoesconjuntosRepetidas) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[i][1][posicoesconjuntosRepetidas[j]][0][1] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função que verifica a coerência com dados do eixo up
	def isthere_complexUp(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][0][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][0][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência com dados externos além dos do eixo up
	def isthere_complexDados(self, arquivo, colisor):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		for i in range(0, len(arquivo)):
			dados = []
			elementos = []
			elementosDesconhecidos = []
			colisoresIgnorados = []
			for j in range(0, len(arquivo[i][1])):
				dados.append(arquivo[i][1][j][0][3][0])
				elementos.append(j)
			for j in range(0, len(dados)):
				if(colisor.count(dados[j]) == 0):
					elementosDesconhecidos.append(elementos[j])
			if(len(elementosDesconhecidos) > 0):
				if(certo):
					erro.append(mensagem)
				certo = 0	
				for j in range(0, len(elementosDesconhecidos)):
					mensagem = "Erro o dado ["+str(arquivo[i][1][elementosDesconhecidos[j]][0][3][0])+"] "+str(arquivo[i][1][elementosDesconhecidos[j]][0][2] + 1)+"º elemento do "+str(arquivo[i][1][elementosDesconhecidos[j]][0][1] + 1)+"º conjunto da linha "+str(arquivo[i][1][elementosDesconhecidos[j]][0][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
					erro.append(mensagem)
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_complex(self, arquivo, zeros1, zeros2, specialOne1 = 0, specialOne2 = 0):
		up = []
		down = []
		matrizes_dadosDim1 = []
		matrizes_dadosDim2 = []
		for i in range(0, len(arquivo)):
			up.append(arquivo[i][0][1][0])
			for j in range(0, len(arquivo[i][1])):
				if(down.count(arquivo[i][1][j][0][3][0]) == 0):
					down.append(arquivo[i][1][j][0][3][0])
		for i in range(0, len(zeros1)):
			matrizes_dadosDim1.append([])
			matrizes_dadosDim2.append([])
			for j in range(0, len(up)):
				matrizes_dadosDim1[-1].append([])
				matrizes_dadosDim2[-1].append([])
				for k in range(0, len(down)):
					matrizes_dadosDim1[-1][-1].append(zeros1[i])
					matrizes_dadosDim2[-1][-1].append(zeros2[i])
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i][1])):
				for k in range(1, len(arquivo[i][1][j])):
					matrizes_dadosDim1[k - 1][up.index(arquivo[i][0][1][0])][down.index(arquivo[i][1][j][0][3][0])] = arquivo[i][1][j][k][3][0]
					matrizes_dadosDim2[k - 1][i][down.index(arquivo[i][1][j][0][3][0])] = arquivo[i][1][j][k][3][1]
				if(specialOne1):
					if(len(arquivo[i][1][j]) - 1 < len(zeros1)):
						for k in range(len(arquivo[i][1][j]) - 1, len(zeros1)):
							matrizes_dadosDim1[k - 1][i][down.index(arquivo[i][1][j][0][3][0])] = specialOne1[k - 1]
							matrizes_dadosDim2[k - 1][i][down.index(arquivo[i][1][j][0][3][0])] = specialOne2[k - 1]
		return up, down, matrizes_dadosDim1, matrizes_dadosDim2
								#função que preenche os dados que o programa que chamou reberá
	def fill_complex(self, entradasDim1, entradasDim2, currentUp, currentDados, expectedUp = 0, expectedDados = 0, zero1 = 0, zero2 = 0):
		if(expectedUp != 0):
			upLen = len(expectedUp)
			for i in range(0, upLen):
				expectedUp[i] = self.better_string(expectedUp[i])
		else:
			upLen = len(currentUp)
		if(expectedDados != 0):
			dadosLen = len(expectedDados)
			for i in range(0, dadosLen):
				expectedDados[i] = self.better_string(expectedDados[i])
		else:
			dadosLen = len(currentDados)
		matrizDim1 = []
		matrizDim2 = []
		for k in range(0, len(entradasDim1)):
			matrizDim1.append([])
			matrizDim2.append([])
			for i in range(0, upLen):
				matrizDim1[-1].append([])
				matrizDim2[-1].append([])
				for j in range(0, dadosLen):
					matrizDim1[-1][-1].append(zero1)
					matrizDim2[-1][-1].append(zero2)
			for i in range(0, len(currentUp)):
				for j in range(0, len(currentDados)):
					m = i
					n = j
					if(expectedUp):
						m = expectedUp.index(currentUp[i])
					if(expectedDados):
						n = expectedDados.index(currentDados[j])
					matrizDim1[-1][m][n] = entradasDim1[k][i][j]
					matrizDim2[-1][m][n] = entradasDim2[k][i][j]
		return matrizDim1, matrizDim2

	##################################################################################################			Grupo que trata a estrutura couple

								#função de quebra
	def break_couple(self, r_arquivo, separador):
		arquivo = []
		for i in range(0, len(r_arquivo)):	
			if(r_arquivo[i].strip() != ""):
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador)			
				if(len(r_arquivo[i]) > 1):			
					aux = r_arquivo[i][0]	
					del r_arquivo[i][0]
					arquivo[-1].append(i)
					arquivo[-1].append(aux.strip())
					arquivo[-1].append(separador.join(r_arquivo[i]).strip())
				else:
					arquivo[-1].append(0)
			else:
				arquivo.append(0)
		return arquivo
								#função de limpeza
	def clean_couple(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
							else:
								if(arquivo[i][2] == ""):
									linesToBeErased.append(i)
									a.append("A linha "+str(i + 1)+" do arquivo"+plus+", será pulado (elemento após o dado inicial em branco)")
								else:
									if(arquivo[i][2][0] == "#"):
										linesToBeErased.append(i)
										a.append("A linha "+str(i + 1)+" do arquivo"+plus+", será pulado (elemento após o dado inicial é um comentário)")
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_coupleUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados do eixo up
	def dontrepete_coupleUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(self.better_string(arquivo[i][1][0]))
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][1][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes linhas: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função de conversão de dados além dos do eixo up, sendo todos tratados igualmente
	def losdados_couple(self, arquivo, tipo, pasta = ""):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
				arquivo[i][2] = pasta+"/"+arquivo[i][2]
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][2], tipo)
			a = self.addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][2] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função de conversão de dados além dos do eixo up, sendo todos tratados de acordo com o valor do eixo up associado
	def losdados_fixedcouple(self, arquivo, relacoes):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][2], self.getValue(relacoes, arquivo[i][1][0]))
			a = self.addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][2] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que verifica a coerência com dados do eixo up
	def isthere_coupleUp(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência com dados além dos do eixo up
	def isthere_coupleDados(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][2][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][2][0])+"] mencionado, após o dado inicial, na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_couple(self, arquivo):
		upDim1 = []
		upDim2 = []
		dadosDim1 = []
		dadosDim2 = []
		for i in range(0, len(arquivo)):
			upDim1.append(arquivo[i][1][0])
			upDim2.append(arquivo[i][1][1])
			dadosDim1.append(arquivo[i][2][0])
			dadosDim2.append(arquivo[i][2][1])
		return upDim1, upDim2, dadosDim1, dadosDim2
								#função que preenche os dados que o programa que chamou receberá
	def fill_couple(self, currentUpDim1, currentUpDim2, currentDadosDim1, currentDadosDim2, expectedUp, zero = 0, zeros = 0):
		if(zeros == 0):
			zeros = []
			for i in range(0, len(expectedUp)):
				zeros.append(zero)
		upDim1 = []
		upDim2 = []
		listaDim1 = []
		listaDim2 = []
		if(expectedUp != 0):
			upLen = len(expectedUp)
			for i in range(0, upLen):
				expectedUp[i] = self.better_string(expectedUp[i])
				upDim2.append(0)
			upDim1 = expectedUp
		else:
			upLen = len(currentUpDim1)
			upDim1 = currentDadosDim1
			upDim2 = currentUpDim2
		for i in range(0, upLen):
			listaDim1.append(zeros[i])
			listaDim2.append(zeros[i])
		for i in range(0, len(currentUpDim1)):
			m = i
			if(expectedUp):
				m = expectedUp.index(currentUpDim1[i])
			listaDim1[m] = currentDadosDim1[i]
			listaDim2[m] = currentDadosDim2[i]
			upDim2[m] = currentUpDim2[i]
		return upDim1, upDim2, self.colide(expectedUp, listaDim1), self.colide(expectedUp, listaDim2)

	##################################################################################################			Grupo que trata a estrutura single

								#função de quebra
	def break_single(self, r_arquivo):
		arquivo = []
		for i in range(0, len(r_arquivo)):
			arquivo.append([i, r_arquivo[i].strip()])
		return arquivo
								#função de limpeza
	def clean_single(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_singleUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados do eixo up
	def dontrepete_singleUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro, o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][1][0])+"] foi mencionado mais de uma vez, mantes em somente uma das seguintes linhas [isso não é um erro, é a indicação de uma redundância no arquivo]: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_single(self, arquivo):
		upDim1 = []
		upDim2 = []
		for i in range(0, len(arquivo)):
			upDim1.append(arquivo[i][1][0])
			upDim2.append(arquivo[i][1][1])
		return upDim1, upDim2

	##################################################################################################			Grupo que trata a estrutura line

								#função de quebra
	def break_line(self, r_arquivo, separador):
		arquivo = []
		for i in range(0, len(r_arquivo)):	
			if(r_arquivo[i].strip() != ""):
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador)			
				if(len(r_arquivo) > 0):
					for j in range(len(r_arquivo[i])):
						arquivo[-1].append([i, j, r_arquivo[i][j].strip()])
			else:
				arquivo.append(0)			
		return arquivo
								#função de limpeza
	def clean_line(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						thereIsFilled = 0
						for j in range(len(arquivo[i])):
							if(arquivo[i][j][2] != ""):
								thereIsFilled += 1
						if(thereIsFilled < 2):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não possui a quantidade de informações necessária)")
							linesToBeErased.append(i)
						else:
							k = 1
							if(arquivo[i][0][2] != ""):
								if(arquivo[i][0][2][0] == "#"):
									a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
									linesToBeErased.append(i)
									k = 0
							if(k):
								elementsToBeErased = []
								for j in range(0, len(arquivo[i])):
									if(arquivo[i][j][2] == ""):
										elementsToBeErased.append(j)
										a.append("O "+str(j + 1)+"º elemento da linha "+str(i + 1)+" do arquivo"+plus+", será pulado (em branco)")
								j = len(elementsToBeErased) - 1
								while(j >= 0):
									del arquivo[i][elementsToBeErased[j]]
									j -= 1
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
								
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		linesToBeErased = []
		for i in range(0, len(arquivo)):
			if(len(arquivo[i]) == 0):
				a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (todos os seus elementos foram pulados)")
				linesToBeErased.append(i)
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão dos dados
	def losdados_line(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i])):
				(c, e, a, o1, o2) = self.better_valor(arquivo[i][j][2], tipo)
				a = self.addToMessage("No "+str(arquivo[i][j][1] + 1)+"° elemento da linha "+str(arquivo[i][j][0] + 1)+", após o dado inicial:", a)
				e = self.addToMessage("Erro no "+str(arquivo[i][j][1] + 1)+"° elemento da linha "+str(arquivo[i][j][0] + 1)+", após o dado inicial:", e)
				if(c):
					arquivo[i][j][2] = o1
					aviso = self.addToList(aviso, a)
				else:
					certo = 0
					erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados na mesma linha
	def dontrepete_lineDados(self, arquivo):
		certo = 1
		erro = []
		for i in range(0, len(arquivo)):
			dados = []
			posicoeselementos = []
			posicoeselementosRepetidas = []
			repetidos = []
			for j in range(0, len(arquivo[i])):
				dados.append(arquivo[i][j][2])
				posicoeselementos.append(j)
			for j in range(0, len(dados)):
				if(dados.count(dados[j]) > 1):
					if(repetidos.count(dados[j]) == 0):
						repetidos.append(dados[j])
						posicoeselementosRepetidas.append([posicoeselementos[j]])
					else:
						posicoeselementosRepetidas[repetidos.index(dados[j])].append(posicoeselementos[j])
			if(len(posicoeselementosRepetidas) > 0):
				certo = 0
				for j in range(0, len(posicoeselementosRepetidas)):
					mensagem = "Erro, na linha "+str(arquivo[i][j][0] + 1)+" o mesmo dado ["+str(arquivo[i][posicoeselementosRepetidas[j][0]][2])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes posições: "
					for k in range(0, len(posicoeselementosRepetidas[j])):
						if(k != 0):
							if(k < len(posicoeselementosRepetidas[j]) - 1):
								mensagem = mensagem+", "
							else:
								mensagem = mensagem+" e "
						mensagem = mensagem+str(arquivo[i][posicoeselementosRepetidas[j][k]][1] + 1)
					erro.append(mensagem+", após o dado inicial")
		return certo, erro, arquivo
								#função que verifica a coerência externa dos dados
	def isthere_lineDados(self, arquivo, colisor):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		for i in range(0, len(arquivo)):
			dados = []
			elementos = []
			elementosDesconhecidos = []
			colisoresIgnorados = []
			for j in range(0, len(arquivo[i])):
				dados.append(arquivo[i][j][2])
				elementos.append(j)
			for j in range(0, len(dados)):
				if(colisor.count(dados[j]) == 0):
					elementosDesconhecidos.append(elementos[j])
			if(len(elementosDesconhecidos) > 0):
				certo = 0
				erro.append(mensagem)
				for j in range(0, len(elementosDesconhecidos)):
					mensagem = "Erro o dado ["+str(arquivo[i][elementosDesconhecidos[j]][2])+"] "+str(arquivo[i][elementosDesconhecidos[j]][1] + 1)+"º elemento da linha "+str(arquivo[i][elementosDesconhecidos[j]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
					erro.append(mensagem)
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que o chamou e os preenche
	def fill_line(self, arquivo, expectedDados, zero = 0):
		matriz = []
		dadosLen = len(expectedDados)
		for i in range(0, dadosLen):
			expectedDados[i] = self.better_string(expectedDados[i])
		for i in range(0, dadosLen):
			matriz.append([])
			for j in range(0, dadosLen):
				matriz[-1].append(zero)
		for i in range(0, len(arquivo)):
			for j in range(0, len(arquivo[i])):
				for k in range(0, len(arquivo[i])):
					m = expectedDados.index(arquivo[i][j][2])
					n = expectedDados.index(arquivo[i][k][2])
					matriz[m][n] = 1
		return matriz

	##################################################################################################			Grupo que trata a estrutura four

								#função de quebra
	def break_four(self, r_arquivo, separador):
		arquivo = []
		for i in range(0, len(r_arquivo)):	
			if(r_arquivo[i].strip() != ""):
				arquivo.append([])
				r_arquivo[i] = r_arquivo[i].split(separador)			
				if(len(r_arquivo[i]) > 1):			
					aux = r_arquivo[i][0]	
					del r_arquivo[i][0]
					arquivo[-1].append(i)
					arquivo[-1].append(aux.strip())
					for j in range(len(r_arquivo[i])):
						arquivo[-1].append(r_arquivo[i][j].strip())
				else:
					arquivo[-1].append(0)
			else:
				arquivo.append(0)
		return arquivo
								#função de limpeza
	def clean_four(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) != 5):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não possui exatamente quatro dados)")
						linesToBeErased.append(i)
					else:
						f = 1
						if(arquivo[i][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
							f = 0
						if(arquivo[i][2] == "" or arquivo[i][3] == "" or arquivo[i][4] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não são fornecidos todos os dados necessários após o dado inicial)")
							linesToBeErased.append(i)
							f = 0
						if(f):
							if(arquivo[i][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_fourUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados no eixo up
	def dontrepete_fourUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(self.better_string(arquivo[i][1][0]))
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][1][0])+"] foi mencionado mais de uma vez, manter em somente uma das seguintes linhas: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função de conversão dos dados1
	def losdados1_four(self, arquivo, tipo, pasta = ""):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
				arquivo[i][2] = pasta+"/"+arquivo[i][2]
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][2], tipo)
			a = self.addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][2] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função de conversão dos dados2
	def losdados2_four(self, arquivo, tipo, pasta = ""):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
				arquivo[i][3] = pasta+"/"+arquivo[i][3]
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][3], tipo)
			a = self.addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][3] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função de conversão dos dados3
	def losdados3_four(self, arquivo, tipo, pasta = ""):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
				arquivo[i][4] = pasta+"/"+arquivo[i][4]
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][4], tipo)
			a = self.addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][4] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que verifica a coerência externa do eixo up
	def isthere_fourUp(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência externa dos dados1
	def isthere1_fourDados(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][2][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][2][0])+"] mencionado, após o dado inicial, na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência externa dos dados2
	def isthere2_fourDados(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][3][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][3][0])+"] mencionado, após o dado inicial, na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que verifica a coerência externa dos dados3
	def isthere3_fourDados(self, arquivo, colisor, noticeLack = 0):
		certo = 1
		erro = []
		aviso = []
		mensagem = "São aceitos as seguintes dados:"
		for i in range(0, len(colisor)):
			colisor[i] = self.better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
		dados = []
		linhas = []
		linhasDesconhecidas = []
		colisoresIgnorados = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][4][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(colisor.count(dados[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
		if(len(linhasDesconhecidas) > 0):
			erro.append(mensagem)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][4][0])+"] mencionado, após o dado inicial, na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
				erro.append(mensagem)
		if(noticeLack):
			for i in range(0, len(colisor)):
				if(dados.count(colisor[i]) == 0):
					if(noticeLack == 1):
						aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
					if(noticeLack > 1):
						certo = 0
						erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_four(self, arquivo):
		up = []
		dados1 = []
		dados2 = []
		dados3 = []
		for i in range(0, len(arquivo)):
			up.append(arquivo[i][1][0])
			dados1.append(arquivo[i][2][0])
			dados2.append(arquivo[i][3][0])
			dados3.append(arquivo[i][4][0])
		return up, dados1, dados2, dados3

	##################################################################################################			Grupo que trata a estrutura doubled //não usada

								#função de quebra
	def break_doubled(self, r_arquivo):
		arquivo = []
		for i in range(0, len(r_arquivo)):
			arquivo.append([i, r_arquivo[i].strip()])
		return arquivo
								#função de limpeza
	def clean_doubled(self, arquivo, plus = ""):

		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
						
				else:
					if(arquivo[i][1] == ""):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][1][0] == "#"):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
							linesToBeErased.append(i)
					
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
								
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
			
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_doubled(self, arquivo, tipo):

		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
				
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados no eixo up
	def dontrepete_doubled(self, arquivo):
		certo = 1
		erro = []
		
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		
		for i in range(0, len(arquivo)):
			if(not arquivo[i][1][1]):
				dados.append([arquivo[i][1][0],arquivo[i][1][1]])
			else:
				dados.append([arquivo[i][1][0],arquivo[i][1][1] - 1])
			
			linhas.append(i)
		
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				if(arquivo[linhasRepetidas[i][0]][1][1] == 2):
					textoNivel = "com um @"
				else:
					textoNivel = "com um ! ou nada"
				mensagem = "Erro, o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][1][0])+"] foi mencionado mais de uma vez ["+textoNivel+"], mantes em somente uma das seguintes linhas [isso não é um erro, é a indicação de uma redundância no arquivo]: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0] + 1)
				erro.append(mensagem)
					
		return certo, erro, arquivo
								#função que verifica a coerência externa dos dados
	def isthere_doubled(self, arquivo, colisor1, colisor2):
		certo = 1
		erro = []
		aviso = []
		
		mensagem1 = "São aceitos as seguintes dados [quando usado nada ou !]:"
		for i in range(0, len(colisor1)):
			colisor1[i] = self.better_string(colisor1[i])
			mensagem1 = mensagem1+"\n"+colisor1[i]
		mensagem2 = "São aceitos as seguintes dados [quando usado @]:"
		for i in range(0, len(colisor2)):
			colisor2[i] = self.better_string(colisor2[i])
			mensagem2 = mensagem2+"\n"+colisor2[i]
		
		dados1 = []
		dados2 = []
		linhas = []
		linhasDesconhecidas = []
		
		pl1 = 0
		pl2 = 0
		
		for i in range(0, len(arquivo)):
			if(arquivo[i][1][1] == 2):
				dados2.append(arquivo[i][1][0])
			else:
				dados1.append(arquivo[i][1][0])
			linhas.append(i)
			
		for i in range(0, len(dados1)):
			if(colisor1.count(dados1[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
				pl1 = 1
				
		for i in range(0, len(dados2)):
			if(colisor2.count(dados2[i]) == 0):
				linhasDesconhecidas.append(linhas[i])
				pl2 = 1
				
		if(len(linhasDesconhecidas) > 0):
			if(pl1):
				erro.append(mensagem1)
			if(pl2):
				erro.append(mensagem2)
			certo = 0	
			for i in range(0, len(linhasDesconhecidas)):
				if(arquivo[linhasDesconhecidas[i]][1][1] == 2):
					mensagem2 = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [lista de elementos com @ aceitos, impressa anteriormente]"
					erro.append(mensagem2)
				else:
					mensagem1 = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][1][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0] + 1)+" não pertence a lista de dados aceitos [lista de elementos com ! ou sem nada aceitos, impressa anteriormente]"
					erro.append(mensagem1)
			
		return certo, erro, aviso, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou
	def readable_doubled(self, arquivo):

		upDim1 = []
		upDim2 = []
		
		for i in range(0, len(arquivo)):
			upDim1.append(arquivo[i][1][0])
			upDim2.append(arquivo[i][1][1])
			
		return upDim1, upDim2

	##################################################################################################			Grupo que trata a estrutura especial single

								#função de quebra
	def break_especialSingle(self, r_arquivo):
		arquivo = []
		for i in range(0, len(r_arquivo)):
			arquivo.append([i, r_arquivo[i].strip()])
		return arquivo
								#função de limpeza
	def clean_especialSingle(self, arquivo, plus = ""):
		if(plus != ""):
			plus = " ["+plus+"]"
		c = 1
		e = []
		a = []
		linesToBeErased = []
		if(len(arquivo) > 0):
			for i in range(0, len(arquivo)):
				if(arquivo[i] == 0):
					a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (em branco)")
					linesToBeErased.append(i)
				else:
					if(len(arquivo[i]) == 1):
						a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (somente um dado)")
						linesToBeErased.append(i)
					else:
						if(arquivo[i][1] == ""):
							a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (não é dado o dado inicial)")
							linesToBeErased.append(i)
						else:
							if(arquivo[i][1][0] == "#"):
								a.append("A linha "+str(i + 1)+" do arquivo"+plus+" será pulada (é um comentário)")
								linesToBeErased.append(i)
		else:
			c = 0
			e.append("Erro: O arquivo"+plus+" está vazio")
		i = len(linesToBeErased) - 1
		while(i >= 0):
			del arquivo[linesToBeErased[i]]
			i -= 1
		if(len(arquivo) == 0 and len(linesToBeErased) > 0):
			c = 0
			e.append("Erro: O arquivo teve todas as suas linhas puladas")
		return c, e, a, arquivo
								#função de conversão de dados do eixo up
	def eixo_especialSingleUp(self, arquivo, tipo):
		certo = 1
		erro = []
		aviso = []
		for i in range(0, len(arquivo)):
			(c, e, a, o1, o2) = self.better_valor(arquivo[i][1], tipo)
			a = self.addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
			e = self.addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
			if(c):
				arquivo[i][1] = [o1, o2]
				aviso = self.addToList(aviso, a)
			else:
				certo = 0
				erro = self.addToList(erro, e)
		return certo, erro, aviso, arquivo
								#função que impede repetição de dados do eixo up
	def dontrepete_especialSingleUp(self, arquivo):
		certo = 1
		erro = []
		dados = []
		linhas = []
		linhasRepetidas = []
		repetidos = []
		for i in range(0, len(arquivo)):
			dados.append(arquivo[i][1][0])
			linhas.append(i)
		for i in range(0, len(dados)):
			if(dados.count(dados[i]) > 1):
				if(repetidos.count(dados[i]) == 0):
					repetidos.append(dados[i])
					linhasRepetidas.append([linhas[i]])
				else:
					linhasRepetidas[repetidos.index(dados[i])].append(linhas[i])
		if(len(linhasRepetidas) > 0):
			certo = 0
			for i in range(0, len(linhasRepetidas)):
				mensagem = "Erro, o mesmo dado ["+str(arquivo[linhasRepetidas[i][0]][1][0])+"] foi mencionado mais de uma vez, mantes em somente uma das seguintes linhas [isso não é um erro, é a indicação de uma redundância no arquivo]: "
				for j in range(0, len(linhasRepetidas[i])):
					if(j != 0):
						if(j < len(linhasRepetidas[i]) - 1):
							mensagem = mensagem+", "
						else:
							mensagem = mensagem+" e "
					mensagem = mensagem+str(arquivo[linhasRepetidas[i][j]][0] + 1)
				erro.append(mensagem)
		return certo, erro, arquivo
								#função que converte dados em informações tratáveis pelo programa que chamou e converte em vetor
	def readable_especialSingle(self, arquivo, out):
		upDim1 = []
		upDim2 = []
		c = 1
		e = []

		for i in range(len(out)):
			upDim1.append(0)
			upDim2.append(0)
		
		for i in range(0, len(arquivo)):
			
			if(out.count(arquivo[i][1][0]) == 0):
				e.append("O dado indicado na linha "+str(arquivo[i][0])+" não é conhecido, verificar se houve erro de escrita, como caracteres dobrados ou invertidos em ["+arquivo[i][1][0]+"]")
				c = 0
			else:
				upDim1[out.index(arquivo[i][1][0])] = arquivo[i][1][0]
				upDim2[out.index(arquivo[i][1][0])] = arquivo[i][1][1]
				
		return c, e, upDim1, upDim2

	##################################################################################################

								#função responsável pela estrutura matriz
	def trate_matriz(self, arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
		right = []
		down = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = self.break_matriz(arquivo, break_rules)
		(c, e, a, arquivo) = self.clean_matriz(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			oc0 = 0
			oc1 = 1
			if(self.better_string(arquivo[0][0][2]) == self.better_string(readable_rules[0])):
				oc0 = 1
				oc1 = 0
			(c, e, a, arquivo) = self.eixo_matrizRight(arquivo, eixo_rules[oc0])
			self.imprimeArray(a)
			if(c):
				(c, e, a, arquivo) = self.eixo_matrizDown(arquivo, eixo_rules[oc1])
				self.imprimeArray(a)
				if(c):
					(c, e, a, arquivo) = self.losdados_matriz(arquivo, losdados_rules)
					self.imprimeArray(a)
					if(c):
						(c, e, arquivo) = self.dontrepete_matrizRight(arquivo)
						if(c):
							(c, e, arquivo) = self.dontrepete_matrizDown(arquivo)
							if(c):
								if(isthere_rules[oc0][0]):
									(c, e, a, arquivo) = self.isthere_matrizRight(arquivo, isthere_rules[oc0][1], isthere_rules[oc0][2], isthere_rules[oc0][3])
									self.imprimeArray(a)
									if(not c):
										self.imprimeArray(e)
								if(c):
									if(isthere_rules[oc1][0]):
										(c, e, a, arquivo) = self.isthere_matrizDown(arquivo, isthere_rules[oc1][1], isthere_rules[oc1][2], isthere_rules[oc1][3])
										self.imprimeArray(a)
										if(not c):
											self.imprimeArray(e)
									if(c):
										(right, down, dadosDim1, dadosDim2) = self.readable_matriz(arquivo, readable_rules[0], readable_rules[1], readable_rules[2])
										(dadosDim1, dadosDim2) = self.fill_matriz(dadosDim1, dadosDim2, right, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
										if(fill_rules[0] != 0):
											right = fill_rules[0]
										if(fill_rules[1] != 0):
											down = fill_rules[1]
							else:
								self.imprimeArray(e)
						else:
							self.imprimeArray(e)
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, right, down, dadosDim1, dadosDim2
								#função responsável pela estrutura simple
	def trate_simple(self, arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
		up = []
		down = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = self.break_simple(arquivo, break_rules[0], break_rules[1])
		(c, e, a, arquivo) = self.clean_simple(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_simpleUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_simpleUp(arquivo)
				if(c):
					(c, e, a, arquivo) = self.losdados_simple(arquivo, losdados_rules)
					self.imprimeArray(a)
					if(c):
						(c, e, arquivo) = self.dontrepete_simpleDados(arquivo)
						if(c):
							if(isthere_rules[0][0]):
								(c, e, a, arquivo) = self.isthere_simpleUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
								self.imprimeArray(a)
								if(not c):
									self.imprimeArray(e)
							if(c):
								if(isthere_rules[1][0]):
									(c, e, a, arquivo) = self.isthere_simpleDados(arquivo, isthere_rules[1][1])
									self.imprimeArray(a)
									if(not c):
										self.imprimeArray(e)
								if(c):
									(up, down, dadosDim1, dadosDim2) = self.readable_simple(arquivo,readable_rules[0], readable_rules[1], readable_rules[2])
									(dadosDim1, dadosDim2) = self.fill_simple(dadosDim1, dadosDim2, up, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
									if(fill_rules[0] != 0):
										up = fill_rules[0]
									if(fill_rules[1] != 0):
										down = fill_rules[1]
						else:
							self.imprimeArray(e)
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)	
		else:
			self.imprimeArray(e)
		return c, up, down, dadosDim1, dadosDim2
								#função responsável pela estrutura complex
	def trate_complex(self, arquivo, nome, break_rules, clean_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
		up = []
		down = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = self.break_complex(arquivo, break_rules[0], break_rules[1], break_rules[2])
		(c, e, a, arquivo) = self.clean_complex(arquivo, clean_rules, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_complexUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_complexUp(arquivo)
				if(c):
					(c, e, a, arquivo) = self.losdados_complex(arquivo, losdados_rules)
					self.imprimeArray(a)
					if(c):
						(c, e, arquivo) = self.dontrepete_complexDados(arquivo)
						if(c):
							if(isthere_rules[0][0]):
								(c, e, a, arquivo) = self.isthere_complexUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
								self.imprimeArray(a)
								if(not c):
									self.imprimeArray(e)
							if(c):
								if(isthere_rules[1][0]):
									(c, e, a, arquivo) = self.isthere_complexDados(arquivo, isthere_rules[1][1])
									self.imprimeArray(a)
									if(not c):
										self.imprimeArray(e)
								if(c):
									(up, down, dadosDim1, dadosDim2) = self.readable_complex(arquivo, readable_rules[0], readable_rules[1], readable_rules[2], readable_rules[3])
									(dadosDim1, dadosDim2) = self.fill_complex(dadosDim1, dadosDim2, up, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
									if(fill_rules[0] != 0):
										up = fill_rules[0]
									if(fill_rules[1] != 0):
										down = fill_rules[1]
									if(clean_rules == 2):
										dadosDim1 = dadosDim1[0]
										dadosDim2 = dadosDim2[0]
							else:
								self.imprimeArray(e)
						else:
							self.imprimeArray(e)
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, up, down, dadosDim1, dadosDim2
								#função responsável pela estrutura couple
	def trate_couple(self, arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, fill_rules):
		upDim1 = []
		upDim2 = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = self.break_couple(arquivo, break_rules)
		(c, e, a, arquivo) = self.clean_couple(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_coupleUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_coupleUp(arquivo)
				if(c):
					if(not losdados_rules[0]):
						(c, e, a, arquivo) = self.losdados_couple(arquivo, losdados_rules[1], losdados_rules[2])
					else:
						(c, e, a, arquivo) = self.losdados_fixedcouple(arquivo, losdados_rules[1])
					self.imprimeArray(a)
					if(c):
						if(len(isthere_rules) != 2):
							if(isthere_rules[0]):
								(c, e, a, arquivo) = self.isthere_coupleUp(arquivo, isthere_rules[1], isthere_rules[2])
								self.imprimeArray(a)
								if(not c):
									self.imprimeArray(e)
						else:
							if(isthere_rules[0][0]):
								(c, e, a, arquivo) = self.isthere_coupleUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
								self.imprimeArray(a)
								if(not c):
									self.imprimeArray(e)
						if(c):
							if(len(isthere_rules) == 2):
								if(isthere_rules[1][0]):
									(c, e, a, arquivo) = self.isthere_coupleDados(arquivo, isthere_rules[1][1], isthere_rules[1][2])
									self.imprimeArray(a)
									if(not c):
										self.imprimeArray(e)
							if(c):
								(upDim1, upDim2, dadosDim1, dadosDim2) = self.readable_couple(arquivo)
								if(fill_rules[0]):
									(upDim1, upDim2, dadosDim1, dadosDim2) = self.fill_couple(upDim1, upDim2, dadosDim1, dadosDim2, fill_rules[1], fill_rules[2], fill_rules[3])
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, upDim1, upDim2, dadosDim1, dadosDim2
								#função responsável pela estrutura single
	def trate_single(self, arquivo, nome, eixo_rules):
		upDim1 = []
		upDim2 = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = break_single(arquivo)
		(c, e, a, arquivo) = clean_single(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = eixo_singleUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = dontrepete_singleUp(arquivo)
				if(c):
					(upDim1, upDim2) = readable_single(arquivo)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, upDim1, upDim2
								#função responsável pela estrutura line
	def trate_line(self, arquivo, nome, break_rules, isthere_rules, losdados_rules, fill_rules):
		dados = []
		arquivo = self.break_line(arquivo, break_rules)
		(c, e, a, arquivo) = self.clean_line(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.losdados_line(arquivo, losdados_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_lineDados(arquivo)
				if(c):
					if(isthere_rules):
						(c, e, a, arquivo) = self.isthere_lineDados(arquivo, isthere_rules)
						self.imprimeArray(a)
						if(not c):
							self.imprimeArray(e)
					if(c):
						(dados) = self.fill_line(arquivo, isthere_rules, fill_rules)
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, dados
								#função responsável pela estrutura four
	def trate_four(self, arquivo, nome, break_rules, eixo_rules, losdados_rules, isthere_rules):
		up = []
		dados1 = []
		dados2 = []
		dados3 = []
		arquivo = self.break_four(arquivo, break_rules)
		(c, e, a, arquivo) = self.clean_four(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_fourUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_fourUp(arquivo)
				if(c):
					(c, e, a, arquivo) = self.losdados1_four(arquivo, losdados_rules[1], losdados_rules[2])
					self.imprimeArray(a)
					if(c):
						(c, e, a, arquivo) = self.losdados2_four(arquivo, losdados_rules[3], losdados_rules[4])
						self.imprimeArray(a)
						if(c):
							(c, e, a, arquivo) = self.losdados3_four(arquivo, losdados_rules[5], losdados_rules[6])
							self.imprimeArray(a)
							if(c):
								if(isthere_rules[0][0]):
									(c, e, a, arquivo) = self.isthere_fourUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
									self.imprimeArray(a)
									if(not c):
										self.imprimeArray(e)
								if(c):
									if(isthere_rules[1][0]):
										(c, e, a, arquivo) = self.isthere1_fourDados(arquivo, isthere_rules[1][1], isthere_rules[1][2])
										self.imprimeArray(a)
										if(not c):
											self.imprimeArray(e)
									if(c):
										if(isthere_rules[2][0]):
											(c, e, a, arquivo) = self.isthere2_fourDados(arquivo, isthere_rules[2][1], isthere_rules[2][2])
											self.imprimeArray(a)
											if(not c):
												self.imprimeArray(e)
										if(c):
											if(isthere_rules[1][0]):
												(c, e, a, arquivo) = self.isthere3_fourDados(arquivo, isthere_rules[3][1], isthere_rules[3][2])
												self.imprimeArray(a)
												if(not c):
													self.imprimeArray(e)
											if(c):
												(up, dados1, dados2, dados3) = self.readable_four(arquivo)
							else:
								self.imprimeArray(e)
						else:
							self.imprimeArray(e)
					else:
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, up, dados1, dados2, dados3
								#função responsável pela estrutura doubled // não usada, inacessível
	def trate_doubled(self, arquivo, nome, eixo_rules, isthere_rules):
		upDim1 = []
		upDim2 = []
		arquivo = self.break_doubled(arquivo)
		(c, e, a, arquivo) = self.clean_doubled(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_doubled(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_doubled(arquivo)
				if(c):
					(c, e, a, arquivo) = self.isthere_doubled(arquivo, isthere_rules[0], isthere_rules[1])
					self.imprimeArray(a)
					if(not c):
						self.imprimeArray(e)
					if(c):
						(upDim1, upDim2) = self.readable_doubled(arquivo)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, upDim1, upDim2
								#função responsável pela estrutura single
	def trate_especialSingle(self, arquivo, nome, eixo_rules, readable_rules):
		upDim1 = []
		upDim2 = []
		dadosDim1 = []
		dadosDim2 = []
		arquivo = self.break_especialSingle(arquivo)
		(c, e, a, arquivo) = self.clean_especialSingle(arquivo, nome)
		self.imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = self.eixo_especialSingleUp(arquivo, eixo_rules)
			self.imprimeArray(a)
			if(c):
				(c, e, arquivo) = self.dontrepete_especialSingleUp(arquivo)
				if(c):
					(c, e, upDim1, upDim2) = self.readable_especialSingle(arquivo, readable_rules)
					if(not c):
						self.imprimeArray(e)
				else:
					self.imprimeArray(e)
			else:
				self.imprimeArray(e)
		else:
			self.imprimeArray(e)
		return c, upDim1, upDim2
	errosLeituraDados = ""
								#função rsponsável por, de acordo com o arquivo, aplicar o tratamento de estrutura necessário
	def trate(self, fileName, fortxt, forcsv, fortwocsv, fortwotxt):
		self.errosLeituraDados = ""
		inverte = 0
		(iscsv, ismorethantwo) = self.fileTipe(fileName)
		if(iscsv == 0 and ismorethantwo == 1 and fortwotxt):
			inverte = fortwotxt[0]
			estrutura = fortwotxt[1]
			parametros = fortwotxt[2:]
		elif(iscsv == 1 and ismorethantwo == 1 and fortwocsv):
			inverte = fortwocsv[0]
			estrutura = fortwocsv[1]
			parametros = fortwocsv[2:]
		elif((iscsv == 1 and ismorethantwo == 0) or (iscsv == 1 and ismorethantwo == 1 and not fortwocsv)):
			inverte = forcsv[0]
			estrutura = forcsv[1]
			parametros = forcsv[2:]
		else:
			inverte = fortxt[0]
			estrutura = fortxt[1]
			parametros = fortxt[2:]
		
		(c, e, file) = self.readFile(fileName)
		if(c):
			if(estrutura == 0):
				(c, right, down, dadosDim1, dadosDim2) = self.trate_matriz(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5])
				if(len(parametros) == 7):
					if(parametros[6]):
						dadosDim1 = self.func_transpor(dadosDim1, right, down)
						dadosDim2 = self.func_transpor(dadosDim2, right, down)
				if(inverte):
					aux = right
					right = down
					down = aux
				return c, right, down, dadosDim1, dadosDim2
			elif(estrutura == 1):
				(c, up, down, dadosDim1, dadosDim2) = self.trate_simple(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5])
				if(inverte):
					aux = up
					up = down
					down = aux
				return c, up, down, dadosDim1, dadosDim2
			elif(estrutura == 2):
				(c, up, down, dadosDim1, dadosDim2) = self.trate_complex(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5], parametros[6])
				if(inverte):
					aux = up
					up = down
					down = aux
				return c, up, down, dadosDim1, dadosDim2
			elif(estrutura == 3):
				(c, up, down, dadosDim1, dadosDim2) = self.trate_couple(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4])
				if(inverte):
					aux = up
					up = down
					down = aux
				return c, up, down, dadosDim1, dadosDim2
			elif(estrutura == 5): #REPARE O 5
				(c, dados) = self.trate_line(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3])
				return c, dados
			elif(estrutura == 6): #REPARE O 6
				(c, up, dados1, dados2, dados3) = self.trate_four(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3])
				return c, up, dados1, dados2, dados3
			elif(estrutura == 7): #REPARE O 7
				(c, upDim1, upDim2) = self.trate_especialSingle(file, fileName, parametros[0], parametros[1])
				return c, upDim1, upDim2
			else:
				(c, dadosDim1, dadosDim2) = self.trate_single(file, fileName, parametros[0])
				return c, dadosDim1, dadosDim2
		else:
			self.imprimeArray(e)
		if(estrutura > 3 and estrutura != 6 and estrutura != 5):
			return c, 0, 0
		elif(estrutura == 5):
			return c, 0
		else:
			return c, 0, 0, 0, 0

	##################################################################################################
	#							Fim
	##################################################################################################

class App(pacotePadraoClass):

	corPadrao = "#ffdf80"
	FcorPadrao = "#000000"
	
	corBot1 = "#c3c388"
	FcorBot1 = "#000000"
	corBot2 = "#ffcc80"
	FcorBot2 = "#000000"
	corBot3 = "#ffb3b3"
	FcorBot3 = "#000000"
	
	corBotRetorno = "#9999ff"
	FcorBotRetorno = "#000000"
	corBotSeguir = "#00ff00"
	FcorBotSeguir = "#000000"
	
	corErro1 = "#ffb3b3"
	FcorErro1 = "#000000"
	corErro2 = "#ffff00"
	FcorErro2 = "#000000"
	corCerto = "#00802b"
	FcorCerto = "#000000"
	
	corOpL = "#00b300"
	FcorOpL = "#000000"
	corOpD = "#9494b8"
	FcorOpD = "#000000"
	
	screen_width = ""
	screen_height = ""
		
	def secondStandard(self):
		
		real = str(self.instancia.geometry()).split("+")
		real = real[0].split("x")
	
		self.screen_width = int(real[0])
		self.screen_height = int(real[1])
	
	def firstStandard(self):
	
		self.screen_width = int(self.instancia.winfo_screenwidth())
		self.screen_height = int(self.instancia.winfo_screenheight())
			
	wsb_a = 0
	wsb_b = 0
			
	def createMain(self, escolhido):
	
		self.cleanContainer(self.instancia)
		
		self.fontePadrao30 = "Times "+str(int(self.screen_height*0.05))
		self.fontePadrao20 = "Times "+str(int(self.screen_height*0.035))
		self.fontePadrao15 = "Times "+str(int(self.screen_height*0.025))
		
		self.wraplengthPadrao1 = int(self.screen_width)#*0.7)
		self.wraplengthPadrao2 = int(self.screen_width)#*0.5)
		
		if(escolhido == 1):
			
			self.instancia.geometry("+%d+%d" % (int(self.screen_width*0.05), int(self.screen_height*0.05)))
		
		self.container_A = Frame(self.instancia, bg = self.corPadrao)
		self.container_B = Frame(self.instancia, bg = self.corPadrao)
		
		if(escolhido == 1):
			if(self.wsb_a != 0 and self.wsb_b != 0):
				self.instancia.geometry("%dx%d" % (int(self.screen_width*0.9) + self.wsb_a, int(self.screen_height*0.8) + self.wsb_b))
			self.canvasA = Canvas(self.container_A, bg = self.corPadrao, width = int(self.screen_width*0.9), height = int(self.screen_height*0.8))
		else:
			if(self.screen_width > self.wsb_a and self.screen_height > self.wsb_b):
				self.canvasA = Canvas(self.container_A, bg = self.corPadrao, width = int(self.screen_width) - self.wsb_a, height = int(self.screen_height) - self.wsb_b)
			
		self.scrollbarA = Scrollbar(self.container_A, orient = "vertical", command = self.canvasA.yview)
		self.scrollbarB = Scrollbar(self.container_B, orient = "horizontal", command = self.canvasA.xview)
		self.containerA = Frame(self.canvasA, bg = self.corPadrao)
		self.containerA.bind(
			"<Configure>", lambda e: self.canvasA.configure(
				scrollregion = self.canvasA.bbox("all")
			)
		)
		self.canvasA.create_window(int(self.screen_width*0.45), 0, window = self.containerA, anchor = N)
		self.canvasA.configure(yscrollcommand = self.scrollbarA.set)
		self.canvasA.configure(xscrollcommand = self.scrollbarB.set)
		self.canvasA.pack(side = LEFT, fill = BOTH, expand = 1)
		self.scrollbarA.pack(side = RIGHT, fill = "y", expand = 1)
		self.scrollbarB.pack(fill = "x", expand = 1)
		self.container_A.pack()
		self.container_B.pack(fill = "x", expand = 1)
		self.wsb_a = int(self.scrollbarA["width"])+2*int(self.scrollbarA["bd"])
		self.wsb_b = int(self.scrollbarB["width"])+2*int(self.scrollbarA["bd"])
		
		self.instancia.resizable(0, 0)
		
		self.container1 = Frame(self.containerA, bg = self.corPadrao)
		self.container2 = Frame(self.containerA, bg = self.corPadrao)
		self.container3 = Frame(self.containerA, bg = self.corPadrao)
		self.container4 = Frame(self.containerA, bg = self.corPadrao)
		
		self.screens(1)
				
	def setResolucao(self):
		
		self.secondStandard()
		
		self.createMain(2)
				
	def setFirst(self):
		
		self.firstStandard()
		
		self.createMain(1)
		
	def changeResolucao(self):
	
		self.cleanContainer(self.instancia)
		self.instancia["bg"] = self.corPadrao
		if(self.screen_width == int(self.instancia.winfo_screenwidth()) and self.screen_height == int(self.instancia.winfo_screenheight())):
			self.container1 = Frame(self.instancia, bg = self.corPadrao, width = self.screen_width*0.9, height = self.screen_height*0.8)
		else:
			self.container1 = Frame(self.instancia, bg = self.corPadrao, width = self.screen_width, height = self.screen_height)
		self.container1.pack()
		self.container1.pack_propagate(0)
		Label(self.container1, text = "Agora o tamanho da janela pode ter seu tamanho modificado", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1)
		Button(self.container1, text = "Pronto!", bg = self.corBot1, fg = self.FcorBot1, font = self.fontePadrao15, wraplength = self.wraplengthPadrao1, command = self.setResolucao).pack(fill = "x", expand = 1)
		Button(self.container1, text = "Restaurar", bg = self.corBot2, fg = self.FcorBot2, font = self.fontePadrao15, wraplength = self.wraplengthPadrao1, command = self.setFirst).pack(fill = "x", expand = 1)
		
		self.instancia.resizable(1, 1)

	def __init__(self, instancia):
	
		self.instancia = instancia
		
		self.instancia.title("Salas para Aulas")
		
		self.firstStandard()
		self.createMain(1)
		
	def cleanContainer(self, container):
	
		criancas = container.winfo_children()
		
		for crianca in criancas:
		
			crianca.destroy()
	
	def limpa(self):
	
		self.cleanContainer(self.container1)
		self.cleanContainer(self.container2)
		self.cleanContainer(self.container3)
		self.cleanContainer(self.container4)
		
		self.container1.pack_forget()
		self.container2.pack_forget()
		self.container3.pack_forget()
		self.container4.pack_forget()
		
		self.scrollbarA.pack_forget()
		self.scrollbarB.pack_forget()
		
		self.scrollbarA = Scrollbar(self.container_A, orient = "vertical", command = self.canvasA.yview)
		self.scrollbarB = Scrollbar(self.container_B, orient = "horizontal", command = self.canvasA.xview)
		self.canvasA.create_window(int(self.screen_width*0.45), 0, window = self.containerA, anchor = N)
		self.canvasA.configure(yscrollcommand = self.scrollbarA.set)
		self.canvasA.configure(xscrollcommand = self.scrollbarB.set)
		self.scrollbarA.pack(side = RIGHT, fill = "y", expand = 1)
		self.scrollbarB.pack(fill = "x", expand = 1)
				
	def screens(self, pagina):
	
		self.limpa()
		
		if(pagina == 1):
		
			Label(self.container1, text = "Aulas em Salas", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao30, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, pady = self.screen_height*0.03)
			Button(self.container1, text = "Acessar projetos", bg = self.corBot1, fg = self.FcorBot1, command = self.screens2, font = self.fontePadrao20).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			Button(self.container1, text = "Ampliar tela", bg = self.corBot2, fg = self.FcorBot2, command = self.changeResolucao, font = self.fontePadrao20).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.container1.pack(fill = BOTH, expand = 1)
		
		elif(pagina == 2):
		
			Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens1, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			Label(self.container1, text = "Pasta do Projeto", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao30, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, side = RIGHT, pady = self.screen_height*0.03)
			
			self.entrada = ttk.Combobox(self.container2, font = self.fontePadrao20)
			listaDirs = [i[0] for i in os.walk(".")]
			listaDirs.remove(".")
			for i in range(len(listaDirs)):
				while(listaDirs[i][0] != "\\"):
					listaDirs[i] = listaDirs[i][1:]
				listaDirs[i] = listaDirs[i][1:]
			self.entrada["values"] = listaDirs
			self.entrada.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			self.entrada.focus()
			self.aviso = Label(self.container2, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao20, wraplength = self.wraplengthPadrao1)
			self.aviso.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			Button(self.container2, text = "Seguir", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide2, font = self.fontePadrao20).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.container1.pack(fill = BOTH, expand = 1)
			self.container2.pack(fill = BOTH, expand = 1)
			
		elif(pagina == 3):
		
			Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens2, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			Label(self.container1, text = "Arquivo de configurações principal", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao20, wraplength = self.wraplengthPadrao1).pack(fill = "x", expand = 1, side = RIGHT, pady = self.screen_height*0.03)
		
			self.opcao1 = Button(self.container2, text = "Utilizar", bg = self.corOpL, fg = self.FcorOpL, font = self.fontePadrao15, command = self.Popcao1)
			self.opcao1.grid(column = 0, row = 1, pady = 15)
			self.opcao2 = Button(self.container2, text = "Criar", bg = self.corOpD, fg = self.FcorOpD, font = self.fontePadrao15, command = self.Popcao2)
			self.opcao2.grid(column = 1, row = 1, pady = 15)
			
			'''----------------------------------------------------------------'''
			
			self.entradaU = ttk.Combobox(self.container3, font = self.fontePadrao20)
			listaFiles = os.listdir(os.getcwd()+"/"+self.pastaProjeto)
			self.entradaU["values"] = listaFiles
			self.entradaU.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			self.entradaU.focus()
			self.avisoA = Label(self.container3, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao1)
			self.avisoA.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			Button(self.container3, text = "Seguir", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide3a, font = self.fontePadrao15).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			#----------------------------------------------------------------
			
			self.tmprr_frame1 = Frame(self.container4, bg = self.corPadrao)
			self.tmprr_frame1a = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1b = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1c = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1d = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1e = Frame(self.tmprr_frame1, bg = self.corPadrao)
			
			listaDirs = [i[0] for i in os.walk("./"+self.pastaProjeto)]
			listaDirs.remove("./"+self.pastaProjeto)
			for i in range(len(listaDirs)):
				while(listaDirs[i][0] != "\\"):
					listaDirs[i] = listaDirs[i][1:]
				listaDirs[i] = listaDirs[i][1:]
			listaFiles = os.listdir(os.getcwd()+"/"+self.pastaProjeto)
			
			Label(self.tmprr_frame1a, text = "Nome do arquivo", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			self.entrada1 = ttk.Combobox(self.tmprr_frame1a, font = self.fontePadrao15)
			self.entrada1["values"] = listaFiles
			self.entrada1.pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			self.entrada1.focus
			
			Label(self.tmprr_frame1b, text = "Pasta com os dados", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			self.entrada2 = ttk.Combobox(self.tmprr_frame1b, font = self.fontePadrao15)
			self.entrada2["values"] = listaDirs
			self.entrada2.pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			Label(self.tmprr_frame1c, text = "Pasta para imprimir a resposta", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			self.entrada3 = ttk.Combobox(self.tmprr_frame1c, font = self.fontePadrao15)
			self.entrada3["values"] = listaDirs
			self.entrada3.pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			Label(self.tmprr_frame1d, text = "Nome do arquivo com a lista dos arquivos de dados", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2).pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			self.entrada4 = ttk.Combobox(self.tmprr_frame1d, font = self.fontePadrao15)
			self.entrada4["values"] = listaFiles
			self.entrada4.pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			self.avisoB = Label(self.tmprr_frame1e, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao1)
			self.avisoB.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			Button(self.tmprr_frame1e, text = "Seguir", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide3b, font = self.fontePadrao15).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.container1.pack(fill = BOTH, expand = 1)
			self.container2.pack(fill = BOTH, expand = 1)
			
			self.tmprr_frame1a.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1b.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1c.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1d.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1e.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1.pack(fill = BOTH, expand = 1)
			
			self.Popcao1()
			
		elif(pagina == 4):
			
			self.tmprr_frame1 = Frame(self.container2, bg = self.corPadrao)
			self.tmprr_frame1a = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1b = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1c = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1d = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1e = Frame(self.tmprr_frame1, bg = self.corPadrao)
		
			Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens3, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			Label(self.container1, text = "Checando os dados gerais", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao20, wraplength = self.wraplengthPadrao1).pack(fill = "x", expand = 1, side = RIGHT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			
			self.holds_file0 = Label(self.tmprr_frame1a, text = "Arquivo com os IDs dos horários: "+self.getValue(self.entradasLista, "HorariosId"), bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.holds_file0.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			self.help_file0 = Label(self.tmprr_frame1a, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.help_file0.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01)
			Button(self.tmprr_frame1a, text = "Validar", bg = "#4d79ff", command = self.valide_files0, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01)
			
			self.holds_file1 = Label(self.tmprr_frame1b, text = "Arquivo com a grade horária: "+self.getValue(self.entradasLista, "GradeHoraria"), bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.holds_file1.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			self.help_file1 = Label(self.tmprr_frame1b, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.help_file1.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01)
			Button(self.tmprr_frame1b, text = "Validar", bg = "#4d79ff", command = self.valide_files1, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01)
			
			if(self.getValue(self.entradasLista, "SalasCapacidades") != ""):
				self.holds_file2 = Label(self.tmprr_frame1c, text = "Arquivo com o número de assentos das salas: "+self.getValue(self.entradasLista, "SalasCapacidades"), bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.holds_file2.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				self.help_file2 = Label(self.tmprr_frame1c, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.help_file2.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01)
				Button(self.tmprr_frame1c, text = "Validar", bg = "#4d79ff", command = self.valide_files2, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01)
			
			if(self.getValue(self.entradasLista, "DisciplinasTamanhos") != ""):
				self.holds_file3 = Label(self.tmprr_frame1d, text = "Arquivo com a quantidade de alunos das turmas: "+self.getValue(self.entradasLista, "DisciplinasTamanhos"), bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.holds_file3.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				self.help_file3 = Label(self.tmprr_frame1d, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.help_file3.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01)
				Button(self.tmprr_frame1d, text = "Validar", bg = "#4d79ff", command = self.valide_files3, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01)
			
			self.botao = Button(self.tmprr_frame1e, text = "Validar todos", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide_AllFiles4, font = self.fontePadrao15)
			self.botao.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.container1.pack(fill = BOTH, expand = 1)
			self.container2.pack(fill = BOTH, expand = 1)
			
			self.tmprr_frame1a.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1b.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1c.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1d.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1e.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1.pack(fill = BOTH, expand = 1)
			
		elif(pagina == 5):
			
			if(self.entradasLista[4][1] == "" and self.entradasLista[5][1] == "" and self.entradasLista[6][1] == ""):
			 
				if(self.entradasLista[7][1] == "" and self.entradasLista[8][1] == "" and self.entradasLista[9][1] == ""):
			
					self.screens(7)
					
				else:
				
					self.screens(6)
				
			else:
		
				self.tmprr_frame1 = Frame(self.container2, bg = self.corPadrao)
				self.tmprr_frame1a = Frame(self.tmprr_frame1, bg = self.corPadrao)
				self.tmprr_frame1b = Frame(self.tmprr_frame1, bg = self.corPadrao)
				self.tmprr_frame1c = Frame(self.tmprr_frame1, bg = self.corPadrao)
				self.tmprr_frame1d = Frame(self.tmprr_frame1, bg = self.corPadrao)
			
				Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens4, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
				Label(self.container1, text = "Checando os dados relacionados aos recursos", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao20, wraplength = self.wraplengthPadrao1).pack(fill = "x", expand = 1, side = RIGHT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
				
				if(self.getValue(self.entradasLista, "SalasRecursos") != ""):
					self.holds_file4 = Label(self.tmprr_frame1a, text = "Arquivo com os recursos presentes nas salas: "+self.files[4], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.holds_file4.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
					self.help_file4 = Label(self.tmprr_frame1a, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.help_file4.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
					Button(self.tmprr_frame1a, text = "Validar", bg = "#4d79ff", command = self.valide_files4, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				
				if(self.getValue(self.entradasLista, "DisciplinasRecursos") != ""):
					self.holds_file5 = Label(self.tmprr_frame1b, text = "Arquivo com os recursos demandados pelas turmas: "+self.files[5], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.holds_file5.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
					self.help_file5 = Label(self.tmprr_frame1b, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.help_file5.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
					Button(self.tmprr_frame1b, text = "Validar", bg = "#4d79ff", command = self.valide_files5, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				
				if(self.getValue(self.entradasLista, "SalasPref") != ""):
					self.holds_file6 = Label(self.tmprr_frame1c, text = "Arquivo com a preferência das salas: "+self.files[6], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.holds_file6.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
					self.help_file6 = Label(self.tmprr_frame1c, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
					self.help_file6.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
					Button(self.tmprr_frame1c, text = "Validar", bg = "#4d79ff", command = self.valide_files6, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				
				self.botao = Button(self.tmprr_frame1d, text = "Validar todos", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide_AllFiles5, font = self.fontePadrao15)
				self.botao.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				
				self.container1.pack(fill = BOTH, expand = 1)
				self.container2.pack(fill = BOTH, expand = 1)
				
				self.tmprr_frame1a.pack(fill = BOTH, expand = 1)
				self.tmprr_frame1b.pack(fill = BOTH, expand = 1)
				self.tmprr_frame1c.pack(fill = BOTH, expand = 1)
				self.tmprr_frame1d.pack(fill = BOTH, expand = 1)
				self.tmprr_frame1.pack(fill = BOTH, expand = 1)

		elif(pagina == 6):
		
			self.tmprr_frame1 = Frame(self.container2, bg = self.corPadrao)
			self.tmprr_frame1a = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1b = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1c = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1d = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1e = Frame(self.tmprr_frame1, bg = self.corPadrao)
		
			if(self.entradasLista[4][1] != "" or self.entradasLista[5][1] != "" or self.entradasLista[6][1] != ""):
				Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens5, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			else:
				Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens4, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
		
			Label(self.container1, text = "Checando os dados relacionados aos currículos", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao20, wraplength = self.wraplengthPadrao1).pack(side = RIGHT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			
			if(self.getValue(self.entradasLista, "CurriculosDisciplinas") != ""):
				self.holds_file7 = Label(self.tmprr_frame1a, text = "Arquivo com a relação entre os currículos e as turmas: "+self.files[7], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.holds_file7.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				self.help_file7 = Label(self.tmprr_frame1a, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.help_file7.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				Button(self.tmprr_frame1a, text = "Validar", bg = "#4d79ff", command = self.valide_files7, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			if(self.getValue(self.entradasLista, "CurriculosSalas") != ""):
				self.holds_file8 = Label(self.tmprr_frame1b, text = "Arquivo com as salas preferidas dos currículos: "+self.files[8], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.holds_file8.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				self.help_file8 = Label(self.tmprr_frame1b, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.help_file8.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				Button(self.tmprr_frame1b, text = "Validar", bg = "#4d79ff", command = self.valide_files8, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			if(self.getValue(self.entradasLista, "Distancias") != ""):
				self.holds_file9 = Label(self.tmprr_frame1c, text = "Arquivo com as distâncias das salas: "+self.files[9], bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.holds_file9.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
				self.help_file9 = Label(self.tmprr_frame1c, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
				self.help_file9.pack(fill = "x", expand = 1, side = LEFT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
				Button(self.tmprr_frame1c, text = "Validar", bg = "#4d79ff", command = self.valide_files9, font = self.fontePadrao15).pack(side = RIGHT, pady = self.screen_height*0.01, padx = self.screen_width*0.01)
			
			self.botao = Button(self.tmprr_frame1e, text = "Validar todos", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.valide_AllFiles6, font = self.fontePadrao15)
			self.botao.pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.container1.pack(fill = BOTH, expand = 1)
			self.container2.pack(fill = BOTH, expand = 1)
			
			self.tmprr_frame1a.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1b.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1c.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1d.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1e.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1.pack(fill = BOTH, expand = 1)
			
		elif(pagina == 7):
		
			self.tmprr_frame1 = Frame(self.container2, bg = self.corPadrao)
			self.tmprr_frame1a = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1b = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1c = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1d = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1e = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1f = Frame(self.tmprr_frame1, bg = self.corPadrao)
			self.tmprr_frame1g = Frame(self.tmprr_frame1, bg = self.corPadrao)
		
			if(self.entradasLista[7][1] != "" or self.entradasLista[8][1] != "" or self.entradasLista[9][1] != ""):
				Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens6, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			else:
				if(self.entradasLista[4][1] != "" or self.entradasLista[5][1] != "" or self.entradasLista[6][1] != ""):
					Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens5, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
				else:
					Button(self.container1, text = "Retornar", bg = self.corBotRetorno, fg = self.FcorBotRetorno, command = self.screens4, font = self.fontePadrao20).pack(side = LEFT, pady = self.screen_height*0.03, padx = self.screen_width*0.01)
			Label(self.container1, text = "Resolver", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao30, wraplength = self.wraplengthPadrao1).pack(fill = "x", expand = 1, pady = self.screen_height*0.01)
			
			self.constante0 = Scale(self.tmprr_frame1a, resolution = 1, label = "Valor da constante 'USO'", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 100, bg = self.corPadrao, fg = self.FcorPadrao)
			if(self.entradasLista[2][1] != "" and self.entradasLista[3][1] != ""):
				self.constante0.pack(fill = "x", expand = 1)
				Button(self.tmprr_frame1a, text = "Diminuir escala", command = self.scaleMenos0).pack(fill = "x", expand = 1, side = LEFT)
				Button(self.tmprr_frame1a, text = "Aumentar escala", command = self.scaleMais0).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.constante1 = Scale(self.tmprr_frame1b, resolution = 1, label = "Valor da constante 'TROCAS'", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 100, bg = self.corPadrao, fg = self.FcorPadrao)
			self.constante1.pack(fill = "x", expand = 1)
			Button(self.tmprr_frame1b, text = "Diminuir escala", command = self.scaleMenos1).pack(fill = "x", expand = 1, side = LEFT)
			Button(self.tmprr_frame1b, text = "Aumentar escala", command = self.scaleMais1).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.constante2 = Scale(self.tmprr_frame1c, resolution = 1, label = "Valor da constante 'DISTANCIAS'", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 100, bg = self.corPadrao, fg = self.FcorPadrao)
			if(self.entradasLista[7][1] != "" and self.entradasLista[9][1] != ""):
				self.constante2.pack(fill = "x", expand = 1)
				Button(self.tmprr_frame1c, text = "Diminuir escala", command = self.scaleMenos2).pack(fill = "x", expand = 1, side = LEFT)
				Button(self.tmprr_frame1c, text = "Aumentar escala", command = self.scaleMais2).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.constante3 = Scale(self.tmprr_frame1d, resolution = 1, label = "Valor da constante 'OCUPACAO'", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 100, bg = self.corPadrao, fg = self.FcorPadrao)
			if(self.entradasLista[6][1] != ""):
				self.constante3.pack(fill = "x", expand = 1)
				Button(self.tmprr_frame1d, text = "Diminuir escala", command = self.scaleMenos3).pack(fill = "x", expand = 1, side = LEFT)
				Button(self.tmprr_frame1d, text = "Aumentar escala", command = self.scaleMais3).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.constante4 = Scale(self.tmprr_frame1e, resolution = 1, label = "Valor da constante 'CURRICULOS'", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 100, bg = self.corPadrao, fg = self.FcorPadrao)
			if(self.entradasLista[7][1] != "" and self.entradasLista[8][1] != ""):
				self.constante4.pack(fill = "x", expand = 1)
				Button(self.tmprr_frame1e, text = "Diminuir escala", command = self.scaleMenos4).pack(fill = "x", expand = 1, side = LEFT)
				Button(self.tmprr_frame1e, text = "Aumentar escala", command = self.scaleMais4).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.tempo = Scale(self.tmprr_frame1f, resolution = 1, label = "Tempo para solução em minutos", font = self.fontePadrao15, orient = HORIZONTAL, from_ = 0, to = 60, bg = self.corPadrao, fg = self.FcorPadrao)
			self.tempo.pack(fill = "x", expand = 1)
			Button(self.tmprr_frame1f, text = "Diminuir escala", command = self.scaleMenosTempo).pack(fill = "x", expand = 1, side = LEFT)
			Button(self.tmprr_frame1f, text = "Aumentar escala", command = self.scaleMaisTempo).pack(fill = "x", expand = 1, side = RIGHT)
			
			self.botao2 = Button(self.tmprr_frame1g, text = "Resolver Modelo", bg = self.corBotSeguir, fg = self.FcorBotSeguir, command = self.resolverModelo, font = self.fontePadrao15)
			self.botao2.pack(fill = "x", expand = 1)
			
			self.impressao1 = Label(self.tmprr_frame1g, text = "", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao1)
			self.impressao1.pack(side = LEFT, pady = self.screen_height*0.01)
			self.impressora1 = Button(self.tmprr_frame1g, text = "Salvar a solução encontrada do problema ", bg = "#b3b3ff", command = self.imprimir, font = self.fontePadrao15, state = "disabled")
			self.impressora1.pack(fill = "x", expand = 1, side = RIGHT)
			
			self.solucao = Label(self.container3, text = "Ainda não temos uma solução", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.solucao.pack(fill = BOTH, expand = 1)
			self.analise = Label(self.container3, text = "Ainda não temos uma análise de solução", bg = self.corPadrao, fg = self.FcorPadrao, font = self.fontePadrao15, wraplength = self.wraplengthPadrao2)
			self.analise.pack(fill = BOTH, expand = 1)
			
			self.container1.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1a.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1b.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1c.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1d.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1e.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1f.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1g.pack(fill = BOTH, expand = 1)
			self.tmprr_frame1.pack(fill = BOTH, expand = 1)
			self.container2.pack(side = LEFT, fill = BOTH, expand = 1)
			self.container3.pack(side = RIGHT, fill = BOTH, expand = 1)
		
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	def screens0(self):
	
		self.screens(0)
			
	def screens1(self):
	
		self.screens(1)
			
	def screens2(self):
	
		self.screens(2)
		
	def screens3(self):
	
		self.screens(3)
		
	def screens4(self):
	
		self.screens(4)
		
	def screens5(self):
	
		self.screens(5)
		
	def screens6(self):
	
		self.screens(6)
	
	def screens7(self):
	
		self.screens(7)
			
	def scaleMais(self, qual):
	
		quais = [self.constante0, self.constante1, self.constante2, self.constante3, self.constante4]
		
		quais[qual]["to"] = quais[qual]["to"]*10
		
	def scaleMenos(self, qual):
	
		quais = [self.constante0, self.constante1, self.constante2, self.constante3, self.constante4]
		
		if(quais[qual]["to"] > 10):
			
			quais[qual]["to"] = quais[qual]["to"]/10
		
	def scaleMais0(self):
	
		self.scaleMais(0)
		
	def scaleMais1(self):
	
		self.scaleMais(1)
		
	def scaleMais2(self):
	
		self.scaleMais(2)
		
	def scaleMais3(self):
	
		self.scaleMais(3)
		
	def scaleMais4(self):
	
		self.scaleMais(4)
		
	def scaleMaisTempo(self):
	
		self.tempo["to"] = self.tempo["to"]+60
		
	def scaleMenos0(self):
	
		self.scaleMenos(0)
		
	def scaleMenos1(self):
	
		self.scaleMenos(1)
		
	def scaleMenos2(self):
	
		self.scaleMenos(2)
		
	def scaleMenos3(self):
	
		self.scaleMenos(3)
		
	def scaleMenos4(self):
	
		self.scaleMenos(4)
		
	def scaleMenosTempo(self):
	
		if(self.tempo["to"] > 60):
		
			self.tempo["to"] = self.tempo["to"]-60
		
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	def Popcao1(self):
	
		self.opcao1["bg"] = self.corOpL
		self.opcao1["fg"] = self.FcorOpL
		self.opcao2["bg"] = self.corOpD
		self.opcao2["fg"] = self.FcorOpD
		
		self.container3.pack(fill = BOTH, expand = 1)
		self.container4.pack_forget()
		
	def Popcao2(self):
	
		self.opcao1["bg"] = self.corOpD
		self.opcao1["fg"] = self.FcorOpD
		self.opcao2["bg"] = self.corOpL
		self.opcao2["fg"] = self.FcorOpL
		
		self.container3.pack_forget()
		self.container4.pack(fill = BOTH, expand = 1)
	
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	pastaProjeto = ""
	
	def valide2(self):
	
		if(os.path.isdir(self.entrada.get()) and self.entrada.get().strip() != ""):
		
			self.pastaProjeto = self.entrada.get()
			self.screens(3)
			
		elif(self.entrada.get().strip() == ""):
		
			self.aviso["text"] = "Não foi indicada nenhuma pasta"
			
		else:
		
			self.aviso["text"] = "A pasta indicada não existe"
	
	def valide3a(self):
	
		self.valide3File_MainSettings()
		
	def valide3b(self):
	
		self.valide3Here_MainSettings()
	
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	def controle_Botao4(self):
	
		if(self.holds_file0["bg"] == "#00cc66" and self.holds_file1["bg"] == "#00cc66"):
			if((self.holds_file2["bg"] == "#00cc66" and self.getValue(self.entradasLista, "SalasCapacidades") != "" and self.holds_file3["bg"] == "#00cc66" and self.getValue(self.entradasLista, "DisciplinasTamanhos") != "") or (self.getValue(self.entradasLista, "SalasCapacidades") == "" and self.getValue(self.entradasLista, "DisciplinasTamanhos") == "")):
		
				return 1
			
		else:
			
			return 0
		
	def valide_AllFiles4(self):
	
		self.valide_files0()
		self.valide_files1()
		self.valide_files2()
		self.valide_files3()
		
		if(self.controle_Botao4()):
		
			self.screens(5)
		
	def valide_files0(self):
	
		self.holds_file0["bg"] = self.corPadrao
	
		analise = self.valideFiles0()
	
		if(analise):
		
			self.holds_file0["bg"] = "#00cc66"
			self.help_file0["text"] = ""
			self.help_file0["bg"] = self.corPadrao
			
		else:
			
			self.help_file0["bg"] = self.corErro1
			
	def valide_files1(self):
	
		self.holds_file1["bg"] = self.corPadrao
		
		if(self.holds_file0["bg"] == "#00cc66"):
	
			analise = self.valideFiles1()
			
			if(analise):
			
				self.holds_file1["bg"] = "#00cc66"
				self.help_file1["text"] = ""
				self.help_file1["bg"] = self.corPadrao
				
			else:
					
				self.help_file1["bg"] = self.corErro1
				
		elif(self.holds_file0["bg"] == self.corPadrao):
		
			self.help_file1["text"] = "Só é possível ler grade horária quando os IDs dos slots forem lidos"
			self.help_file1["bg"] = "#ffff33"
			
		else:
		
			self.help_file1["text"] = "Só é possível ler a grade horária quando é lido um arquivo válido com os IDs dos slots"
			self.help_file1["bg"] = "#ffff33"
			
	def valide_files2(self):
	
		self.holds_file2["bg"] = self.corPadrao
	
		analise = self.valideFiles2()
		
		if(analise):
		
			self.holds_file2["bg"] = "#00cc66"
			self.help_file2["text"] = ""
			self.help_file2["bg"] = self.corPadrao
			
		else:
				
			self.help_file2["bg"] = self.corErro1
			
	def valide_files3(self):
	
		self.holds_file3["bg"] = self.corPadrao
	
		if(self.holds_file2["bg"] == "#00cc66"):
		
			if(self.holds_file1["bg"] == "#00cc66"):
		
				analise = self.valideFiles3()
					
				if(analise):
					
					self.holds_file3["bg"] = "#00cc66"
					self.help_file3["text"] = ""
					self.help_file3["bg"] = self.corPadrao
						
				else:
					
					self.help_file3["bg"] = self.corErro1
					
			elif(self.holds_file1["bg"] == self.corPadrao):
		
				self.help_file3["text"] = "Só é possível ler o tamanho das turmas quando a grade horária for lida"
				self.help_file3["bg"] = "#ffff33"
				
			else:
			
				self.help_file3["text"] = "Só é possível ler o tamanho das turmas quando é lido um arquivo válido com a grade horária"
				self.help_file3["bg"] = "#ffff33"
				
		elif(self.holds_file2["bg"] == self.corPadrao):
		
			self.help_file3["text"] = "Só é possível ler o tamanho das turmas quando a capacidade das salas forem lidos"
			self.help_file3["bg"] = "#ffff33"
			
		else:
		
			self.help_file3["text"] = "Só é possível ler o tamanho das turmas quando é lido um arquivo válido com a capacidade das salas"
			self.help_file3["bg"] = "#ffff33"
					
	def controle_Botao5(self):
	
		if(self.holds_file6["bg"] == "#00cc66" or self.getValue(self.entradasLista, "SalasPref") == ""):
		
			if((self.holds_file4["bg"] == "#00cc66" and self.getValue(self.entradasLista, "SalasRecursos") != "" and self.holds_file5["bg"] == "#00cc66" and self.getValue(self.entradasLista, "DisciplinasRecursos") != "") or (self.getValue(self.entradasLista, "SalasRecursos") == "" and self.getValue(self.entradasLista, "DisciplinasRecursos") == "")):
		
				return 1
			
		else:
			
			return 0
		
	def valide_AllFiles5(self):
	
		self.valide_files4()
		self.valide_files5()
		self.valide_files6()
		
		if(self.controle_Botao5()):
		
			self.screens(6)
		
	def valide_files4(self):
	
		self.holds_file4["bg"] = self.corPadrao
	
		analise = self.valideFiles4()
	
		if(analise):
		
			self.holds_file4["bg"] = "#00cc66"
			self.help_file4["text"] = ""
			self.help_file4["bg"] = self.corPadrao
			
		else:
					
			self.help_file4["bg"] = self.corErro1
			
	def valide_files5(self):
	
		self.holds_file5["bg"] = self.corPadrao
	
		if(self.holds_file4["bg"] == "#00cc66"):
	
			analise = self.valideFiles5()
		
			if(analise):
			
				self.holds_file5["bg"] = "#00cc66"
				self.help_file5["text"] = ""
				self.help_file5["bg"] = self.corPadrao
				
			else:
					
				self.help_file5["bg"] = self.corErro1
			
		elif(self.holds_file4["bg"] == self.corPadrao):
		
			self.help_file5["text"] = "Só é possível ler os recursos das turmas quando os recursos das salas forem lidos"
			self.help_file5["bg"] = "#ffff33"
			
		else:
		
			self.help_file5["text"] = "Só é possível ler os recursos das turmas quando é lido um arquivo válido com os recursos das salas"
			self.help_file5["bg"] = "#ffff33"
			
	def valide_files6(self):
	
		self.holds_file6["bg"] = self.corPadrao
	
		analise = self.valideFiles6()
		
		if(analise):
			
			self.holds_file6["bg"] = "#00cc66"
			self.help_file6["text"] = ""
			self.help_file6["bg"] = self.corPadrao
				
		else:
					
			self.help_file6["bg"] = self.corErro1
			
	def controle_Botao6(self):
	
		if(self.holds_file9["bg"] == "#00cc66" or self.getValue(self.entradasLista, "Distancias") == ""):
		
			if((self.holds_file7["bg"] == "#00cc66" and self.getValue(self.entradasLista, "CurriculosDisciplinas") != "" and self.holds_file8["bg"] == "#00cc66" and self.getValue(self.entradasLista, "CurriculosSalas") != "") or (self.getValue(self.entradasLista, "CurriculosDisciplinas") == "" and self.getValue(self.entradasLista, "CurriculosSalas") == "")):
		
				return 1
			
		else:
			
			return 0
		
	def valide_AllFiles6(self):
	
		self.valide_files7()
		self.valide_files8()
		self.valide_files9()
		
		if(self.controle_Botao6()):
		
			self.screens(7)
	
	def valide_files7(self):
	
		self.holds_file7["bg"] = self.corPadrao
	
		analise = self.valideFiles7()
	
		if(analise):
		
			self.holds_file7["bg"] = "#00cc66"
			self.help_file7["text"] = ""
			self.help_file7["bg"] = self.corPadrao
			
		else:
		
			self.help_file7["bg"] = self.corErro1
		
	def valide_files8(self):
	
		self.holds_file8["bg"] = self.corPadrao
	
		if(self.holds_file7["bg"] == "#00cc66"):
	
			analise = self.valideFiles8()
		
			if(analise):
			
				self.holds_file8["bg"] = "#00cc66"
				self.help_file8["text"] = ""
				self.help_file8["bg"] = self.corPadrao
				
			else:
			
				self.help_file8["bg"] = self.corErro1
			
		elif(self.holds_file7["bg"] == self.corPadrao):
		
			self.help_file8["text"] = "Só é possível ler as turmas dos currículos quando os currículos forem lidos"
			self.help_file8["bg"] = "#ffff33"
			
		else:
		
			self.help_file8["text"] = "Só é possível ler as turmas dos currículos quando é lido um arquivo válido com os currículos"
			self.help_file8["bg"] = "#ffff33"
			
	def valide_files9(self):
	
		self.holds_file9["bg"] = self.corPadrao
	
		if(self.holds_file7["bg"] == "#00cc66"):
	
			analise = self.valideFiles9()
		
			if(analise):
			
				self.holds_file9["bg"] = "#00cc66"
				self.help_file9["text"] = ""
				self.help_file9["bg"] = self.corPadrao
				
			else:
			
				self.help_file9["bg"] = self.corErro1
			
		elif(self.holds_file7["bg"] == self.corPadrao):
		
			self.help_file9["text"] = "Só é possível ler as distâncias entre as salas quando os currículos forem lidos"
			self.help_file9["bg"] = "#ffff33"
			
		else:
		
			self.help_file9["text"] = "Só é possível ler as distâncias entre as salas quando é lido um arquivo válido com os currículos"
			self.help_file9["bg"] = "#ffff33"
	
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	mainData = ""
	files = []
	
	def valide3File_MainSettings(self):
	
		mainData = self.readArquivoInicial(self.entradaU.get())
		
		if(mainData[0]):
		
			self.mainData = mainData[1]
			
			nomes_arquivosDados = ["HorariosId","GradeHoraria","SalasCapacidades","DisciplinasTamanhos","SalasRecursos","DisciplinasRecursos","SalasPref","CurriculosDisciplinas","CurriculosSalas","Distancias"]
			(c, g, g, self.entradasLista, g) = self.trate(self.pastaProjeto+"/"+self.mainData[1][0], 
				[0, 3,
					":",
					"texto",
					[1, nomes_arquivosDados, 1],
					[0, "arquivo", self.pastaProjeto+"/"+self.mainData[0][0]],
					[1, nomes_arquivosDados, "", 0]
				],
				[0, 3,
					";",
					"texto",
					[1, nomes_arquivosDados, 1],
					[0, "arquivo", self.pastaProjeto+"/"+self.mainData[0][0]],
					[1, nomes_arquivosDados, "", 0]
				],
				0,
				0
			)
			
			if(c):
			
				if(self.getValue(self.entradasLista, "HorariosId") == ""):
					c = 0
					self.avisoA["text"] = self.avisoA["text"]+"Aviso: Não foi indicado um arquivo com os IDs dos horários na lista de arquivos de dados\n"
				if(self.getValue(self.entradasLista, "GradeHoraria") == ""):
					c = 0
					self.avisoA["text"] = self.avisoA["text"]+"Aviso: Não foi indicado um arquivo com a grade horária das turmas na lista de arquivos de dados\n"
				
				if(c):
				
					self.files = []
					for i in range(len(self.entradasLista)):
						self.files.append(self.entradasLista[i][1])
						
					self.screens(4)
					
			else:
				self.avisoA["text"] = self.errosLeituraDados
			
		else:
		
			self.avisoA["text"] = ""
		
			for i in range(0, len(mainData[1][0])):
		
				if(i > 0):
				
					self.avisoA["text"] = self.avisoA["text"]+"\n"
		
				self.avisoA["text"] = self.avisoA["text"]+mainData[1][0][i]
			
	def valide3Here_MainSettings(self):
		
		segue = 1
		
		mensagensErro = []
		dados = [[],[]]
		
		caminhoConfPrincipal = self.entrada1.get()
		pastaDados = self.entrada2.get()
		pastaSaida = self.entrada3.get()
		arquivoDados = self.entrada4.get()
		
		if(caminhoConfPrincipal == ""):
		
			mensagensErro.append("ERRO: Não foi indicado nenhum nome para o arquivo de configurações principal")
			segue = 0
		
		if(pastaDados == ""):
		
			mensagensErro.append("ERRO: Não foi indicada nenhuma pasta para 'pasta com os dados'")
			segue = 0
		
		elif(not os.path.isdir(self.pastaProjeto+"/"+pastaDados)):
					
			mensagensErro.append("ERRO: Uma pasta que não existe ("+pastaDados+") é listada para 'pasta com os dados'")
			segue = 0
		
		if(pastaSaida == ""):
		
			mensagensErro.append("ERRO: Não foi indicada nenhuma pasta para 'pasta destino da resolução'")
			segue = 0
		
		elif(not os.path.isdir(self.pastaProjeto+"/"+pastaSaida)):
					
			mensagensErro.append("ERRO: Uma pasta que não existe ("+pastaSaida+") é listada para 'pasta destino da resolução'")
			segue = 0
		
		if(arquivoDados == ""):
					
			mensagensErro.append("ERRO: Não foi indicada nenhuma pasta para 'arquivo com a lista de dados'")
			segue = 0
		
		elif(not os.path.exists(self.pastaProjeto+"/"+arquivoDados)):
					
			mensagensErro.append("ERRO: Um arquivo que não existe ("+arquivoDados+") é listado para 'arquivo com a lista de dados'")
			segue = 0
			
		else:
		
			self.mainData = [[pastaDados, pastaSaida],[arquivoDados]]
			
			nomes_arquivosDados = ["HorariosId","GradeHoraria","SalasCapacidades","DisciplinasTamanhos","SalasRecursos","DisciplinasRecursos","SalasPref","CurriculosDisciplinas","CurriculosSalas","Distancias"]
			(c, g, g, self.entradasLista, g) = self.trate(self.pastaProjeto+"/"+self.mainData[1][0], 
				[0, 3,
					":",
					"texto",
					[1, nomes_arquivosDados, 1],
					[0, "arquivo", self.pastaProjeto+"/"+self.mainData[0][0]],
					[1, nomes_arquivosDados, "", 0]
				],
				[0, 3,
					";",
					"texto",
					[1, nomes_arquivosDados, 1],
					[0, "arquivo", self.pastaProjeto+"/"+self.mainData[0][0]],
					[1, nomes_arquivosDados, "", 0]
				],
				0,
				0
			)
			
			if(c):
			
				if(self.getValue(self.entradasLista, "HorariosId") == ""):
					c = 0
					self.avisoB["text"] = self.avisoB["text"]+"Aviso: Não foi indicado um arquivo com os IDs dos horários\n"
				if(self.getValue(self.entradasLista, "GradeHoraria") == ""):
					c = 0
					self.avisoB["text"] = "Aviso: Não foi indicado um arquivo com a grade horária das turmas\n"
				
				if(c):
				
					self.files = []
					for i in range(len(self.entradasLista)):
						self.files.append(self.entradasLista[i][1])
						
					self.screens(4)
					
			else:
				self.avisoB["text"] = "Verificar o arquivo ["+self.pastaProjeto+"/"+self.mainData[1][0]+"]\nOs padrões estabelecidos não foram seguidos\nou os arquivos indicados não existem\no painel de controle (prompt de comando) pode ser útil"
			
		if(segue):
		
			dados[0].append(pastaDados)
			dados[0].append(pastaSaida)
			dados[1].append(self.pastaProjeto+"/"+arquivoDados)
			
			try:
		
				with open(self.pastaProjeto+"/"+caminhoConfPrincipal, "w+", encoding = "utf8") as arquivo:
				
					arquivo.write(dados[0][0])
					arquivo.write(";")
					arquivo.write(dados[0][1])
					arquivo.write("\n")
					arquivo.write(arquivoDados)
					
					self.mainData = dados
					
					self.screens(4)
					
			except:
			
				self.avisoB["text"] = "Não foi possível criar o arquivo de configurações principal com o nome ("+caminhoConfPrincipal+")"
			
		else:
		
			self.avisoB["text"] = ""
		
			for i in range(0, len(mensagensErro)):
		
				if(i > 0):
				
					self.avisoB["text"] = self.avisoB["text"]+"\n"
		
				self.avisoB["text"] = self.avisoB["text"]+mensagensErro[i]
	
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	I_Salas = 0
	I_Horarios = 0
	I_HorariosN = 0
	I_HorariosM = 0
	I_Disciplinas = 0
	I_Aulas = 0
	I_Recursos = 0
	I_Curriculos = 0
	
	R_SalasRecursos = 0
	R_DisciplinasRecursos = 0
	R_CurriculosDisciplinas = 0
	R_Distancias = 0
	
	Rd_CurriculosSalas = 0
	
	C_SalasPref = 0
	C_SalasCapacidades = 0
	C_DisciplinasTamanhos = 0
	
	def extensaoGet(self, nome):
	
		extensao = nome.split(".")
		extensao = extensao[len(extensao) - 1].strip()
							
		if(extensao == "txt"):
							
			extensao = 0
								
		else:
							
			extensao = 1
			
		return extensao
	
	def valideFiles0(self):
	
		fileName = self.getValue(self.entradasLista, "HorariosId")
		
		if(fileName != ""):
			(c, self.I_HorariosN, g, self.I_HorariosM, g) = self.trate(fileName,
				[0, 3,
					":",
					"texto",
					[
						0
					],
					[0,  "intervalod", ""],
					[0],
					[0]
				],
				[0, 3,
					";",
					"texto",
					[
						0
					],
					[0,  "intervalod", ""],
					[0],
					[0]
				],
				0,
				0
			)
			if(c):
				self.I_Horarios = self.colide(self.I_HorariosN, self.I_HorariosM)
		
		self.help_file0["text"] = self.errosLeituraDados
		return c
	
	def valideFiles1(self):
		
		fileName = self.getValue(self.entradasLista, "GradeHoraria")
		if(fileName != "" and self.I_Horarios):
		
			(c, horariosLinha, self.I_Disciplinas, gradeHoraria, g) = self.trate(fileName,
				[1, 1,
					[":", ";"],
					"texto",
					[
						[
							0
						],
						[
							1,
							self.I_HorariosN
						],
					],
					"texto",
					[0, 1, 0],
					[0, self.I_HorariosN, 0, 0]
				],
				[1, 1,
					[";", ";"],
					"texto",
					[
						[
							0
						],
						[
							1,
							self.I_HorariosN
						],
					],
					"texto",
					[0, 1, 0],
					[0, self.I_HorariosN, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							1,
							self.I_HorariosN,
							0,
							1
						],
						[
							0
						]
					],
					"BIN",
					["DISCIPLINAS", 0, 0],
					[self.I_HorariosN, 0, 0, 0]
				],
				0
			)
			if(c):
				horarios = []
				for j in range(len(self.I_Horarios)):
					horarios.append(self.getValue(self.I_Horarios, horariosLinha[j]))
				
				self.I_Aulas = []
				disciplinasDeletar = []
				for i in range(len(self.I_Disciplinas)):
					existe = 0
					for j in range(len(horarios)):
						if(gradeHoraria[i][j]):
							existe = 1
							self.I_Aulas.append([self.I_Disciplinas[i], horarios[j]])
					if(not existe):
						disciplinasDeletar.append(i)
				i = len(disciplinasDeletar) - 1
				while(i >= 0):
					self.errosLeituraDados = self.errosLeituraDados+"A disciplina ["+self.I_Disciplinas[disciplinasDeletar[i]]+"] será deletada pois não foi associada a nenhum horário\n"
					del self.I_Disciplinas[disciplinasDeletar[i]]
					i -= 1
					
		self.help_file1["text"] = self.errosLeituraDados
		return c
	
	def valideFiles2(self):
		
		fileName = self.getValue(self.entradasLista, "SalasCapacidades")
		if(fileName != ""):
			(c, self.I_Salas, g, self.C_SalasCapacidades, g) = self.trate(fileName, 
				[0, 3,
					":",
					"texto",
					[0, 0, 0],
					[0, "Numerico", 0],
					[0, 0, 0, 0]
				],
				[0, 3,
					";",
					"texto",
					[0, 0, 0],
					[0, "Numerico", ""],
					[0, 0, 0, 0]
				],
				0,
				0
			)
			if(not c):
				self.I_Salas = 0
				self.C_SalasCapacidades = 0
			else:
				self.C_SalasCapacidades = self.colide(self.I_Salas, self.C_SalasCapacidades) #É necessário pois não foi indicado nada em fill // Não era possível o fazer
	
		self.help_file2["text"] = self.errosLeituraDados
		return c
	
	def valideFiles3(self):
		
		fileName = self.getValue(self.entradasLista, "DisciplinasTamanhos")
		if(fileName != "" and self.I_Disciplinas):
			(c, g, g, self.C_DisciplinasTamanhos, g) = self.trate(fileName, 
				[0, 3,
					":",
					"texto",
					[
						1,
						self.I_Disciplinas,
						1
					],
					[0, "Numerico", 0],
					[1, self.I_Disciplinas, 0, 0]
				],
				[0, 3,
					";",
					"texto",
					[
						1,
						self.I_Disciplinas,
						1
					],
					[0, "Numerico", 0],
					[1, self.I_Disciplinas, 0, 0]
				],
				0,
				0
			)
			if(not c):
				self.C_DisciplinasTamanhos = 0
	
		self.help_file3["text"] = self.errosLeituraDados
		return c
	
	def valideFiles4(self):
		
		fileName = self.getValue(self.entradasLista, "SalasRecursos")
		if(fileName != "" and self.I_Salas):
			(c, self.I_Recursos, g, self.R_SalasRecursos, g) = self.trate(fileName,
				[1, 2,
					[":", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Salas,
							1
						],
						[
							0
						],
					],
					["texto","numerico"],
					[[0], [0], [1], [0]],
					[self.I_Salas, 0, 0, 0]
				],
				[1, 2,
					[";", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Salas,
							1
						],
						[
							0
						],
					],
					["texto","numerico"],
					[[0], [0], [1], [0]],
					[self.I_Salas, 0, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							0
						],
						[
							1,
							self.I_Salas,
							0,
							1
						]
					],
					"NUMERICO",
					["SALAS", 0, 0],
					[0, self.I_Salas, 0, 0]
				],
				0
			)
			if(not c):
				self.I_Recursos = 0
				self.R_SalasRecursos = 0
		
		self.help_file4["text"] = self.errosLeituraDados
		return c
	
	def valideFiles5(self):
	
		fileName = self.getValue(self.entradasLista, "DisciplinasRecursos")
		if(fileName != "" and self.I_Disciplinas and self.I_Recursos):
			(c, g, g, self.R_DisciplinasRecursos, g) = self.trate(fileName,
				[1, 2,
					[":", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Disciplinas,
							1
						],
						[
							1,
							self.I_Recursos,
							1
						],
					],
					["texto","numerico"],
					[[0], [0], [1], [0]],
					[self.I_Disciplinas, self.I_Recursos, 0, 0]
				],
				[1, 2,
					[";", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Disciplinas,
							1
						],
						[
							1,
							self.I_Recursos,
							1
						],
					],
					["texto","numerico"],
					[[0], [0], [1], [0]],
					[self.I_Disciplinas, self.I_Recursos, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							1,
							self.I_Recursos,
							0,
							1
						],
						[
							1,
							self.I_Disciplinas,
							0,
							1
						]
					],
					"NUMERICO",
					["DISCIPLINAS", 0, 0],
					[self.I_Recursos, self.I_Disciplinas, 0, 0]
				],
				0
			)
			if(not c):
				self.R_DisciplinasRecursos = 0
		
		self.help_file5["text"] = self.errosLeituraDados
		return c
		
	def valideFiles6(self):
		
		fileName = self.getValue(self.entradasLista, "SalasPref")
		if(fileName != "" and self.I_Salas):
			(c, g, g, self.C_SalasPref, g) = self.trate(fileName, 
				[0, 3,
					":",
					"texto",
					[
						1,
						self.I_Salas,
						1
					],
					[0, "BIN", 0],
					[1, self.I_Salas, 0, 0]
				],
				[0, 3,
					";",
					"texto",
					[
						1,
						self.I_Salas,
						1
					],
					[0, "BIN", 0],
					[1, self.I_Salas, 0, 0]
				],
				0,
				0
			)
			if(not c):
				self.C_SalasPref = []
				for i in range(len(self.I_Salas)):
					self.C_SalasPref.append([self.I_Salas[i],0])
			else:
				for i in range(len(self.I_Salas)):
					self.C_SalasPref[i][1] = - self.C_SalasPref[i][1]
		else:
			if(self.I_Salas):
				self.C_SalasPref = []
				for i in range(len(self.I_Salas)):
					self.C_SalasPref.append([self.I_Salas[i],0])
		
		self.help_file6["text"] = self.errosLeituraDados
		return c
	
	def valideFiles7(self):
	
		fileName = self.getValue(self.entradasLista, "CurriculosDisciplinas")
		if(fileName != "" and self.I_Disciplinas):
			(c, self.I_Curriculos, g, self.R_CurriculosDisciplinas, g) = self.trate(fileName,
				[0, 1,
					[":", ";"],
					"texto",
					[
						[
							0
						],
						[
							1,
							self.I_Disciplinas
						],
					],
					"texto",
					[0, 1, 0],
					[0, self.I_Disciplinas, 0, 0]
				],
				[0, 1,
					[";", ";"],
					"texto",
					[
						[
							0
						],
						[
							1,
							self.I_Disciplinas
						],
					],
					"texto",
					[0, 1, 0],
					[0, self.I_Disciplinas, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							0
						],
						[
							1,
							self.I_Disciplinas,
							0,
							1
						]
					],
					"BIN",
					["DISCIPLINAS", 0, 0],
					[0, self.I_Disciplinas, 0, 0],
					1
				],
				0
			)
			if(not c):
				self.I_Curriculos = 0
				self.R_CurriculosDisciplinas = 0
		
		self.help_file7["text"] = self.errosLeituraDados
		return c
		
	def valideFiles8(self):
	
		fileName = self.getValue(self.entradasLista, "CurriculosSalas")
		if(fileName != "" and self.I_Salas and self.I_Curriculos):
			(c, g, g, g, valor) = self.trate(fileName,
				[0, 2,
					[":", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Curriculos,
							1
						],
						[
							1,
							self.I_Salas,
							1
						],
					],
					["texto","texto"],
					[[0], [0], [0], [2]],
					[self.I_Curriculos, self.I_Salas, 0, 0]
				],
				[0, 2,
					[":", ";", ":"],
					2,
					"texto",
					[
						[
							1,
							self.I_Curriculos,
							1
						],
						[
							1,
							self.I_Salas,
							1
						],
					],
					["texto","texto"],
					[[0], [0], [0], [2]],
					[self.I_Curriculos, self.I_Salas, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							1,
							self.I_Salas,
							0,
							1
						],
						[
							1,
							self.I_Curriculos,
							0,
							1
						]
					],
					"texto",
					["CURRICULOS", 0, 0],
					[self.I_Salas, self.I_Curriculos, 0, 0]
				],
				0
			)
			if(c):
				self.Rd_CurriculosSalas = []
				for i in range(len(self.I_Curriculos)):
					self.Rd_CurriculosSalas.append([])
					for j in range(len(self.I_Salas)):
						self.Rd_CurriculosSalas[-1].append(-valor[i][j])
		
		self.help_file8["text"] = self.errosLeituraDados
		return c
		
	def valideFiles9(self):
	
		fileName = self.getValue(self.entradasLista, "Distancias")
		if(fileName != "" and self.I_Salas):
			(c, g, g, self.R_Distancias, g) = self.trate(fileName,
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							1,
							self.I_Salas,
							0,
							1
						],
						[
							1,
							self.I_Salas,
							0,
							1
						]
					],
					"NUMERICO",
					["ORIGENS", 0, 0],
					[self.I_Salas, self.I_Salas, 0, 0]
				],
				[0, 0,
					";",
					["texto", "texto"],
					[
						[
							1,
							self.I_Salas,
							0,
							1
						],
						[
							1,
							self.I_Salas,
							0,
							1
						]
					],
					"NUMERICO",
					["ORIGENS", 0, 0],
					[self.I_Salas, self.I_Salas, 0, 0]
				],
				0,
				0
			)
			if(not c):
				self.R_Distancias = 0
		
		self.help_file9["text"] = self.errosLeituraDados
		return c
		
	'''--------------------------------------------------------------------------------------------------------------------------------'''
		
	def readArquivoInicial(self, caminho):
	
		segue = 1
		retorno = [0,[[],["",""]]]

		dados = [[],[]]

		if(caminho.strip() != ""):

			try:
			
				with open(self.pastaProjeto+"/"+caminho, "r", encoding = "utf8") as arquivo:
					
					nLinha = 1
					for linha in arquivo:
						if(nLinha == 1):
						
							linha = linha.split(";")
							
							if(len(linha) == 2):
							
								pastaDados = linha[0].strip()
								pastaSaida = linha[1].strip()
								
								if(pastaDados == ""):
								
									retorno[1][0].append("ERRO: Na linha "+str(nLinha)+", não foi indicada nenhuma pasta para 'pasta com os dados'")
									segue = 0
								
								elif(not os.path.isdir(self.pastaProjeto+"/"+pastaDados)):
											
									retorno[1][0].append("ERRO: Na linha "+str(nLinha)+", uma pasta que não existe ("+pastaDados+") é listada para 'pasta com os dados'")
									segue = 0
								
								if(pastaSaida == ""):
								
									retorno[1][0].append("ERRO: Na linha "+str(nLinha)+", não foi indicada nenhuma pasta para 'pasta destino da resolução'")
									segue = 0
								
								elif(not os.path.isdir(self.pastaProjeto+"/"+pastaSaida)):
											
									retorno[1][0].append("ERRO: Na linha "+str(nLinha)+", uma pasta que não existe ("+pastaSaida+") é listada para 'pasta destino da resolução'")
									segue = 0
									
								if(segue):
								
									dados[0].append(pastaDados)
									dados[0].append(pastaSaida)
							
							else:
							
								retorno[1][0].append("ERRO: Na linha um deveria haver um ';' para que fossem separadas as pasta com os dados e a pasta onde será armazenada a resolução")
								segue = 0
					
						elif(nLinha == 2):
						
							arquivoDados = linha.strip()
							
							if(arquivoDados == ""):
							
								retorno[1][0].append("ERRO: Na linha "+str(nLinha)+", não foi indicada nenhum arquivo para 'arquivo com a lista de dados'")
								segue = 0
								
							elif(not os.path.exists(self.pastaProjeto+"/"+arquivoDados)):
								
								retorno[1][0].append("ERRO!!: Na linha "+str(nLinha)+", um arquivo que não existe ("+arquivoDados+") é listado para 'arquivo com a lista de dados'")
								segue = 0
								
							if(segue):
								
								dados[1].append(arquivoDados)
								
						elif(segue and nLinha > 2):
						
							retorno[1][0].append("ERRO: Não lemos a linha "+str(nLinha)+" e nem a partir dela, pois o padrão do documento só possui duas linhas")
							segue = 0
							
						nLinha += 1
						
					if(nLinha == 1):
					
						retorno[1][0].append("ERRO: Arquivo vazio")
						segue = 0
						
					elif(nLinha == 2):
					
						retorno[1][0].append("ERRO: O arquivo deveria possuir duas linhas, mas só há uma")
						segue = 0
			
			except:
			
				retorno[1][0].append("ERRO: Não foi possível abrir o arquivo "+caminho)
				retorno[1][1][0] = self.corErro2
				retorno[1][1][1] = self.FcorErro2
				segue = 0
			
		else:

			retorno[1][0].append("Não foi indicada nenhum arquivo")
			retorno[1][1][0] = self.corErro1
			retorno[1][1][1] = self.FcorErro1
			segue = 0
		
		if(retorno[1][1][0] == ""):
		
			retorno[1][1][0] = self.corErro1
			retorno[1][1][1] = self.FcorErro1
			
		if(segue):
		
			retorno[1] = dados
			
		retorno[0] = segue
			
		return retorno
	
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
	Matriz_o = []
	Matriz_n = []
	Matriz_aulasDisciplinas = []
	Matriz_aulasCurriculos = 0
	Matriz_uso = []
	
	x = 0
		
	def resolverModelo(self):
	
		self.Matriz_o = []
		self.Matriz_n = []
		self.Matriz_aulasDisciplinas = []
		self.Matriz_aulasCurriculos = 0
		self.Matriz_uso = []
	
		grandeErro = []
		c = 1
	
		self.solucao["text"] = "Resolvendo o modelo"
		self.analise["text"] = "Resolvendo o modelo"
		self.solucao["bg"] = "#ff8533"
		self.analise["bg"] = "#ff8533"
	
		self.analise["text"] = "Agora estamos realizando o pré-processamento - isso pode demorar um pouco"
	
		for i in range(len(self.I_Aulas)):
			self.Matriz_o.append([])
			for j in range(len(self.I_Aulas)):
				self.Matriz_o[-1].append(0)
		for i in range(len(self.I_Aulas)):
			for j in range(len(self.I_Aulas)):
				if(i != j and self.I_Aulas[i][0] != self.I_Aulas[j][0]):
					if((self.I_Aulas[i][1][0] <= self.I_Aulas[j][1][0] and self.I_Aulas[i][1][1] > self.I_Aulas[j][1][0]) or (self.I_Aulas[i][1][0] < self.I_Aulas[j][1][1] and self.I_Aulas[i][1][1] >= self.I_Aulas[j][1][1]) or (self.I_Aulas[i][1][0] == self.I_Aulas[j][1][0] and self.I_Aulas[i][1][1] == self.I_Aulas[j][1][1])):
						self.Matriz_o[i][j] = 1
		
		for i in range(len(self.I_Disciplinas)):
			self.Matriz_aulasDisciplinas.append([])
			for j in range(len(self.I_Aulas)):
				self.Matriz_aulasDisciplinas[i].append(0)
		
		if(self.entradasLista[7][1] != "" and self.entradasLista[8][1] != ""):
			self.Matriz_aulasCurriculos = []
			for i in range(len(self.I_Curriculos)):
				self.Matriz_aulasCurriculos.append([])
				for j in range(len(self.I_Aulas)):
					self.Matriz_aulasCurriculos[i].append(0)

		for i in range(len(self.I_Aulas)):
			self.Matriz_n.append([])
			self.Matriz_uso.append([])
		
		for i in range(len(self.I_Aulas)):
		
			posDis = self.I_Disciplinas.index(self.I_Aulas[i][0])
			self.Matriz_aulasDisciplinas[posDis][i] = 1
			
			if(self.entradasLista[7][1] != "" and self.entradasLista[8][1] != ""):
				for j in range(len(self.I_Curriculos)):
					if(self.R_CurriculosDisciplinas[j][posDis]):
						self.Matriz_aulasCurriculos[j][i] = 1
			
			alocavel = 0
			for j in range(len(self.I_Salas)):
			
				self.Matriz_n[i].append(0)
				self.Matriz_uso[i].append(0)
				
				if(self.C_DisciplinasTamanhos[posDis][1] > self.C_SalasCapacidades[j][1]):
					self.Matriz_n[i][j] = 1
				else:
					self.Matriz_uso[i][j] = self.C_SalasCapacidades[j][1] - self.C_DisciplinasTamanhos[posDis][1]
				
				if(self.entradasLista[4][1] != "" and self.entradasLista[5][1] != ""):
					for k in range(len(self.I_Recursos)):
						if(self.R_DisciplinasRecursos[posDis][k] > self.R_SalasRecursos[j][k]):
							self.Matriz_n[i][j] = 1
				
				if(not self.Matriz_n[i][j]):
					alocavel += 1
					
			if(not alocavel):
				c = 0
				grandeErro.append("Erro gravíssimo: A aula de ["+self.I_Disciplinas[posDis]+"] das ["+self.minuto_paraHorario(self.I_Aulas[i][1], 1)+"] não pode ser ministrada em nenhuma das salas")
	
		if(c):
	
			preechido = 0
		
			constante0 = self.constante0.get()
			if(constante0):
			
				preechido = 1
				
			constante1 = self.constante1.get()
			if(constante1):
			
				preechido = 1
				
			constante2 = self.constante2.get()
			if(constante2):
			
				preechido = 1
				
			constante3 = self.constante3.get()
			if(constante3):
			
				preechido = 1
				
			constante4 = self.constante4.get()
			if(constante4):
			
				preechido = 1
		
			if(not preechido):
			
				self.solucao["text"] = "Todas as constantes zeradas"
				self.analise["text"] = "É necessário que pelo menos uma constante seja maior que zero"
				situacao = 0
			
			else:

				self.analise["text"] = "Agora estamos montando o modelo"
				modelo = Model()
				
				self.analise["text"] = "Prepararando as variáveis de decisão"
				
				x = [[modelo.add_var(var_type=BINARY) for j in range(len(self.I_Salas))] for i in range(len(self.I_Aulas))]
				x_in_dis = [[modelo.add_var(var_type=BINARY) for j in range(len(self.I_Salas))] for i in range(len(self.I_Disciplinas))]
				
				y = [modelo.add_var(var_type=INTEGER) for i in range(len(self.I_Disciplinas))]
				
				if(self.I_Curriculos):
				
					w = [[modelo.add_var(var_type=BINARY) for j in range(len(self.I_Salas))] for i in range(len(self.I_Curriculos))]
					v = [[[modelo.add_var(var_type=BINARY) for k in range(len(self.I_Salas))] for j in range(len(self.I_Salas))] for i in range(len(self.I_Curriculos))]
				
				self.analise["text"] = "Preparando restrições"
				
				for i in range(len(self.I_Aulas)):
					
					for j in range(len(self.I_Salas)):
						if(self.Matriz_n[i][j]):
							modelo.add_constr(x[i][j] <= 0)	#3.10
					
					modelo.add_constr(xsum(x[i][j] for j in range(len(self.I_Salas))) == 1)	#3.9
				
				self.analise["text"] = "Duas restrições de sete prontas"
				
				for i in range(len(self.I_Disciplinas)):
					
					for j in range(len(self.I_Aulas)):
						
						if(self.Matriz_aulasDisciplinas[i][j]):
						
							for k in range(len(self.I_Salas)):
							
								modelo.add_constr(x[j][k] <= x_in_dis[i][k])	#3.12 AUX
								
					modelo.add_constr(xsum(x_in_dis[i][j] for j in range(len(self.I_Salas))) <= 1 + y[i])	#3.12
				
				self.analise["text"] = "Três restrições de sete prontas"
				
				for i in range(len(self.I_Aulas)):
					
					for j in range(len(self.I_Aulas)):
						if(self.Matriz_o[i][j]):
							for k in range(len(self.I_Salas)):
								modelo.add_constr(x[i][k] + x[j][k] <= 1)	#3.11
					
					if(self.I_Curriculos):
					
						for j in range(len(self.I_Curriculos)):
							for k in range(len(self.I_Salas)):
								if(self.Matriz_aulasCurriculos[j][i]):
									modelo.add_constr(x[i][k] <= w[j][k])	#3.13
				
				self.analise["text"] = "Cinco restrições de sete prontas"
				
				if(self.I_Curriculos):
				
					for i in range(len(self.I_Curriculos)):
						for j in range(len(self.I_Salas)):
							for k in range(len(self.I_Salas)):
								modelo.add_constr(2*v[i][j][k] <= w[i][j] + w[i][k])	#3.14
								modelo.add_constr(v[i][j][k] >= w[i][j] + w[i][k] - 1)	#3.15
				
				self.analise["text"] = "Preparando a função objetiva"
				
				alpha = (xsum(self.Matriz_uso[i][j]*x[i][j] for j in range(len(self.I_Salas)) for i in range(len(self.I_Aulas))))
				beta = (xsum(y[i] for i in range(len(self.I_Disciplinas))))
				if(self.R_Distancias):
					gama = (xsum(self.R_Distancias[j][k]*v[i][j][k] for i in range(len(self.I_Curriculos)) for j in range(len(self.I_Salas)) for k in range(len(self.I_Salas))))
				else:
					gama = 0
				if(self.C_SalasPref):
					delta = (xsum(self.C_SalasPref[j][1]*x[i][j] for i in range(len(self.I_Aulas)) for j in range(len(self.I_Salas))))
				else:
					delta = 0
				if(self.Rd_CurriculosSalas):
					episolon = (xsum(self.Rd_CurriculosSalas[i][j]*w[i][j] for i in range(len(self.I_Curriculos)) for j in range(len(self.I_Salas))))
				else:
					episolon = 0

				modelo.objective = minimize(constante0*alpha + constante1*beta + constante2*gama + constante3*delta + constante4*episolon)
				
				if(self.tempo.get() != 0):
				
					situacao = modelo.optimize(max_seconds = self.tempo.get()*60)
				
				else:
				
					self.tempo.set(60)
					situacao = modelo.optimize(max_seconds = 60*60)
				
				if(not (situacao == OptimizationStatus.OPTIMAL or situacao == OptimizationStatus.FEASIBLE) and preechido):
					self.solucao["bg"] = self.corPadrao
					self.analise["bg"] = self.corPadrao
			
					self.solucao["text"] = "Não foi encontrada uma solução! tente aliviar as restrições e expandir as possibilidades"
					self.analise["text"] = "Solução não encontrada"
					
				else:
					
					self.x = x
					
					self.solucao["bg"] = self.corPadrao
					self.analise["bg"] = self.corPadrao
				
					self.impressora1["state"] = "normal"
					self.impressao1["text"] = ""
					self.impressao1["bg"] = self.corPadrao
				
					if(situacao == OptimizationStatus.OPTIMAL):
					
						self.solucao["text"] = "Solução ótima encontrada\n"
					
					else:
					
						self.solucao["text"] = "Solução sub ótima encontrada\n"
						
					alpha = 0
					if(self.entradasLista[2][1] != "" and self.entradasLista[3][1] != ""):
					
						for i in range(len(self.I_Aulas)):
					
							for j in range(len(self.I_Salas)):
							
								alpha += self.Matriz_uso[i][j]*x[i][j].x
								
					beta = 0
					for i in range(len(self.I_Disciplinas)):
					
						beta += y[i].x
						
					gama = 0
					if(self.entradasLista[7][1] != "" and self.entradasLista[9][1] != ""):
					
						for i in range(len(self.I_Curriculos)):
							
							for j in range(len(self.I_Salas)):
							
								for k in range(len(self.I_Salas)):
									
									gama += self.R_Distancias[j][k]*v[i][j][k].x
									
					delta = 0
					if(self.entradasLista[6][1] != ""):
					
						for i in range(len(self.I_Aulas)):
						
							for j in range(len(self.I_Salas)):
								
								delta += self.C_SalasPref[j][1]*x[i][j].x
					
					epsilon = 0
					if(self.entradasLista[7][1] != "" and self.entradasLista[8][1] != ""):
					
						for i in range(len(self.I_Curriculos)):
						
							for j in range(len(self.I_Salas)):
								
								epsilon += self.Rd_CurriculosSalas[i][j]*w[i][j].x
					
					self.analise["text"] = ""
					if(self.entradasLista[2][1] != "" and self.entradasLista[3][1] != ""):
						self.analise["text"] = self.analise["text"]+"USO :"+str(constante0*alpha)+"\n"
					self.analise["text"] = self.analise["text"]+"TROCAS :"+str(constante1*beta)+"\n"
					if(self.entradasLista[7][1] != "" and self.entradasLista[9][1] != ""):
						self.analise["text"] = self.analise["text"]+"DISTÂNCIAS :"+str(constante2*gama)+"\n"
					if(self.entradasLista[6][1] != ""):
						self.analise["text"] = self.analise["text"]+"OCUPAÇÃO :"+str(constante3*delta)+"\n"
					if(self.entradasLista[8][1] != ""):
						self.analise["text"] = self.analise["text"]+"TURMAS :"+str(constante4*epsilon)+"\n"
		
		else:
			
			self.solucao["text"] = "Ocorreu um erro gravíssimo durante o pré-processamento!"
			mensagemGrandeErro = ""
			for i in range(len(grandeErro)):
				mensagemGrandeErro = mensagemGrandeErro+"\n"+grandeErro[i]
			self.analise["text"] = mensagemGrandeErro
		
	def imprimir(self):
	
		self.impressao1["text"] = ""
					
		self.impressao1["text"] = "Agora vamos salvar isso no arquivo solucao.txt e solucao.csv\n"
	
		try:
			with open(self.pastaProjeto+"/"+self.mainData[0][1]+"/solucao.txt", "w+") as arquivo:
				arquivo.write("Aulas e suas salas:\n\n")
				for i in range(len(I_Aulas)):
					linha = ""
					for j in range(len(I_Salas)):
						if(self.x[i][j].x):
							arquivo.write("A aula de ["+self.I_Aulas[i][0]+"] das ["+self.minuto_paraHorario(self.I_Aulas[i][1], 1)+"] ocupará a sala ["+self.I_Salas[j]+"]\n")
				self.impressao1["text"] = self.impressao1["text"]+"Acabamos de criar o arquivo solucao.txt\n"
		except:
			self.impressao1["text"] = self.impressao1["text"]+"Não foi possível criar o arquivo solucao.txt\n"
			
		try:
			with open(self.pastaProjeto+"/"+self.mainData[0][1]+"/solucao.csv", "w+") as arquivo:
				arquivo.write("Disciplina;;Horário da aula;;Sala:\n\n")
				for i in range(len(self.I_Aulas)):
					for j in range(len(self.I_Salas)):
						if(self.x[i][j].x):
							arquivo.write(self.I_Aulas[i][0]+";;"+self.minuto_paraHorario(self.I_Aulas[i][1], 1)+";;"+self.I_Salas[j]+"\n")
				self.impressao1["text"] = self.impressao1["text"]+"Acabamos de criar o arquivo solucao.csv\n"
		except:
			self.impressao1["text"] = self.impressao1["text"]+"Não foi possível criar o arquivo solucao.csv\n"
		
		self.impressao1["text"] = self.impressao1["text"]+"Estamos nos preparando para salvar as soluções expandidas por dia\n"
			
		mensagens = ["","","","","","",""]
		I_AulasDia = [[],[],[],[],[],[],[]]
		I_HorariosDia = [[],[],[],[],[],[],[]]
			
		for i in range(len(self.I_Aulas)):
			if(self.I_Aulas[i][1][0] < 60*24*1):
				I_AulasDia[0].append(i)
			elif(self.I_Aulas[i][1][0] < 60*24*2):
				I_AulasDia[1].append(i)
			elif(self.I_Aulas[i][1][0] < 60*24*3):
				I_AulasDia[2].append(i)
			elif(self.I_Aulas[i][1][0] < 60*24*4):
				I_AulasDia[3].append(i)
			elif(self.I_Aulas[i][1][0] < 60*24*5):
				I_AulasDia[4].append(i)
			elif(self.I_Aulas[i][1][0] < 60*24*6):
				I_AulasDia[5].append(i)
			else:
				I_AulasDia[6].append(i)
					
		for i in range(len(self.I_Horarios)):
			if(self.I_Horarios[i][1][0] < 60*24*1):
				I_HorariosDia[0].append(self.I_Horarios[i][1])
			elif(self.I_Horarios[i][1][0] < 60*24*2):
				I_HorariosDia[1].append(self.I_Horarios[i][1])
			elif(self.I_Horarios[i][1][0] < 60*24*3):
				I_HorariosDia[2].append(self.I_Horarios[i][1])
			elif(self.I_Horarios[i][1][0] < 60*24*4):
				I_HorariosDia[3].append(self.I_Horarios[i][1])
			elif(self.I_Horarios[i][1][0] < 60*24*5):
				I_HorariosDia[4].append(self.I_Horarios[i][1])
			elif(self.I_Horarios[i][1][0] < 60*24*6):
				I_HorariosDia[5].append(self.I_Horarios[i][1])
			else:
				I_HorariosDia[6].append(self.I_Horarios[i][1])
			
		for dia in range(0, 7):
			if(len(I_HorariosDia[dia]) > 0 and len(I_AulasDia[dia]) > 0):
					
				for i in range(len(I_HorariosDia[dia])):
					mensagens[dia] = mensagens[dia]+";"+self.minuto_paraHorario(I_HorariosDia[dia][i], 1)
					
				gradeSalas = []
				for i in range(len(self.I_Salas)):
					gradeSalas.append([])
					for j in range(len(I_HorariosDia[dia])):
						gradeSalas[-1].append("")	
					
				for i in range(len(I_AulasDia[dia])):
					for j in range(len(self.I_Salas)):
						if(self.x[I_AulasDia[dia][i]][j].x):
							gradeSalas[j][I_HorariosDia[dia].index(self.I_Aulas[I_AulasDia[dia][i]][1])] = self.I_Aulas[I_AulasDia[dia][i]][0]
					
				for i in range(len(self.I_Salas)):
					mensagens[dia] = mensagens[dia]+"\n"+self.I_Salas[i]
					for j in range(len(I_HorariosDia[dia])):
						mensagens[dia] = mensagens[dia]+";"+gradeSalas[i][j]
					
		self.impressao1["text"] = self.impressao1["text"]+"Agora vamos começar a salvar as soluções expandidas por dia\n"
		diasExtenso = ["a segunda","a terça","a quarta","a quinta","a sexta","o sábado","o domingo"]
		for dia in range(0, 7):
			if(len(I_HorariosDia[dia]) > 0 and len(I_AulasDia[dia]) > 0):
				self.impressao1["text"] = self.impressao1["text"]+"Agora vamos salvar a solução expandida d"+diasExtenso[dia]+" em solucao_expandida_"+diasExtenso[dia][2:]+".csv\n"
				try:
					with open(self.pastaProjeto+"/"+self.mainData[0][1]+"/solucao_expandida_"+diasExtenso[dia][2:]+".csv", "w+") as arquivo:
						arquivo.write(mensagens[dia])
						self.impressao1["text"] = self.impressao1["text"]+"Acabamos de criar o arquivo solucao_expandida_"+diasExtenso[dia][2:]+".csv\n"
				except:
					self.impressao1["text"] = self.impressao1["text"]+"Não foi possível criar o arquivo solucao_expandida_"+diasExtenso[dia][2:]+".csv\n"
				
			else:
				self.impressao1["text"] = self.impressao1["text"]+"Não há aulas n"+diasExtenso[dia]+", então não vamos criar um arquivo com a sulução expandida desse dia\n"
			
		self.impressao1["text"] = self.impressao1["text"]+"Estamos nos preparando para salvar as soluções expandidas por sala\n"
		mensagensSalas = []
		for j in range(len(self.I_Salas)):
			mensagensSalas.append([])
			for i in range(len(self.I_Aulas)):
				if(self.x[i][j].x):
					mensagensSalas[-1].append("["+self.I_Aulas[i][0]+"] das ["+self.minuto_paraHorario(self.I_Aulas[i][1], 1)+"]\n")
					
		self.impressao1["text"] = self.impressao1["text"]+"Agora vamos começar a salvar as soluções expandidas por dia\n"
		for i in range(len(self.I_Salas)):
			self.impressao1["text"] = self.impressao1["text"]+"Tentando criar o arquivo da sala ["+self.I_Salas[i]+"] [ocupacaoSala_"+self.I_Salas[i]+".txt]\n"
			try:
				with open(self.pastaProjeto+"/"+self.mainData[0][1]+"/ocupacaoSala_"+self.I_Salas[i]+".txt", "w+") as arquivo:
					if(len(mensagensSalas[i]) == 0):
						arquivo.write("A sala ["+self.I_Salas[i]+"] não será ocupada por nenhuma aula!")
					else:
						arquivo.write("A sala ["+self.I_Salas[i]+"] será ocupada pelas seguintes aulas:\n\n")
						for j in range(len(mensagensSalas[i])):
							arquivo.write(mensagensSalas[i][j])
				self.impressao1["text"] = self.impressao1["text"]+"Acabamos de criar o arquivo da sala ["+self.I_Salas[i]+"] ["+self.mainData[0][1]+"/ocupacaoSala_"+self.I_Salas[i]+".txt]\n"
			except:
				self.impressao1["text"] = self.impressao1["text"]+"Não foi possível criar o arquivo da sala ["+self.I_Salas[i]+"] ["+self.mainData[0][1]+"/ocupacaoSala_"+self.I_Salas[i]+".txt]\n"
	
		'''
		if(certo):
		
			self.impressao1["text"] = "Pronta"
			self.impressao1["bg"] = "#00ff00"
			self.impressora1["state"] = "disabled"
		'''
		
	'''--------------------------------------------------------------------------------------------------------------------------------'''
	
root = Tk()
interface = App(root)
root.mainloop()