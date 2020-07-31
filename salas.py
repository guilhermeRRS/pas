from mip import *
import io, time
from pacotePadrao import *

time_inicio = time.time()

arquivoInicial = "salas.in"
campos_arquivoInicial = ["Pasta dados", "Pasta Solução", "Lista entradas", "Arquivo Constantes"]
tipos_arquivoInicial = [["Pasta dados", "pasta"], ["Pasta Solução", "arquivo"],["Lista entradas","arquivo"],["Arquivo Constantes","arquivo"],["TimeMax","numerico"],["SolucoesMax","numerico"]]

nomes_arquivosDados = ["HorariosId","GradeHoraria","SalasCapacidades","DisciplinasTamanhos","SalasRecursos","DisciplinasRecursos","SalasPref","CurriculosDisciplinas","CurriculosSalas","Distancias"]

campos_constantes = ["Constante trocas de sala","Constante desperdício salas","Constante distâncias","Constante preferência salas","Constante preferência currículos"]
Constantes = [["Constante trocas de sala",1],["Constante desperdício salas",1],["Constante distâncias",1],["Constante preferência salas",1],["Constante preferência currículos",1]]

(c, g, g, mainConfs, g) = trate(arquivoInicial, 
	[0, 3,
		":",
		"texto",
		[1, campos_arquivoInicial, 1],
		[1, tipos_arquivoInicial],
		[1, campos_arquivoInicial, "", 0]
	],
	[0, 3,
		";",
		"texto",
		[1, campos_arquivoInicial, 1],
		[1, tipos_arquivoInicial],
		[1, campos_arquivoInicial, "", 0]
	],
	0,
	0
)

if(c):
	mainConfs_pastaDados = getValue(mainConfs, "Pasta dados")
	mainConfs_pastaSolucao= getValue(mainConfs, "Pasta solução")
	mainConfs_listaEntradas = getValue(mainConfs, "Lista entradas")
	mainConfs_ArquivoConstantes = getValue(mainConfs, "Arquivo Constantes")

if(c):

	if(mainConfs_pastaSolucao == ""):
		
		print("Aviso: Não foi indicado uma pasta para ser inserida a solução, no arquivo ["+arquivoInicial+"], colocaremos no mesmo diretório que ["+arquivoInicial+"]")
		
	if(mainConfs_listaEntradas == ""):
		c = 0
		print("ERRO: Não foi indicado um arquivo com a lista dos arquivos de dados, no arquivo ["+arquivoInicial+"]")
	
	if(mainConfs_ArquivoConstantes == ""):
		print("Aviso, não foi indicado um arquivo com o valor das constantes do modelo, no arquivo ["+arquivoInicial+"]. Consideraremos o valor de todas um")

if(c):
	
	fileName = mainConfs_listaEntradas
	(c, g, g, entradasLista, g) = trate(fileName, 
		[0, 3,
			":",
			"texto",
			[1, nomes_arquivosDados, 1],
			[0, "arquivo", mainConfs_pastaDados],
			[1, nomes_arquivosDados, "", 0]
		],
		[0, 3,
			";",
			"texto",
			[1, nomes_arquivosDados, 1],
			[0, "arquivo", mainConfs_pastaDados],
			[1, nomes_arquivosDados, "", 0]
		],
		0,
		0
	)
	
	if(getValue(entradasLista, "HorariosId") == ""):
		c = 0
		print("Aviso: Não foi indicado um arquivo com os IDs dos horários")
	if(getValue(entradasLista, "GradeHoraria") == ""):
		c = 0
		print("Aviso: Não foi indicado um arquivo com a grade horária das turmas")

if(c):
	
	if(getValue(mainConfs, "TimeMax") == 0):
		mainConfs = setValue(mainConfs, "TimeMax", 3600)
		print("Aviso rápido e importante: Limitamos o tempo de solução do problema para uma hora, caso queira processar mais/menos, reinicie o programa (sugerimos aumentar para o maior tempo que lhe for possível), definindo o valor no arquivo ["+arquivoInicial+"]")

	print("\nAgora vamos começar a coletar os dados do problema!\n\n")
	leituraSucesso = 1
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
	
	fileName = getValue(entradasLista, "HorariosId")
	if(fileName != ""):
		(c, I_HorariosN, g, I_HorariosM, g) = trate(fileName,
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
		if(not c):
			leituraSucesso = c
		else:
			I_Horarios = colide(I_HorariosN, I_HorariosM)
	fileName = getValue(entradasLista, "GradeHoraria")
	if(fileName != "" and I_Horarios):
		(c, horariosLinha, I_Disciplinas, gradeHoraria, g) = trate(fileName,
			[1, 1,
				[":", ";"],
				"texto",
				[
					[
						0
					],
					[
						1,
						I_HorariosN
					],
				],
				"texto",
				[0, 1, 0],
				[0, I_HorariosN, 0, 0]
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
						I_HorariosN
					],
				],
				"texto",
				[0, 1, 0],
				[0, I_HorariosN, 0, 0]
			],
			[0, 0,
				";",
				["texto", "texto"],
				[
					[
						1,
						I_HorariosN,
						0,
						1
					],
					[
						0
					]
				],
				"BIN",
				["DISCIPLINAS", 0, 0],
				[I_HorariosN, 0, 0, 0]
			],
			0
		)
		if(not c):
			leituraSucesso = c
		else:
			horarios = []
			for j in range(len(I_Horarios)):
				horarios.append(getValue(I_Horarios, horariosLinha[j]))
			
			I_Aulas = []
			disciplinasDeletar = []
			for i in range(len(I_Disciplinas)):
				existe = 0
				for j in range(len(horarios)):
					if(gradeHoraria[i][j]):
						existe = 1
						I_Aulas.append([I_Disciplinas[i], horarios[j]])
				if(not existe):
					disciplinasDeletar.append(i)
			i = len(disciplinasDeletar) - 1
			while(i >= 0):
				print("A disciplina ["+I_Disciplinas[disciplinasDeletar[i]]+"] será deletada pois não foi associada a nenhum horário")
				del I_Disciplinas[disciplinasDeletar[i]]
				i -= 1
	fileName = getValue(entradasLista, "SalasCapacidades")
	if(fileName != ""):
		(c, I_Salas, g, C_SalasCapacidades, g) = trate(fileName, 
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
			I_Salas = 0
			C_SalasCapacidades = 0
			leituraSucesso = c
		else:
			C_SalasCapacidades = colide(I_Salas, C_SalasCapacidades) #É necessário pois não foi indicado nada em fill // Não era possível o fazer
	fileName = getValue(entradasLista, "DisciplinasTamanhos")
	if(fileName != "" and I_Disciplinas):
		(c, g, g, C_DisciplinasTamanhos, g) = trate(fileName, 
			[0, 3,
				":",
				"texto",
				[
					1,
					I_Disciplinas,
					1
				],
				[0, "Numerico", 0],
				[1, I_Disciplinas, 0, 0]
			],
			[0, 3,
				";",
				"texto",
				[
					1,
					I_Disciplinas,
					1
				],
				[0, "Numerico", 0],
				[1, I_Disciplinas, 0, 0]
			],
			0,
			0
		)
		if(not c):
			C_DisciplinasTamanhos = 0
			leituraSucesso = c
	fileName = getValue(entradasLista, "SalasRecursos")
	if(fileName != "" and I_Salas):
		(c, I_Recursos, g, R_SalasRecursos, g) = trate(fileName,
			[1, 2,
				[":", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Salas,
						1
					],
					[
						0
					],
				],
				["texto","numerico"],
				[[0], [0], [1], [0]],
				[I_Salas, 0, 0, 0]
			],
			[1, 2,
				[";", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Salas,
						1
					],
					[
						0
					],
				],
				["texto","numerico"],
				[[0], [0], [1], [0]],
				[I_Salas, 0, 0, 0]
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
						I_Salas,
						0,
						1
					]
				],
				"NUMERICO",
				["SALAS", 0, 0],
				[0, I_Salas, 0, 0]
			],
			0
		)
		if(not c):
			I_Recursos = 0
			R_SalasRecursos = 0
			leituraSucesso = c
	fileName = getValue(entradasLista, "DisciplinasRecursos")
	if(fileName != "" and I_Disciplinas and I_Recursos):
		(c, g, g, R_DisciplinasRecursos, g) = trate(fileName,
			[1, 2,
				[":", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Disciplinas,
						1
					],
					[
						1,
						I_Recursos,
						1
					],
				],
				["texto","numerico"],
				[[0], [0], [1], [0]],
				[I_Disciplinas, I_Recursos, 0, 0]
			],
			[1, 2,
				[";", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Disciplinas,
						1
					],
					[
						1,
						I_Recursos,
						1
					],
				],
				["texto","numerico"],
				[[0], [0], [1], [0]],
				[I_Disciplinas, I_Recursos, 0, 0]
			],
			[0, 0,
				";",
				["texto", "texto"],
				[
					[
						1,
						I_Recursos,
						0,
						1
					],
					[
						1,
						I_Disciplinas,
						0,
						1
					]
				],
				"NUMERICO",
				["DISCIPLINAS", 0, 0],
				[I_Recursos, I_Disciplinas, 0, 0]
			],
			0
		)
		if(not c):
			R_DisciplinasRecursos = 0
			leituraSucesso = c
	fileName = getValue(entradasLista, "SalasPref")
	if(fileName != "" and I_Salas):
		(c, g, g, C_SalasPref, g) = trate(fileName, 
			[0, 3,
				":",
				"texto",
				[
					1,
					I_Salas,
					1
				],
				[0, "BIN", 0],
				[1, I_Salas, 0, 0]
			],
			[0, 3,
				";",
				"texto",
				[
					1,
					I_Salas,
					1
				],
				[0, "BIN", 0],
				[1, I_Salas, 0, 0]
			],
			0,
			0
		)
		if(not c):
			leituraSucesso = c
		else:
			for i in range(len(I_Salas)):
				C_SalasPref[i][1] = - C_SalasPref[i][1]
	else:
		if(I_Salas):
			C_SalasPref = []
			for i in range(len(I_Salas)):
				C_SalasPref.append([I_Salas[i],0])
	fileName = getValue(entradasLista, "CurriculosDisciplinas")
	if(fileName != "" and I_Disciplinas):
		(c, I_Curriculos, g, R_CurriculosDisciplinas, g) = trate(fileName,
			[0, 1,
				[":", ";"],
				"texto",
				[
					[
						0
					],
					[
						1,
						I_Disciplinas
					],
				],
				"texto",
				[0, 1, 0],
				[0, I_Disciplinas, 0, 0]
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
						I_Disciplinas
					],
				],
				"texto",
				[0, 1, 0],
				[0, I_Disciplinas, 0, 0]
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
						I_Disciplinas,
						0,
						1
					]
				],
				"BIN",
				["DISCIPLINAS", 0, 0],
				[0, I_Disciplinas, 0, 0],
				1
			],
			0
		)
		if(not c):
			I_Curriculos = 0
			R_CurriculosDisciplinas = 0
			leituraSucesso = c
	fileName = getValue(entradasLista, "CurriculosSalas")
	if(fileName != "" and I_Salas and I_Curriculos):
		(c, g, g, g, valor) = trate(fileName,
			[0, 2,
				[":", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Curriculos,
						1
					],
					[
						1,
						I_Salas,
						1
					],
				],
				["texto","texto"],
				[[0], [0], [0], [2]],
				[I_Curriculos, I_Salas, 0, 0]
			],
			[0, 2,
				[":", ";", ":"],
				2,
				"texto",
				[
					[
						1,
						I_Curriculos,
						1
					],
					[
						1,
						I_Salas,
						1
					],
				],
				["texto","texto"],
				[[0], [0], [0], [2]],
				[I_Curriculos, I_Salas, 0, 0]
			],
			[0, 0,
				";",
				["texto", "texto"],
				[
					[
						1,
						I_Salas,
						0,
						1
					],
					[
						1,
						I_Curriculos,
						0,
						1
					]
				],
				"texto",
				["CURRICULOS", 0, 0],
				[I_Salas, I_Curriculos, 0, 0]
			],
			0
		)
		if(not c):
			leituraSucesso = c
		else:
			Rd_CurriculosSalas = []
			for i in range(len(I_Curriculos)):
				Rd_CurriculosSalas.append([])
				for j in range(len(I_Salas)):
					Rd_CurriculosSalas[-1].append(-valor[i][j])
	fileName = getValue(entradasLista, "Distancias")
	if(fileName != "" and I_Salas):
		(c, g, g, R_Distancias, g) = trate(fileName,
			[0, 0,
				";",
				["texto", "texto"],
				[
					[
						1,
						I_Salas,
						0,
						1
					],
					[
						1,
						I_Salas,
						0,
						1
					]
				],
				"NUMERICO",
				["ORIGENS", 0, 0],
				[I_Salas, I_Salas, 0, 0]
			],
			[0, 0,
				";",
				["texto", "texto"],
				[
					[
						1,
						I_Salas,
						0,
						1
					],
					[
						1,
						I_Salas,
						0,
						1
					]
				],
				"NUMERICO",
				["ORIGENS", 0, 0],
				[I_Salas, I_Salas, 0, 0]
			],
			0,
			0
		)
		if(not c):
			R_Distancias = 0
			leituraSucesso = c
	
	fileName = mainConfs_ArquivoConstantes
	if(fileName != ""):
		(c, g, g, Constantes, g) = trate(fileName, 
			[0, 3,
				":",
				"texto",
				[1, campos_constantes, 1],
				[0, "Numerico", 0],
				[1, campos_constantes, 1, 0]
			],
			[0, 3,
				";",
				"texto",
				[1, campos_constantes, 1],
				[0, "Numerico", 0],
				[1, campos_constantes, 1, 0]
			],
			0,
			0
		)
		if(not c):
			Constantes = 0
			leituraSucesso = c
	
	c = leituraSucesso

	time_coleta = time.time()
	if(time_coleta - time_inicio > 60):
		print("\nDemoramos cerca de ",int((time_coleta - time_inicio)/60)," minutos para coletarmos os dados\n")
	else:
		print("\nDemoramos cerca de ",int(time_coleta - time_inicio)," segundos para coletarmos os dados\n")

if(c): #pré-processamento

	print("Agora estamos realizando o pré-processamento - isso pode demorar um pouco")
	
	Matriz_o = []
	for i in range(len(I_Aulas)):
		Matriz_o.append([])
		for j in range(len(I_Aulas)):
			Matriz_o[-1].append(0)
	if(c):
		for i in range(len(I_Aulas)):
			for j in range(len(I_Aulas)):
				if(i != j and I_Aulas[i][0] != I_Aulas[j][0]):
					if((I_Aulas[i][1][0] <= I_Aulas[j][1][0] and I_Aulas[i][1][1] > I_Aulas[j][1][0]) or (I_Aulas[i][1][0] < I_Aulas[j][1][1] and I_Aulas[i][1][1] >= I_Aulas[j][1][1]) or (I_Aulas[i][1][0] == I_Aulas[j][1][0] and I_Aulas[i][1][1] == I_Aulas[j][1][1])):
						Matriz_o[i][j] = 1
	
	Matriz_n = []
	Matriz_aulasDisciplinas = []
	Matriz_aulasCurriculos = 0
	Matriz_uso = []
	
	for i in range(len(I_Disciplinas)):
		Matriz_aulasDisciplinas.append([])
		for j in range(len(I_Aulas)):
			Matriz_aulasDisciplinas[i].append(0)
	
	if(I_Curriculos):
		Matriz_aulasCurriculos = []
		for i in range(len(I_Curriculos)):
			Matriz_aulasCurriculos.append([])
			for j in range(len(I_Aulas)):
				Matriz_aulasCurriculos[i].append(0)

	for i in range(len(I_Aulas)):
		Matriz_n.append([])
		Matriz_uso.append([])
	
	for i in range(len(I_Aulas)):
	
		posDis = I_Disciplinas.index(I_Aulas[i][0])
		Matriz_aulasDisciplinas[posDis][i] = 1
		
		if(I_Curriculos):
			for j in range(len(I_Curriculos)):
				if(R_CurriculosDisciplinas[j][posDis]):
					Matriz_aulasCurriculos[j][i] = 1
		
		alocavel = 0
		for j in range(len(I_Salas)):
		
			Matriz_n[i].append(0)
			Matriz_uso[i].append(0)
			
			if(C_DisciplinasTamanhos[posDis][1] > C_SalasCapacidades[j][1]):
				Matriz_n[i][j] = 1
			else:
				Matriz_uso[i][j] = C_SalasCapacidades[j][1] - C_DisciplinasTamanhos[posDis][1]
			
			if(I_Recursos):
				for k in range(len(I_Recursos)):
					if(R_DisciplinasRecursos[posDis][k] > R_SalasRecursos[j][k]):
						Matriz_n[i][j] = 1
			
			if(not Matriz_n[i][j]):
				alocavel += 1
				
		if(not alocavel):
			c = 0
			print("Erro gravíssimo: A aula de ["+I_Disciplinas[posDis]+"] das ["+minuto_paraHorario(I_Aulas[i][1], 1)+"] não pode ser ministrada em nenhuma das salas")
			
if(c):

	print("Agora estamos montando o modelo")	
	modelo = Model()
	
	print("Prepararando as variáveis de decisão")
	
	x = [[modelo.add_var(var_type=BINARY) for j in range(len(I_Salas))] for i in range(len(I_Aulas))]
	x_in_dis = [[modelo.add_var(var_type=BINARY) for j in range(len(I_Salas))] for i in range(len(I_Disciplinas))]
	
	y = [modelo.add_var(var_type=INTEGER) for i in range(len(I_Disciplinas))]
	
	if(I_Curriculos):
	
		w = [[modelo.add_var(var_type=BINARY) for j in range(len(I_Salas))] for i in range(len(I_Curriculos))]
		v = [[[modelo.add_var(var_type=BINARY) for k in range(len(I_Salas))] for j in range(len(I_Salas))] for i in range(len(I_Curriculos))]
	
	print("Preparando restrições")
	
	for i in range(len(I_Aulas)):
		
		for j in range(len(I_Salas)):
			if(Matriz_n[i][j]):
				modelo.add_constr(x[i][j] <= 0)	#3.10
		
		modelo.add_constr(xsum(x[i][j] for j in range(len(I_Salas))) == 1)	#3.9
	
	print("Duas restrições de sete prontas")
	
	for i in range(len(I_Disciplinas)):
		
		for j in range(len(I_Aulas)):
			
			if(Matriz_aulasDisciplinas[i][j]):
			
				for k in range(len(I_Salas)):
				
					modelo.add_constr(x[j][k] <= x_in_dis[i][k])	#3.12 AUX
					
		modelo.add_constr(xsum(x_in_dis[i][j] for j in range(len(I_Salas))) <= 1 + y[i])	#3.12
	
	print("Três restrições de sete prontas")
	
	for i in range(len(I_Aulas)):
		
		for j in range(len(I_Aulas)):
			if(Matriz_o[i][j]):
				for k in range(len(I_Salas)):
					modelo.add_constr(x[i][k] + x[j][k] <= 1)	#3.11
		
		if(I_Curriculos):
		
			for j in range(len(I_Curriculos)):
				for k in range(len(I_Salas)):
					if(Matriz_aulasCurriculos[j][i]):
						modelo.add_constr(x[i][k] <= w[j][k])	#3.13
	
	print("Cinco restrições de sete prontas")
	
	if(I_Curriculos):
	
		for i in range(len(I_Curriculos)):
			for j in range(len(I_Salas)):
				for k in range(len(I_Salas)):
					modelo.add_constr(2*v[i][j][k] <= w[i][j] + w[i][k])	#3.14
					modelo.add_constr(v[i][j][k] >= w[i][j] + w[i][k] - 1)	#3.15
	
	print("Preparando a função objetiva")
			
	if(I_Curriculos):
					
		modelo.objective = minimize(getValue(Constantes, "Constante desperdício salas")*(xsum(Matriz_uso[i][j]*x[i][j] for j in range(len(I_Salas)) for i in range(len(I_Aulas)))) + getValue(Constantes, "Constante trocas de sala")*(xsum(y[i] for i in range(len(I_Disciplinas)))) + getValue(Constantes, "Constante distâncias")*(xsum(R_Distancias[j][k]*v[i][j][k] for i in range(len(I_Curriculos)) for j in range(len(I_Salas)) for k in range(len(I_Salas)))) + getValue(Constantes, "Constante preferência salas")*(xsum(C_SalasPref[j][1]*x[i][j] for i in range(len(I_Aulas)) for j in range(len(I_Salas)))) + getValue(Constantes, "Constante preferência currículos")*(xsum(Rd_CurriculosSalas[i][j]*w[i][j] for i in range(len(I_Curriculos)) for j in range(len(I_Salas)))))
		
	else:
	
		modelo.objective = minimize(getValue(Constantes, "Constante desperdício salas")*(xsum(Matriz_uso[i][j]*x[i][j] for j in range(len(I_Salas)) for i in range(len(I_Aulas)))) + getValue(Constantes, "Constante trocas de sala")*(xsum(y[i] for i in range(len(I_Disciplinas)))) + getValue(Constantes, "Constante preferência salas")*(xsum(C_SalasPref[j][1]*x[i][j] for i in range(len(I_Aulas)) for j in range(len(I_Salas)))))
	
	print("Tentaremos criar o arquivo com o modelo, caso o programa feche, provavelmente seja porque não há solução ["+mainConfs_pastaSolucao+"/modelo.mps]")
	if(modelo.write(mainConfs_pastaSolucao+"/modelo.mps")):
		print("Concluímos a criação do arquivo com modelo ["+mainConfs_pastaSolucao+"/modelo.mps]")
	else:
		print("Não foi possível criar o arquivo com modelo ["+mainConfs_pastaSolucao+"/modelo.mps]")
			
	print("Tentaremos criar o arquivo com o modelo, caso o programa feche, provavelmente seja porque não há solução ["+mainConfs_pastaSolucao+"/modelo.lp]")
	if(modelo.write(mainConfs_pastaSolucao+"/modelo.lp")):
		print("Concluímos a criação do arquivo com modelo ["+mainConfs_pastaSolucao+"/modelo.lm]")
	else:
		print("Não foi possível criar o arquivo com modelo ["+mainConfs_pastaSolucao+"/modelo.lp]")
	
	modelo.max_mip_gap = 1e-1
	modelo.integer_tol = 1e-1
	modelo.emphasis = "FEASIBILITY"
	
	time_processa = time.time()
	if(time_processa - time_coleta > 60):
		print("\nDemoramos cerca de ",int((time_processa - time_coleta)/60)," minutos para processarmos os dados\n")
	else:
		print("\nDemoramos cerca de ",int(time_processa - time_coleta)," segundos para processarmos os dados\n")
	
	print("Vamos começar a resolver")
	
	#tentamos escapar os erros, mas não conseguimos todos
	try:
		print("O Python pode cancelar a execução do programa em qualquer problema, nesse caso pode ser ausência de solução (inclusive pelo tempo) ou questões de memória, entre outros - que não ao alcance de nosso software")
		if(getValue(mainConfs, "SolucoesMax") == 0):
			situacao = modelo.optimize(max_seconds = getValue(mainConfs, "TimeMax"))
		else:
			situacao = modelo.optimize(max_seconds = getValue(mainConfs, "TimeMax"), max_solutions = getValue(mainConfs, "SolucoesMax"))
	except:
		print("Não foi possível processar o problema, podem ser falta de memória, nenhuma solução ou outro motivo não reconhecido")

	print(situacao)

	if(not (situacao == OptimizationStatus.OPTIMAL or situacao == OptimizationStatus.FEASIBLE)):
	
		print("Não foi possível encontrar nenhuma solução! Tente aliviar as restrições, expandir as possibilidades e aumentar os limites de processamento =)")
		
	else:
	
		if(situacao == OptimizationStatus.OPTIMAL):
		
			print("Encontramos uma solução ótima! Estamos muito felizes =)")
			
		else:
		
			print("Encontramos uma solução sub ótima, mas ainda assim estamos felizes =)")
		
		for i in range(len(I_Aulas)):
			for j in range(len(I_Salas)):
				if(x[i][j].x):
					print("A aula de ["+I_Aulas[i][0]+"] das ["+minuto_paraHorario(I_Aulas[i][1], 1)+"] ocupará a sala ["+I_Salas[j]+"]")
					
		print("Agora vamos salvar isso no arquivo ["+mainConfs_pastaSolucao+"/solucao.txt] e ["+mainConfs_pastaSolucao+"/solucao.csv]")
	
		try:
			with io.open(mainConfs_pastaSolucao+"/solucao.txt", "w+") as arquivo:
				arquivo.write("Aulas e suas salas:\n\n")
				for i in range(len(I_Aulas)):
					linha = ""
					for j in range(len(I_Salas)):
						if(x[i][j].x):
							arquivo.write("A aula de ["+I_Aulas[i][0]+"] das ["+minuto_paraHorario(I_Aulas[i][1], 1)+"] ocupará a sala ["+I_Salas[j]+"]\n")
				print("Acabamos de criar o arquivo ["+mainConfs_pastaSolucao+"/solucao.txt]")
		except:
			print("Não foi possível criar o arquivo ["+mainConfs_pastaSolucao+"/solucao.txt]")
			
		try:
			with io.open(mainConfs_pastaSolucao+"/solucao.csv", "w+") as arquivo:
				arquivo.write("Disciplina;;Horário da aula;;Sala:\n\n")
				for i in range(len(I_Aulas)):
					for j in range(len(I_Salas)):
						if(x[i][j].x):
							arquivo.write(I_Aulas[i][0]+";;"+minuto_paraHorario(I_Aulas[i][1], 1)+";;"+I_Salas[j]+"\n")
				print("Acabamos de criar o arquivo ["+mainConfs_pastaSolucao+"/solucao.csv]")
		except:
			print("Não foi possível criar o arquivo ["+mainConfs_pastaSolucao+"/solucao.csv]")
		
		print("Estamos nos preparando para salvar as soluções expandidas por dia")
			
		mensagens = ["","","","","","",""]
		I_AulasDia = [[],[],[],[],[],[],[]]
		I_HorariosDia = [[],[],[],[],[],[],[]]
			
		for i in range(len(I_Aulas)):
			if(I_Aulas[i][1][0] < 60*24*1):
				I_AulasDia[0].append(i)
			elif(I_Aulas[i][1][0] < 60*24*2):
				I_AulasDia[1].append(i)
			elif(I_Aulas[i][1][0] < 60*24*3):
				I_AulasDia[2].append(i)
			elif(I_Aulas[i][1][0] < 60*24*4):
				I_AulasDia[3].append(i)
			elif(I_Aulas[i][1][0] < 60*24*5):
				I_AulasDia[4].append(i)
			elif(I_Aulas[i][1][0] < 60*24*6):
				I_AulasDia[5].append(i)
			else:
				I_AulasDia[6].append(i)
					
		for i in range(len(I_Horarios)):
			if(I_Horarios[i][1][0] < 60*24*1):
				I_HorariosDia[0].append(I_Horarios[i][1])
			elif(I_Horarios[i][1][0] < 60*24*2):
				I_HorariosDia[1].append(I_Horarios[i][1])
			elif(I_Horarios[i][1][0] < 60*24*3):
				I_HorariosDia[2].append(I_Horarios[i][1])
			elif(I_Horarios[i][1][0] < 60*24*4):
				I_HorariosDia[3].append(I_Horarios[i][1])
			elif(I_Horarios[i][1][0] < 60*24*5):
				I_HorariosDia[4].append(I_Horarios[i][1])
			elif(I_Horarios[i][1][0] < 60*24*6):
				I_HorariosDia[5].append(I_Horarios[i][1])
			else:
				I_HorariosDia[6].append(I_Horarios[i][1])
			
		for dia in range(0, 7):
			if(len(I_HorariosDia[dia]) > 0 and len(I_AulasDia[dia]) > 0):
					
				for i in range(len(I_HorariosDia[dia])):
					mensagens[dia] = mensagens[dia]+";"+minuto_paraHorario(I_HorariosDia[dia][i], 1)
					
				gradeSalas = []
				for i in range(len(I_Salas)):
					gradeSalas.append([])
					for j in range(len(I_HorariosDia[dia])):
						gradeSalas[-1].append("")	
					
				for i in range(len(I_AulasDia[dia])):
					for j in range(len(I_Salas)):
						if(x[I_AulasDia[dia][i]][j].x):
							gradeSalas[j][I_HorariosDia[dia].index(I_Aulas[I_AulasDia[dia][i]][1])] = I_Aulas[I_AulasDia[dia][i]][0]
					
				for i in range(len(I_Salas)):
					mensagens[dia] = mensagens[dia]+"\n"+I_Salas[i]
					for j in range(len(I_HorariosDia[dia])):
						mensagens[dia] = mensagens[dia]+";"+gradeSalas[i][j]
					
		print("Agora vamos começar a salvar as soluções expandidas por dia")
		diasExtenso = ["a segunda","a terça","a quarta","a quinta","a sexta","o sábado","o domingo"]
		for dia in range(0, 7):
			if(len(I_HorariosDia[dia]) > 0 and len(I_AulasDia[dia]) > 0):
				print("Agora vamos salvar a solução expandida d"+diasExtenso[dia]+" em ["+mainConfs_pastaSolucao+"/solucao_expandida_"+diasExtenso[dia][2:]+".csv]")
				try:
					with io.open(mainConfs_pastaSolucao+"/solucao_expandida_"+diasExtenso[dia][2:]+".csv", "w+") as arquivo:
						arquivo.write(mensagens[dia])
						print("Acabamos de criar o arquivo ["+mainConfs_pastaSolucao+"/solucao_expandida_"+diasExtenso[dia][2:]+".csv]")
				except:
					print("Não foi possível criar o arquivo ["+mainConfs_pastaSolucao+"/solucao_expandida_"+diasExtenso[dia][2:]+".csv]")
				
			else:
				print("Não há aulas n"+diasExtenso[dia]+", então não vamos criar um arquivo com a sulução expandida desse dia")
			
		print("Estamos nos preparando para salvar as soluções expandidas por sala")
		mensagensSalas = []
		for j in range(len(I_Salas)):
			mensagensSalas.append([])
			for i in range(len(I_Aulas)):
				if(x[i][j].x):
					mensagensSalas[-1].append("["+I_Aulas[i][0]+"] das ["+minuto_paraHorario(I_Aulas[i][1], 1)+"]\n")
					
		print("Agora vamos começar a salvar as soluções expandidas por dia")
		for i in range(len(I_Salas)):
			print("Tentando criar o arquivo da sala ["+I_Salas[i]+"] ["+mainConfs_pastaSolucao+"/ocupacaoSala_"+I_Salas[i]+".txt]")
			try:
				with io.open(mainConfs_pastaSolucao+"/ocupacaoSala_"+I_Salas[i]+".txt", "w+") as arquivo:
					if(len(mensagensSalas[i]) == 0):
						arquivo.write("A sala ["+I_Salas[i]+"] não será ocupada por nenhuma aula!")
					else:
						arquivo.write("A sala ["+I_Salas[i]+"] será ocupada pelas seguintes aulas:\n\n")
						for j in range(len(mensagensSalas[i])):
							arquivo.write(mensagensSalas[i][j])
				print("Acabamos de criar o arquivo da sala ["+I_Salas[i]+"] ["+mainConfs_pastaSolucao+"/ocupacaoSala_"+I_Salas[i]+".txt]")
			except:
				print("Não foi possível criar o arquivo da sala ["+I_Salas[i]+"] ["+mainConfs_pastaSolucao+"/ocupacaoSala_"+I_Salas[i]+".txt]")

time_fim = time.time()
if(time_fim - time_inicio > 60):
	print("\nDemoramos cerca de ",int((time_fim - time_inicio)/60)," minutos para finalizar o programa")
else:
	print("\nDemoramos cerca de ",int(time_fim - time_inicio)," segundos para finalizar o programa")
print("\n\nFim da execução do programa")