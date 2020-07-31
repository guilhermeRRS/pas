##################################################################################################
'''

	Conjunto de funções responsáveis pela coleta, leitura, adaptação dos dados e, por fim, seu retorno na forma desejada

'''
##################################################################################################			Importando 'os' e 'io', necessários para a coleta de dados

import os, io

##################################################################################################			Constantes

CONSTANTE_BIMESTRE = 1000000
CONSTANTE_DOUBLE_1 = "!"
CONSTANTE_DOUBLE_2 = "@"	#essas constantes já abrangem as necessárias para os tipos especificos, sendo assim, cortamos duas condicionais de <verifiqueEspeciais>

##################################################################################################			Grupo "betters", 

							#função responável pro transformar um intevalo de minutos em um texto
def minuto_paraHorario(e_intervalo, dia = 0, bimestre = 0):
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
def minuto_irredutivel(e_intervalo):
	intervalo = e_intervalo
	for i in range(0, 2):		
		if(intervalo[i] >= CONSTANTE_BIMESTRE):
			intervalo[i] -= CONSTANTE_BIMESTRE
		while(intervalo[i] - 24*60 >= 0):
			intervalo[i] -= 24*60
	return intervalo
							#função tenta escapar caracteres especiais como acentos, espaço e tab
def better_string(e_texto):
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
def verifiqueEspeciais(e_texto, erro):
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
def better_valor(e_valor, e_tipo, separadorTempo = "-"):
	certo = 1
	erro = []
	aviso = []
	out1 = out2 = 0
	tipo = better_string(e_tipo)
	valor = str(e_valor).strip()
	if(tipo == "TEXTO"):
		valor = better_string(valor)
		(c, erro) = verifiqueEspeciais(valor, erro)
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
		valor = better_string(valor)
		(c, erro) = verifiqueEspeciais(valor, erro)
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
						dia = better_string(dia)
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
				dia = better_valor(dia, "texto")
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
			valor = better_string(valor)
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
def func_transpor(matriz, right = 0, down = 0):
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
def makeIgualOutroList(lista):
	listaLinha = []
	for i in range(0, len(lista)):
		listaLinha.append(lista[i])
	return listaLinha
							#função que adiciona mais elementos a lista
def addToList(e_lista, add):
	lista = makeIgualOutroList(e_lista)
	for i in range(0, len(add)):
		lista.append(add[i])
	return lista
							#função que adiciona "descrição" a cada elemento de uma lista
def addToWarning(e_warning, tipo, local):
	warning = makeIgualOutroList(e_warning)
	if(tipo != ""):
		tipo = tipo+": "
	for i in range(0, len(warning)):
		warning[i] = "[Na "+local+"]: "+tipo+warning[i]
	return warning
							#função que emite lista
def imprimeArray(erro, imprime = 1):
	if(imprime):
		for i in range(0, len(erro)):
			print(erro[i])
							#função similar a addToWarning, porém com "descrição" diferente
def addToMessage(before, e_messages):
	messages = makeIgualOutroList(e_messages)
	for i in range(0, len(messages)):
		messages[i] = before+" "+messages[i]
	return messages
							#função une duas lista em uma outra bidimencional (dLista1+dLista2)
def colide(lista1, lista2):
	lista = []
	for i in range(0, len(lista1)):
		lista.append([lista1[i], lista2[i]])
	return lista
							#função que percorre lista procurando um valor
def getValue(lista, colisor, fill = 0, place = 1):
	colisor = better_string(colisor)
	for i in range(0, len(lista)):
		if(better_string(lista[i][0]) == colisor):
			fill = lista[i][place]
	return fill
							#função que retorna uma determinada dimensão (ou conjunto) de uma lista
def getAllValues(lista, place = 1):
	retorno = []
	for i in range(0, len(lista)):
		retorno.append(lista[i][place])
	return retorno
							#função que define valor de um dado elemento da lista e, caso não exista, o adiciona
def setValue(e_lista, colisor, valor, place = 1):
	c = 0
	lista = []
	colisor = better_string(colisor)
	for i in range(0, len(e_lista)):
		lista.append([e_lista[i][0], e_lista[i][1]])
		if(better_string(lista[i][0]) == colisor):
			c = 1
			lista[i][place] = valor
	if(not c):
		lista.append([colisor,valor])
	return lista

##################################################################################################			Grupo "files", analisa extensão e coleta de cada linha

							#função responsável por abrir o arquivo e coletar cada uma das linhas
def readFile(caminho):
	certo = 1
	erro = []
	arquivo = []	
	try:	
		with io.open(caminho, "r", encoding = "utf8") as file:		
			nLinha = 1
			for linha in file:			
				linha = str(linha)
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
def fileTipe(caminho):
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
def break_matriz(r_arquivo, separador):
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
def clean_matriz(arquivo, plus):
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
def eixo_matrizRight(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(1, len(arquivo[0])):
		(c, e, a, o1, o2) = better_valor(arquivo[0][i][2], tipo)
		a = addToMessage("No elemento da linha 1, coluna "+str(arquivo[0][i][1] + 1)+":", a)
		e = addToMessage("Erro no elemento da linha 1, coluna "+str(arquivo[0][i][1] + 1)+":", e)
		if(c):
			arquivo[0][i][2] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função de conversão de dado do eixo down
def eixo_matrizDown(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(1, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][0][2], tipo)
		a = addToMessage("No elemento da linha "+str(arquivo[i][0][0] + 1)+", coluna 1:", a)
		e = addToMessage("Erro no elemento da linha "+str(arquivo[i][0][0] + 1)+", coluna 1:", e)
		if(c):
			arquivo[i][0][2] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função de conversão de dados internos da matriz
def losdados_matriz(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(1, len(arquivo)):
		for j in range(1, len(arquivo[i])):
			(c, e, a, o1, o2) = better_valor(arquivo[i][j][2], tipo)
			a = addToMessage("No elemento da linha "+str(arquivo[i][j][0] + 1)+", coluna "+str(arquivo[i][j][1])+":", a)
			e = addToMessage("Erro no elemento da linha "+str(arquivo[i][j][0] + 1)+", coluna "+str(arquivo[i][j][1])+":", e)
			if(c):
				arquivo[i][j][2] = [o1, o2]
				aviso = addToList(aviso, a)
			else:
				certo = 0
				erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados no eixo right
def dontrepete_matrizRight(arquivo):
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
def dontrepete_matrizDown(arquivo):
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
def isthere_matrizRight(arquivo, colisor, interEntry, noticeLack):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	if(not interEntry):
		for i in range(0, len(colisor)):
			colisor[i] = better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
	else:
		for i in range(0, len(colisor)):
		
			(c, e, a, colisor[i], g) = better_valor(colisor[i], interEntry)
			colisor[i] = minuto_irredutivel(colisor[i])
			mensagem = mensagem+"\n"+minuto_paraHorario(colisor[i])
	dados = []
	colunas = []
	colunasDesconhecidas = []
	colisoresIgnorados = []
	for i in range(1, len(arquivo[0])):
		if(not interEntry):
			dados.append(arquivo[0][i][2][0])
		else:
			dados.append(minuto_irredutivel(arquivo[0][i][2][0]))
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
def isthere_matrizDown(arquivo, colisor, interEntry, noticeLack):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	if(not interEntry):
		for i in range(0, len(colisor)):
			colisor[i] = better_string(colisor[i])
			mensagem = mensagem+"\n"+colisor[i]
	else:
		for i in range(0, len(colisor)):
			(c, e, a, colisor[i], g) = better_valor(colisor[i], interEntry)
			colisor[i] = minuto_irredutivel(colisor[i])
			mensagem = mensagem+"\n"+minuto_paraHorario(colisor[i])
	dados = []
	linhas = []
	linhasDesconhecidas = []
	colisoresIgnorados = []
	for i in range(1, len(arquivo)):
		if(not interEntry):
			dados.append(arquivo[i][0][2][0])
		else:
			dados.append(minuto_irredutivel(arquivo[i][0][2][0]))
		linhas.append(i)
	for i in range(0, len(dados)):
		if(colisor.count(dados[i]) == 0):
			linhasDesconhecidas.append(linhas[i])
	if(len(linhasDesconhecidas) > 0):
		erro.append(mensagem)
		certo = 0	
		for i in range(0, len(linhasDesconhecidas)):
			if(interEntry):
				arquivo[linhasDesconhecidas[i]][0][2][0] = minuto_paraHorario(arquivo[linhasDesconhecidas[i]][0][2][0])
			mensagem = "Erro o dado ["+str(arquivo[linhasDesconhecidas[i]][0][2][0])+"] mencionado na linha "+str(arquivo[linhasDesconhecidas[i]][0][0] + 1)+" não pertence a lista de dados aceitos [impressa anteriormente]"
			erro.append(mensagem)
	if(noticeLack):
		for i in range(0, len(colisor)):
			if(dados.count(colisor[i]) == 0):
				if(interEntry):
					colisor[i] = minuto_paraHorario(colisor[i])
				if(noticeLack == 1):
					aviso.append("Aviso, não foi mencionado ["+colisor[i]+"] no arquivo")
				if(noticeLack > 1):
					certo = 0
					erro.append("Erro, não foi mencionado ["+colisor[i]+"] no arquivo")
	return certo, erro, aviso, arquivo
							#função que converte dados em informações tratáveis pelo programa que chamou
def readable_matriz(arquivo, expected_down, zero1, zero2):
	transpor = 0
	if(better_string(arquivo[0][0][2]) == better_string(expected_down)):
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
		dadosDim1 = func_transpor(dadosDim1, right, down)
		dadosDim2 = func_transpor(dadosDim2, right, down)
		aux = right
		right = down
		down = aux
	return right, down, dadosDim1, dadosDim2
							#função que preenche os dados que o programa que chamou receberá
def fill_matriz(entradaDim1, entradaDim2, currentRight, currentDown, expectedRight, expectedDown, zero1, zero2):
	matrizDim1 = []
	matrizDim2 = []
	if(expectedRight != 0):
		rightLen = len(expectedRight)
		for i in range(0, rightLen):
			expectedRight[i] = better_string(expectedRight[i])
	else:
		rightLen = len(currentRight)
	if(expectedDown != 0):
		downLen = len(expectedDown)
		for i in range(0, downLen):
			expectedDown[i] = better_string(expectedDown[i])
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
def break_simple(r_arquivo, separador1, separador2):
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
def clean_simple(arquivo, plus = ""):
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
def eixo_simpleUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][0][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", e)
		if(c):
			arquivo[i][0][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados do eixo up
def dontrepete_simpleUp(arquivo):
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
def losdados_simple(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		for j in range(0, len(arquivo[i][1])):
			(c, e, a, o1, o2) = better_valor(arquivo[i][1][j][2], tipo)
			a = addToMessage("No "+str(arquivo[i][1][j][1] + 1)+"° elemento da linha "+str(arquivo[i][1][j][0] + 1)+", após o dado inicial:", a)
			e = addToMessage("Erro no "+str(arquivo[i][1][j][1] + 1)+"° elemento da linha "+str(arquivo[i][1][j][0] + 1)+", após o dado inicial:", e)
			if(c):
				arquivo[i][1][j][2] = [o1, o2]
				aviso = addToList(aviso, a)
			else:
				certo = 0
				erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados além dos do eixo up na mesma linha
def dontrepete_simpleDados(arquivo):
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
def isthere_simpleUp(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere_simpleDados(arquivo, colisor):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def readable_simple(arquivo, zero1 = 0, one1 = 1, zero2 = 0):
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
def fill_simple(entradaDim1, entradaDim2, currentUp, currentDados, expectedUp = 0, expectedDados = 0, zero1 = 0, zero2 = 0):
	matrizDim1 = []
	matrizDim2 = []
	if(expectedUp != 0):
		upLen = len(expectedUp)
		for i in range(0, upLen):
			expectedUp[i] = better_string(expectedUp[i])
	else:
		upLen = len(currentUp)
	if(expectedDados != 0):
		dadosLen = len(expectedDados)
		for i in range(0, dadosLen):
			expectedDados[i] = better_string(expectedDados[i])
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
def break_complex(r_arquivo, separador1, separador2, separador3):
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
def clean_complex(arquivo, lim, plus = ""):
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
def eixo_complexUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][0][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0][0] + 1)+":", e)
		if(c):
			arquivo[i][0][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados do eixo up
def dontrepete_complexUp(arquivo):
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
def losdados_complex(arquivo, tipos):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		for j in range(0, len(arquivo[i][1])):
			for k in range(0, len(arquivo[i][1][j])):
				(c, e, a, o1, o2) = better_valor(arquivo[i][1][j][k][3], tipos[k])
				a = addToMessage("No "+str(arquivo[i][1][j][k][2] + 1)+"° elemento do "+str(arquivo[i][1][j][k][1] + 1)+"° conjunto da linha "+str(arquivo[i][1][j][k][0] + 1)+":", a)
				e = addToMessage("Erro no "+str(arquivo[i][1][j][k][2] + 1)+"° elemento do "+str(arquivo[i][1][j][k][1] + 1)+"° conjunto da linha "+str(arquivo[i][1][j][k][0] + 1)+":", e)
				if(c):
					arquivo[i][1][j][k][3] = [o1, o2]
					aviso = addToList(aviso, a)
				else:
					certo = 0
					erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados além dos do eixo up na mesma linha
def dontrepete_complexDados(arquivo):
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
def isthere_complexUp(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere_complexDados(arquivo, colisor):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def readable_complex(arquivo, zeros1, zeros2, specialOne1 = 0, specialOne2 = 0):
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
def fill_complex(entradasDim1, entradasDim2, currentUp, currentDados, expectedUp = 0, expectedDados = 0, zero1 = 0, zero2 = 0):
	if(expectedUp != 0):
		upLen = len(expectedUp)
		for i in range(0, upLen):
			expectedUp[i] = better_string(expectedUp[i])
	else:
		upLen = len(currentUp)
	if(expectedDados != 0):
		dadosLen = len(expectedDados)
		for i in range(0, dadosLen):
			expectedDados[i] = better_string(expectedDados[i])
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
def break_couple(r_arquivo, separador):
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
def clean_couple(arquivo, plus = ""):
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
def eixo_coupleUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados do eixo up
def dontrepete_coupleUp(arquivo):
	certo = 1
	erro = []
	dados = []
	linhas = []
	linhasRepetidas = []
	repetidos = []
	for i in range(0, len(arquivo)):
		dados.append(better_string(arquivo[i][1][0]))
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
def losdados_couple(arquivo, tipo, pasta = ""):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
			arquivo[i][2] = pasta+"/"+arquivo[i][2]
		(c, e, a, o1, o2) = better_valor(arquivo[i][2], tipo)
		a = addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][2] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função de conversão de dados além dos do eixo up, sendo todos tratados de acordo com o valor do eixo up associado
def losdados_fixedcouple(arquivo, relacoes):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][2], getValue(relacoes, arquivo[i][1][0]))
		a = addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][2] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que verifica a coerência com dados do eixo up
def isthere_coupleUp(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere_coupleDados(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def readable_couple(arquivo):
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
def fill_couple(currentUpDim1, currentUpDim2, currentDadosDim1, currentDadosDim2, expectedUp, zero = 0, zeros = 0):
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
			expectedUp[i] = better_string(expectedUp[i])
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
	return upDim1, upDim2, colide(expectedUp, listaDim1), colide(expectedUp, listaDim2)

##################################################################################################			Grupo que trata a estrutura single

							#função de quebra
def break_single(r_arquivo):
	arquivo = []
	for i in range(0, len(r_arquivo)):
		arquivo.append([i, r_arquivo[i].strip()])
	return arquivo
							#função de limpeza
def clean_single(arquivo, plus = ""):
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
def eixo_singleUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados do eixo up
def dontrepete_singleUp(arquivo):
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
def readable_single(arquivo):
	upDim1 = []
	upDim2 = []
	for i in range(0, len(arquivo)):
		upDim1.append(arquivo[i][1][0])
		upDim2.append(arquivo[i][1][1])
	return upDim1, upDim2

##################################################################################################			Grupo que trata a estrutura line

							#função de quebra
def break_line(r_arquivo, separador):
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
def clean_line(arquivo, plus = ""):
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
def losdados_line(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		for j in range(0, len(arquivo[i])):
			(c, e, a, o1, o2) = better_valor(arquivo[i][j][2], tipo)
			a = addToMessage("No "+str(arquivo[i][j][1] + 1)+"° elemento da linha "+str(arquivo[i][j][0] + 1)+", após o dado inicial:", a)
			e = addToMessage("Erro no "+str(arquivo[i][j][1] + 1)+"° elemento da linha "+str(arquivo[i][j][0] + 1)+", após o dado inicial:", e)
			if(c):
				arquivo[i][j][2] = o1
				aviso = addToList(aviso, a)
			else:
				certo = 0
				erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados na mesma linha
def dontrepete_lineDados(arquivo):
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
def isthere_lineDados(arquivo, colisor):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def fill_line(arquivo, expectedDados, zero = 0):
	matriz = []
	dadosLen = len(expectedDados)
	for i in range(0, dadosLen):
		expectedDados[i] = better_string(expectedDados[i])
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
def break_four(r_arquivo, separador):
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
def clean_four(arquivo, plus = ""):
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
					print(arquivo[i])
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
def eixo_fourUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados no eixo up
def dontrepete_fourUp(arquivo):
	certo = 1
	erro = []
	dados = []
	linhas = []
	linhasRepetidas = []
	repetidos = []
	for i in range(0, len(arquivo)):
		dados.append(better_string(arquivo[i][1][0]))
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
def losdados1_four(arquivo, tipo, pasta = ""):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
			arquivo[i][2] = pasta+"/"+arquivo[i][2]
		(c, e, a, o1, o2) = better_valor(arquivo[i][2], tipo)
		a = addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][2] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função de conversão dos dados2
def losdados2_four(arquivo, tipo, pasta = ""):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
			arquivo[i][3] = pasta+"/"+arquivo[i][3]
		(c, e, a, o1, o2) = better_valor(arquivo[i][3], tipo)
		a = addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][3] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função de conversão dos dados3
def losdados3_four(arquivo, tipo, pasta = ""):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		if(tipo.strip().upper() == "ARQUIVO" and pasta != ""):
			arquivo[i][4] = pasta+"/"+arquivo[i][4]
		(c, e, a, o1, o2) = better_valor(arquivo[i][4], tipo)
		a = addToMessage("O elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no elemento após o dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][4] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que verifica a coerência externa do eixo up
def isthere_fourUp(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere1_fourDados(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere2_fourDados(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def isthere3_fourDados(arquivo, colisor, noticeLack = 0):
	certo = 1
	erro = []
	aviso = []
	mensagem = "São aceitos as seguintes dados:"
	for i in range(0, len(colisor)):
		colisor[i] = better_string(colisor[i])
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
def readable_four(arquivo):
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
def break_doubled(r_arquivo):
	arquivo = []
	for i in range(0, len(r_arquivo)):
		arquivo.append([i, r_arquivo[i].strip()])
	return arquivo
							#função de limpeza
def clean_doubled(arquivo, plus = ""):

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
def eixo_doubled(arquivo, tipo):

	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
			
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados no eixo up
def dontrepete_doubled(arquivo):
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
def isthere_doubled(arquivo, colisor1, colisor2):
	certo = 1
	erro = []
	aviso = []
	
	mensagem1 = "São aceitos as seguintes dados [quando usado nada ou !]:"
	for i in range(0, len(colisor1)):
		colisor1[i] = better_string(colisor1[i])
		mensagem1 = mensagem1+"\n"+colisor1[i]
	mensagem2 = "São aceitos as seguintes dados [quando usado @]:"
	for i in range(0, len(colisor2)):
		colisor2[i] = better_string(colisor2[i])
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
def readable_doubled(arquivo):

	upDim1 = []
	upDim2 = []
	
	for i in range(0, len(arquivo)):
		upDim1.append(arquivo[i][1][0])
		upDim2.append(arquivo[i][1][1])
		
	return upDim1, upDim2

##################################################################################################			Grupo que trata a estrutura especial single

							#função de quebra
def break_especialSingle(r_arquivo):
	arquivo = []
	for i in range(0, len(r_arquivo)):
		arquivo.append([i, r_arquivo[i].strip()])
	return arquivo
							#função de limpeza
def clean_especialSingle(arquivo, plus = ""):
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
def eixo_especialSingleUp(arquivo, tipo):
	certo = 1
	erro = []
	aviso = []
	for i in range(0, len(arquivo)):
		(c, e, a, o1, o2) = better_valor(arquivo[i][1], tipo)
		a = addToMessage("No dado inicial da linha "+str(arquivo[i][0] + 1)+":", a)
		e = addToMessage("Erro no dado inicial da linha "+str(arquivo[i][0] + 1)+":", e)
		if(c):
			arquivo[i][1] = [o1, o2]
			aviso = addToList(aviso, a)
		else:
			certo = 0
			erro = addToList(erro, e)
	return certo, erro, aviso, arquivo
							#função que impede repetição de dados do eixo up
def dontrepete_especialSingleUp(arquivo):
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
def readable_especialSingle(arquivo, out):
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
def trate_matriz(arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
	right = []
	down = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_matriz(arquivo, break_rules)
	(c, e, a, arquivo) = clean_matriz(arquivo, nome)
	imprimeArray(a)
	if(c):
		oc0 = 0
		oc1 = 1
		if(better_string(arquivo[0][0][2]) == better_string(readable_rules[0])):
			oc0 = 1
			oc1 = 0
		(c, e, a, arquivo) = eixo_matrizRight(arquivo, eixo_rules[oc0])
		imprimeArray(a)
		if(c):
			(c, e, a, arquivo) = eixo_matrizDown(arquivo, eixo_rules[oc1])
			imprimeArray(a)
			if(c):
				(c, e, a, arquivo) = losdados_matriz(arquivo, losdados_rules)
				imprimeArray(a)
				if(c):
					(c, e, arquivo) = dontrepete_matrizRight(arquivo)
					if(c):
						(c, e, arquivo) = dontrepete_matrizDown(arquivo)
						if(c):
							if(isthere_rules[oc0][0]):
								(c, e, a, arquivo) = isthere_matrizRight(arquivo, isthere_rules[oc0][1], isthere_rules[oc0][2], isthere_rules[oc0][3])
								imprimeArray(a)
								if(not c):
									imprimeArray(e)
							if(c):
								if(isthere_rules[oc1][0]):
									(c, e, a, arquivo) = isthere_matrizDown(arquivo, isthere_rules[oc1][1], isthere_rules[oc1][2], isthere_rules[oc1][3])
									imprimeArray(a)
									if(not c):
										imprimeArray(e)
								if(c):
									(right, down, dadosDim1, dadosDim2) = readable_matriz(arquivo, readable_rules[0], readable_rules[1], readable_rules[2])
									(dadosDim1, dadosDim2) = fill_matriz(dadosDim1, dadosDim2, right, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
									if(fill_rules[0] != 0):
										right = fill_rules[0]
									if(fill_rules[1] != 0):
										down = fill_rules[1]
						else:
							imprimeArray(e)
					else:
						imprimeArray(e)
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, right, down, dadosDim1, dadosDim2
							#função responsável pela estrutura simple
def trate_simple(arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
	up = []
	down = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_simple(arquivo, break_rules[0], break_rules[1])
	(c, e, a, arquivo) = clean_simple(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_simpleUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_simpleUp(arquivo)
			if(c):
				(c, e, a, arquivo) = losdados_simple(arquivo, losdados_rules)
				imprimeArray(a)
				if(c):
					(c, e, arquivo) = dontrepete_simpleDados(arquivo)
					if(c):
						if(isthere_rules[0][0]):
							(c, e, a, arquivo) = isthere_simpleUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
							imprimeArray(a)
							if(not c):
								imprimeArray(e)
						if(c):
							if(isthere_rules[1][0]):
								(c, e, a, arquivo) = isthere_simpleDados(arquivo, isthere_rules[1][1])
								imprimeArray(a)
								if(not c):
									imprimeArray(e)
							if(c):
								(up, down, dadosDim1, dadosDim2) = readable_simple(arquivo,readable_rules[0], readable_rules[1], readable_rules[2])
								(dadosDim1, dadosDim2) = fill_simple(dadosDim1, dadosDim2, up, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
								if(fill_rules[0] != 0):
									up = fill_rules[0]
								if(fill_rules[1] != 0):
									down = fill_rules[1]
					else:
						imprimeArray(e)
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)	
	else:
		imprimeArray(e)
	return c, up, down, dadosDim1, dadosDim2
							#função responsável pela estrutura complex
def trate_complex(arquivo, nome, break_rules, clean_rules, eixo_rules, isthere_rules, losdados_rules, readable_rules, fill_rules):
	up = []
	down = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_complex(arquivo, break_rules[0], break_rules[1], break_rules[2])
	(c, e, a, arquivo) = clean_complex(arquivo, clean_rules, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_complexUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_complexUp(arquivo)
			if(c):
				(c, e, a, arquivo) = losdados_complex(arquivo, losdados_rules)
				imprimeArray(a)
				if(c):
					(c, e, arquivo) = dontrepete_complexDados(arquivo)
					if(c):
						if(isthere_rules[0][0]):
							(c, e, a, arquivo) = isthere_complexUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
							imprimeArray(a)
							if(not c):
								imprimeArray(e)
						if(c):
							if(isthere_rules[1][0]):
								(c, e, a, arquivo) = isthere_complexDados(arquivo, isthere_rules[1][1])
								imprimeArray(a)
								if(not c):
									imprimeArray(e)
							if(c):
								(up, down, dadosDim1, dadosDim2) = readable_complex(arquivo, readable_rules[0], readable_rules[1], readable_rules[2], readable_rules[3])
								(dadosDim1, dadosDim2) = fill_complex(dadosDim1, dadosDim2, up, down, fill_rules[0], fill_rules[1], fill_rules[2], fill_rules[3])
								if(fill_rules[0] != 0):
									up = fill_rules[0]
								if(fill_rules[1] != 0):
									down = fill_rules[1]
								if(clean_rules == 2):
									dadosDim1 = dadosDim1[0]
									dadosDim2 = dadosDim2[0]
						else:
							imprimeArray(e)
					else:
						imprimeArray(e)
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, up, down, dadosDim1, dadosDim2
							#função responsável pela estrutura couple
def trate_couple(arquivo, nome, break_rules, eixo_rules, isthere_rules, losdados_rules, fill_rules):
	upDim1 = []
	upDim2 = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_couple(arquivo, break_rules)
	(c, e, a, arquivo) = clean_couple(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_coupleUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_coupleUp(arquivo)
			if(c):
				if(not losdados_rules[0]):
					(c, e, a, arquivo) = losdados_couple(arquivo, losdados_rules[1], losdados_rules[2])
				else:
					(c, e, a, arquivo) = losdados_fixedcouple(arquivo, losdados_rules[1])
				imprimeArray(a)
				if(c):
					if(len(isthere_rules) != 2):
						if(isthere_rules[0]):
							(c, e, a, arquivo) = isthere_coupleUp(arquivo, isthere_rules[1], isthere_rules[2])
							imprimeArray(a)
							if(not c):
								imprimeArray(e)
					else:
						if(isthere_rules[0][0]):
							(c, e, a, arquivo) = isthere_coupleUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
							imprimeArray(a)
							if(not c):
								imprimeArray(e)
					if(c):
						if(len(isthere_rules) == 2):
							if(isthere_rules[1][0]):
								(c, e, a, arquivo) = isthere_coupleDados(arquivo, isthere_rules[1][1], isthere_rules[1][2])
								imprimeArray(a)
								if(not c):
									imprimeArray(e)
						if(c):
							(upDim1, upDim2, dadosDim1, dadosDim2) = readable_couple(arquivo)
							if(fill_rules[0]):
								(upDim1, upDim2, dadosDim1, dadosDim2) = fill_couple(upDim1, upDim2, dadosDim1, dadosDim2, fill_rules[1], fill_rules[2], fill_rules[3])
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, upDim1, upDim2, dadosDim1, dadosDim2
							#função responsável pela estrutura single
def trate_single(arquivo, nome, eixo_rules):
	upDim1 = []
	upDim2 = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_single(arquivo)
	(c, e, a, arquivo) = clean_single(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_singleUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_singleUp(arquivo)
			if(c):
				(upDim1, upDim2) = readable_single(arquivo)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, upDim1, upDim2
							#função responsável pela estrutura line
def trate_line(arquivo, nome, break_rules, isthere_rules, losdados_rules, fill_rules):
	dados = []
	arquivo = break_line(arquivo, break_rules)
	(c, e, a, arquivo) = clean_line(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = losdados_line(arquivo, losdados_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_lineDados(arquivo)
			if(c):
				if(isthere_rules):
					(c, e, a, arquivo) = isthere_lineDados(arquivo, isthere_rules)
					imprimeArray(a)
					if(not c):
						imprimeArray(e)
				if(c):
					(dados) = fill_line(arquivo, isthere_rules, fill_rules)
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, dados
							#função responsável pela estrutura four
def trate_four(arquivo, nome, break_rules, eixo_rules, losdados_rules, isthere_rules):
	up = []
	dados1 = []
	dados2 = []
	dados3 = []
	arquivo = break_four(arquivo, break_rules)
	(c, e, a, arquivo) = clean_four(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_fourUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_fourUp(arquivo)
			if(c):
				(c, e, a, arquivo) = losdados1_four(arquivo, losdados_rules[1], losdados_rules[2])
				imprimeArray(a)
				if(c):
					(c, e, a, arquivo) = losdados2_four(arquivo, losdados_rules[3], losdados_rules[4])
					imprimeArray(a)
					if(c):
						(c, e, a, arquivo) = losdados3_four(arquivo, losdados_rules[5], losdados_rules[6])
						imprimeArray(a)
						if(c):
							if(isthere_rules[0][0]):
								(c, e, a, arquivo) = isthere_fourUp(arquivo, isthere_rules[0][1], isthere_rules[0][2])
								imprimeArray(a)
								if(not c):
									imprimeArray(e)
							if(c):
								if(isthere_rules[1][0]):
									(c, e, a, arquivo) = isthere1_fourDados(arquivo, isthere_rules[1][1], isthere_rules[1][2])
									imprimeArray(a)
									if(not c):
										imprimeArray(e)
								if(c):
									if(isthere_rules[2][0]):
										(c, e, a, arquivo) = isthere2_fourDados(arquivo, isthere_rules[2][1], isthere_rules[2][2])
										imprimeArray(a)
										if(not c):
											imprimeArray(e)
									if(c):
										if(isthere_rules[1][0]):
											(c, e, a, arquivo) = isthere3_fourDados(arquivo, isthere_rules[3][1], isthere_rules[3][2])
											imprimeArray(a)
											if(not c):
												imprimeArray(e)
										if(c):
											(up, dados1, dados2, dados3) = readable_four(arquivo)
						else:
							imprimeArray(e)
					else:
						imprimeArray(e)
				else:
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, up, dados1, dados2, dados3
							#função responsável pela estrutura doubled // não usada, inacessível
def trate_doubled(arquivo, nome, eixo_rules, isthere_rules):
	upDim1 = []
	upDim2 = []
	arquivo = break_doubled(arquivo)
	(c, e, a, arquivo) = clean_doubled(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_doubled(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_doubled(arquivo)
			if(c):
				(c, e, a, arquivo) = isthere_doubled(arquivo, isthere_rules[0], isthere_rules[1])
				imprimeArray(a)
				if(not c):
					imprimeArray(e)
				if(c):
					(upDim1, upDim2) = readable_doubled(arquivo)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, upDim1, upDim2
							#função responsável pela estrutura single
def trate_especialSingle(arquivo, nome, eixo_rules, readable_rules):
	upDim1 = []
	upDim2 = []
	dadosDim1 = []
	dadosDim2 = []
	arquivo = break_especialSingle(arquivo)
	(c, e, a, arquivo) = clean_especialSingle(arquivo, nome)
	imprimeArray(a)
	if(c):
		(c, e, a, arquivo) = eixo_especialSingleUp(arquivo, eixo_rules)
		imprimeArray(a)
		if(c):
			(c, e, arquivo) = dontrepete_especialSingleUp(arquivo)
			if(c):
				(c, e, upDim1, upDim2) = readable_especialSingle(arquivo, readable_rules)
				if(not c):
					imprimeArray(e)
			else:
				imprimeArray(e)
		else:
			imprimeArray(e)
	else:
		imprimeArray(e)
	return c, upDim1, upDim2
							#função rsponsável por, de acordo com o arquivo, aplicar o tratamento de estrutura necessário
def trate(fileName, fortxt, forcsv, fortwocsv, fortwotxt):
	inverte = 0
	(iscsv, ismorethantwo) = fileTipe(fileName)
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
	(c, e, file) = readFile(fileName)
	if(c):
		print("\nEstamos extraindo os dados do arquivo ["+fileName+"]")
		if(estrutura == 0):
			(c, right, down, dadosDim1, dadosDim2) = trate_matriz(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5])
			if(len(parametros) == 7):
				if(parametros[6]):
					dadosDim1 = func_transpor(dadosDim1, right, down)
					dadosDim2 = func_transpor(dadosDim2, right, down)
			if(inverte):
				aux = right
				right = down
				down = aux
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, right, down, dadosDim1, dadosDim2
		elif(estrutura == 1):
			(c, up, down, dadosDim1, dadosDim2) = trate_simple(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5])
			if(inverte):
				aux = up
				up = down
				down = aux
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, up, down, dadosDim1, dadosDim2
		elif(estrutura == 2):
			(c, up, down, dadosDim1, dadosDim2) = trate_complex(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4], parametros[5], parametros[6])
			if(inverte):
				aux = up
				up = down
				down = aux
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, up, down, dadosDim1, dadosDim2
		elif(estrutura == 3):
			(c, up, down, dadosDim1, dadosDim2) = trate_couple(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3], parametros[4])
			if(inverte):
				aux = up
				up = down
				down = aux
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, up, down, dadosDim1, dadosDim2
		elif(estrutura == 5): #REPARE O 5
			(c, dados) = trate_line(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3])
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, dados
		elif(estrutura == 6): #REPARE O 6
			(c, up, dados1, dados2, dados3) = trate_four(file, fileName, parametros[0], parametros[1], parametros[2], parametros[3])
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, up, dados1, dados2, dados3
		elif(estrutura == 7): #REPARE O 7
			(c, upDim1, upDim2) = trate_especialSingle(file, fileName, parametros[0], parametros[1])
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, upDim1, upDim2
		else:
			(c, dadosDim1, dadosDim2) = trate_single(file, fileName, parametros[0])
			if(c):
				print("Acabamos de extrair os dados com sucesso do arquivo ["+fileName+"]\n")
			else:
				print("Acabamos de extrair os dados sem sucesso do arquivo ["+fileName+"]\n")
			return c, dadosDim1, dadosDim2
	else:
		imprimeArray(e)
	if(estrutura > 3 and estrutura != 6 and estrutura != 5):
		return c, 0, 0
	elif(estrutura == 5):
		return c, 0
	else:
		return c, 0, 0, 0, 0

##################################################################################################
#							Fim
##################################################################################################