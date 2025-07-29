from UHDRPCAN import UHDRPCAN
import time
import os

import sys
#rev 23-07-2025
#adição de menu pra teste de funcoes isoladas
#para o transmissor
#time.sleep(x) funcao que aguarda x segundos para passar pra proxima linha de instrução
#arquivo apenas para ESCRITA NOS REGISTRADORES

#rev 28-07-2025, teste_simples
#modificacao para executar direto alguns comandos para ler registros do TXX
# alguns poucos comandos para ESCREVER 

# tentar colocar o salvamento em arquivo.txt.

def clear_menu():
	#opcao nt para wiondows e outras pra Linux e mac
	if os.name == 'nt':
		_ = os.system('cls')
	else:
		_ = os.system('clear')




def salvar_log():
	nome_arquivo = "log_do_teste.txt"
	with open(nome_arquivo_log, 'w') as f:
		# Salvar a saída padrão original (o console)	
		stdout_original = sys.stdout
		# Redirecionar a saída padrão para o arquivo
		sys.stdout = f
		uhdrtx.get_id()
		uhdrtx.get_serial()
		uhdrtx.get_uptime()
		uhdrtx.get_uptime()
		uhdrtx.get_can0_status()
		uhdrtx.get_can0_conf()
		uhdrtx.get_mode()
		get_scratchpad()
		# Voltar a saída padrão para o console
		sys.stdout = stdout_original
	print(f"Os resultados foram salvos em '{nome_arquivo_log}'")




def teste_simples():
	clear_menu()
	uhdrtx = UHDRPCAN(channel='can0')
	print("\n#### Programa de teste para Transmissor uHDRTx  - ESCRITA ####")
	print("\USO DA FUNCAO get_id")
	uhdrtx.get_id()
	print("\USO DA FUNCAO get_serial")
	uhdrtx.get_serial()
	#uhdrtx.get_swversion()
	#uhdrtx.get_fwversion()
	print("\USO DA FUNCAO get_uptime")
	uhdrtx.get_uptime()
	#input("Aperte ENTER para continua...")
	print("\USO DA FUNCAO can0_status")
	uhdrtx.get_can0_status()
	print("\USO DA FUNCAO can0_conf")
	uhdrtx.get_can0_conf()
	#uhdrtx.get_lvds_status()
	#uhdrtx.get_status()
	#uhdrtx.get_rf_status()
	print("\USO DA FUNCAO get_mode")
	uhdrtx.get_mode()
#	input("Aperte ENTER para continua...")
    print("\USO DA FUNCAO get_scratchpad (LER)")
	get_scratchpad()
    print("\ESCREVER no scratchpad ")
	set_scratchpad(0x01020304)
	print("\LER OUTRA VEZ o scratchpad ")
	get_scratchpad()

	print("\escrevendo no LOG ...... ")
	salvar_log()





	#uhdrtx.get_temperature0()
	#uhdrtx.get_temperature1()
	#uhdrtx.get_currents()
	#uhdrtx.get_voltages()
	#uhdrtx.get_all_encoding()
	#uhdrtx.get_symbol_rate()
	#input("Aperte ENTER para continua...")
	#uhdrtx.get_data_source()
	#uhdrtx.get_chx_freq(channel=0)
	#uhdrtx.get_chx_freq(channel=1)
	#uhdrtx.get_chx_freq(channel=3)
	#uhdrtx.get_chx_freq(channel=4)
	#input("Aperte ENTER para continua...")
	#uhdrtx.get_all_pa_conf()
	#uhdrtx.get_pax_status0(pa=0)
	#uhdrtx.get_pax_status0(pa=1)
	#uhdrtx.get_pax_status1(pa=0)
	#uhdrtx.get_pax_status1(pa=1)

	input("Aperte ENTER para continua...")

def main():
	teste_simples()





















# NAO USAR OS CODIGOS ABAIXO ------------------------------------------------

def show_menu():
	clear_menu() 
	print("\n#### Programa de teste para Transmissor uHDRTx  - ESCRITA ####")
	print("\n<------------Menu principal----------------------->")
	print("\n1 - ESCREVER NO GET MODE (stby)")
	print("\n2 - ESCREVER NO GET MODE (config)")
	print("\n3 - ESCREVER NO GET MODE (transmit)")
	print("\n4 - Ajustar DADO de ENTRADA para TEST PATTERN")
	print("\n5 - Ajustar DADO de ENTRADA para LVDS")
	print("\n6 - Ajustar DADO de ENTRADA para SERDES 1")
	print("\n7 - TESTE De escrita scratchpad(0x01020304)")
	print("\n8 - Ajustar rolloff=0, pilots=0, modcod=0")
	print("\n9 - Ajustar symbol_rate=200000")
	print("\n10 - Ajustar all_pa_conf(target_dbm=27)")
	print("\n11 - Ajustar chx_freq(channel=0, freq=515")
	print("\n12 - Ajustar chx_freq(channel=1, freq=515")
	print("\n13 - Ajustar chx_freq(channel=3, freq=515")
	print("\n14 - Ajustar chx_freq(channel=4, freq=515")
	#print("\n15 - Requisitar config dos Canais do TXX")
	#print("\n16 - Requisitar config dos PA do TXX")
	#print("\n17 - Requisitar config dos PAX do TXX")
	print("\n18 - Requisitar TODAS AS INFORMAÇÕES ESCRITAS no TXX")
	print("\n20 - SAIR ---")


# NAO USAR OS CODIGOS ABAIXO ------------------------------------------------

def main_NAO_USAR():
	uhdrtx = UHDRPCAN(channel='can0')
	while True:
		time.sleep(1)
		show_menu()
		option = input("Digite sua escolha e aperte ENTER\n")
		if option == '1':
			clear_menu()
			uhdrtx.set_mode(0x00)
			input("Aperte ENTER para continua...")
		elif option == '2':
			clear_menu()
			uhdrtx.set_mode(0x01)
			input("Aperte ENTER para continua...")
		elif option == '3':
			clear_menu()
			uhdrtx.set_mode(0x02)
			input("Aperte ENTER para continua...")
		elif option == '4':
			clear_menu()
			uhdrtx.set_data_source(data_source=0x04)
			input("Aperte ENTER para continua...")
		elif option == '5':
			clear_menu()
			uhdrtx.set_data_source(data_source=0x02)
			input("Aperte ENTER para continua...")
		elif option == '6':
			clear_menu()
			uhdrtx.set_data_source(data_source=0x01)
			input("Aperte ENTER para continua...")
		elif option == '7':
			clear_menu()
			uhdrtx.set_scratchpad(0x01020304)
			input("Aperte ENTER para continua...")
		elif option == '8':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_all_encoding(rolloff=0, pilots=0, modcod=0)
			input("Aperte ENTER para continua...")
		elif option == '9':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_symbol_rate(symbol_rate=200000)
			input("Aperte ENTER para continua...")
		elif option == '10':
			print("verificar...")
			#uhdrtx.set_all_pa_conf(target_dbm=27)
			input("Aperte ENTER para continua...")
		elif option == '11':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_chx_freq(channel=0, freq=515)
			input("Aperte ENTER para continua...")
		elif option == '12':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_chx_freq(channel=1, freq=515)
			input("Aperte ENTER para continua...")
		elif option == '13':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_chx_freq(channel=3, freq=515)
			input("Aperte ENTER para continua...")
		elif option == '14':
			clear_menu()
			print("verificar...")
			#uhdrtx.set_chx_freq(channel=4, freq=515)
			input("Aperte ENTER para continua...")
		elif option == '15':
			clear_menu()
			print("vago...")
			input("Aperte ENTER para continua...")
		elif option == '16':
			clear_menu()
			print("vago...")
			input("Aperte ENTER para continua...")
		elif option == '17':
			clear_menu()
			print("vago...")
			input("Aperte ENTER para continua...")
		elif option == '18':
			clear_menu()
			list_all()
			input("Aperte ENTER para continua...")


		elif option == '20':
			print("\n saindo do programa ...")		
			break
		else:
			print("\n Escolha invalida no menu \n")





# NAO USAR OS CODIGOS ABAIXO ------------------------------------------------



#comentada, versao antiga
#if __name__ == '__main__':

def nao_usar():  
    
    uhdrtx = UHDRPCAN(channel='can0')

    uhdrtx.get_id() #id do transmissor regAddr = 0x0001
	# valor default = 0x48445478			

    uhdrtx.get_serial() #contem o serial do transmissor = 0x0002
	# valor default = 0x48445478

    uhdrtx.get_swversion()


    uhdrtx.get_fwversion()


    uhdrtx.get_hwversion()


    uhdrtx.get_uptime()
    
    uhdrtx.get_scratchpad()


    uhdrtx.set_scratchpad(0x01020304)


    uhdrtx.get_can0_status()
    uhdrtx.get_can0_conf()

    uhdrtx.get_can1_status()
    uhdrtx.get_can1_conf()

    uhdrtx.get_lvds_status()
    # uhdrtx.get_lvds_conf()

    uhdrtx.get_status()
    uhdrtx.get_rf_status()

    uhdrtx.get_temperature0()
    uhdrtx.get_temperature1()
    # uhdrtx.get_temperature_err()

    uhdrtx.get_currents()
    uhdrtx.get_voltages()

    uhdrtx.get_mode()
    # uhdrtx.set_mode(0x01)   # 0x00 standy, 0x01 config, 0x02 transmit
    uhdrtx.get_mode()

    # uhdrtx.get_channel_mode()

    uhdrtx.get_all_encoding()
    # uhdrtx.set_all_encoding(rolloff=0, pilots=0, modcod=0) # Check table 11 and table 12
    uhdrtx.get_all_encoding()

    uhdrtx.get_data_source()
    # uhdrtx.set_data_source(data_source=0x04) # Configuring the Test pattern as data source

    
    uhdrtx.get_symbol_rate()
    # uhdrtx.set_symbol_rate(symbol_rate=200000)
    uhdrtx.get_symbol_rate()

    uhdrtx.get_all_pa_conf()
    # uhdrtx.set_all_pa_conf(target_dbm=27)
    uhdrtx.get_all_pa_conf()

    uhdrtx.get_chx_freq(channel=0)
    uhdrtx.get_chx_freq(channel=1)
    uhdrtx.get_chx_freq(channel=3)
    uhdrtx.get_chx_freq(channel=4)
    # uhdrtx.set_chx_freq(channel=0, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=1, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=3, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=4, freq=515) # in MHz

    uhdrtx.get_pax_status0(pa=0) # power amplifier 0
    uhdrtx.get_pax_status0(pa=1) # power amplifier 1

    uhdrtx.get_pax_status1(pa=0) # power amplifier 0
    uhdrtx.get_pax_status1(pa=1) # power amplifier 1









# PARTE PRINCIPAL ABAIXO ------------------------------------------------
if __name__ == '__main__':
	main()
    


