from botcity.web import WebBot, Browser, By
from botcity.plugins.files import BotFilesPlugin
from botcity.plugins.ftp import BotFTPPlugin
from botcity.plugins.email import BotEmailPlugin
from anticaptchaofficial.recaptchav2enterpriseproxyless import *
from botcity.plugins.captcha import BotAntiCaptchaPlugin
from datetime import date
from datetime import datetime
import os
import shutil
from botcity.maestro import *
import emailErro
import emailSucesso
from datetime import datetime
import time

class Bot(WebBot):
    def action(self, execution=None):
         # Instanciando variável para calculo de tempo de execução (inicial)
        ini = time.time()

        # *-- Variáveis para acesso Federal CND --*
        infosArqTxt = execution.parameters["dados"]
        # infosArqTxt = "BotMunCndUbajara|teste.txt|42|12774042000169|10.1.4.230|COD_EMPRESA|carolina.mathiello@tscti.com.br|1255"
        arrayInfosArqTxt = infosArqTxt.split("|")
        nomeBot = arrayInfosArqTxt[0]
        nomeArquivoTxt = arrayInfosArqTxt[1]
        idBot = arrayInfosArqTxt[2]
        cnpj = arrayInfosArqTxt[3]
        servidor = arrayInfosArqTxt[4]
        codEmpresa = arrayInfosArqTxt[5]
        emailDestinado = arrayInfosArqTxt[6]
        inscri_mun = arrayInfosArqTxt[7]

        cnpjFormatado = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'

        # Instanciando variáveis de erro
        codErro = 0
        elemento = ''

        # Descrição do bot
        descBot = "Bot de extração CND municipal de Ubajara"

        # Variável para restartar a tarefa novamente
        qtdExecucoes = 1
        if len(arrayInfosArqTxt) > 8:
            qtdExecucoes = int(arrayInfosArqTxt[-1])
        print(qtdExecucoes)

        # *-- Variáveis para acesso do FTP --*
        hostname = servidor
        username = "tmbot"
        password = "tmbot2016"
        ftp = BotFTPPlugin(hostname, username, password)
        
        # *-- Variáveis de formatação de data e hora --*
        data = date.today()
        if(data.day < 10):
            dia = f'0{data.day}'
        else:
            dia = data.day

        if(data.month < 10):
            mes = f'0{data.month}'
        else:
            mes = data.month

        ano = data.year

        if (datetime.now().hour < 10):
            hora = f'0{datetime.now().hour}'
        else:
            hora = datetime.now().hour

        if (datetime.now().minute < 10):
            minuto = f'0{datetime.now().minute}'
        else:
            minuto = datetime.now().minute

        if (datetime.now().second < 10):
            segundo = f'0{datetime.now().second}'
        else:
            segundo = datetime.now().second

        dataHora = f'{dia}/{mes}/{ano} &nbsp;&nbsp; {hora}:{minuto}:{segundo}'
        
        # F6etch the Activity ID from the task:
        task = self.maestro.get_task(execution.task_id)
        activity_id = task.activity_id

        # *-- Criação da pasta --*
        nomePastaZip = f'{idBot}_MUN_CND_{cnpj}_{ano}{mes}{dia}.zip'

        # *-- Funções --*
        def moveErro(nomeArquivo):
            try:
                shutil.move(
                    f'C:\TaxBots\Exec\{nomeArquivo}', 'C:\TaxBots\Erro')
            except:
                try:
                    os.remove(f'C:\TaxBots\Erro\{nomeArquivo}')
                    shutil.move(f'C:\TaxBots\Exec\{nomeArquivo}', 'C:\TaxBots\Erro')
                except:
                    print("Ocorreu um erro ao mover o arquivo para a pasta Erro.")

        def moveSucesso(nomeArquivo):
            try:
                shutil.move(f'C:\TaxBots\Exec\{nomeArquivo}', 'C:\TaxBots\Old')
            except:
                try:
                    os.remove(f'C:\TaxBots\Old\{nomeArquivo}')
                    shutil.move(f'C:\TaxBots\Exec\{nomeArquivo}', 'C:\TaxBots\Old')
                except:
                    print("Ocorreu um erro ao mover o arquivo para a pasta Old.")

        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = r"C:\WebDriver\chromedriver.exe"
        
        # Configurando envio de email
        email = BotEmailPlugin()
        # email.configure_imap("email-ssl.com.br", 993)
        email.configure_smtp("smtp.tscti.com.br", 587)
        email.login("naoresponda@tscti.com.br", "nao@responda1")

        if not ';' in emailDestinado:
            to = [emailDestinado, "erro_processo@tscti.com.br"]
        else:
            emailDestinado = emailDestinado.split(";")
            emailDestinado.append("erro_processo@tscti.com.br")
            to = emailDestinado
        
        try:
            # abrir site da prefeitura.
            self.browse("http://servicos2.speedgov.com.br/ubajara/pages/certidao_economico")

            
            input_inscr = self.find_element("#dados_inscricao" , By.CSS_SELECTOR)
            if not input_inscr: 
                codErro = 100
                elemento = "input_inscr"
            input_inscr.click()   
            self.paste(inscri_mun)
            self.tab()
            self.paste(cnpj)

        

            solver = recaptchaV2EnterpriseProxyless()
            solver.set_verbose(1)
            captcha = BotAntiCaptchaPlugin("5ab3a6859fe1ee638bf99d707f5972a4")
            token = captcha.solve_re("http://servicos2.speedgov.com.br/ubajara/pages/certidao_economico", "6LcD_dYUAAAAAPg9_NAytSHHu-eQXdRw6hiAF1Cl")
            if token != 0:
                print(token)
            
                self.wait(2000)
                self.execute_javascript(f"document.getElementById('g-recaptcha-response').innerHTML = '{token}'")
            else:
                print(solver.err_string)
            
            self.wait(2000)
            
            input_button = self.find_element("#gerar_certidao_inscricao_e_doc" , By.CSS_SELECTOR)
            if not input_button:
                codErro = 100
                elemento = "input_button"
            input_button.click()

            self.wait(2000)

            a_imprimir = self.find_element('//*[@id="content"]/div/div[2]/div[2]/table/tbody/tr/td[6]/a', By.XPATH)
            if not a_imprimir:
                codErro = 100
                elemento = "a_imprimir"
                mensagem_de_erro = self.find_element("#content > div > div.panel-body > p:nth-child(2) > span" , By.CSS_SELECTOR)
                if mensagem_de_erro: 
                    codErro = 800
                    print(emailErro.mensagemErroMaestro(codErro,'test'))
                    raise Exception()
            
            a_imprimir.click()
            input()

            pdf = self.wait_for_new_file(path=None, file_extension='.pdf', current_count=0, timeout=60000)
            if not pdf:
                codErro = 300
                raise Exception()

            print(pdf)
            # Instanciando variáve
            # l para calculo de tempo de execução (final)
            fim = time.time()
            segundosTempExec = fim-ini
            if segundosTempExec > 60:
                minutos = round(segundosTempExec / 60, 0)
                segundos = segundosTempExec % 60
                tempExec = f'{int(minutos)}min {int(segundos)}seg'
            else:
                tempExec = f'{round(segundosTempExec, 2)} seg'
        
        except Exception as erro:
            print(f"Except: {erro}")
            # Bloco de código caso ocorra algum erro
            # Formatando mensagem de erro para o Maestro
            mensagemMaestro = emailErro.mensagemErroMaestro(codErro, elemento)

            # Bloco de código caso for para ir criando novas tarefas
            if codErro == 0 or codErro == 100 or codErro == 300 or codErro == 400 or codErro == 500 or codErro == 600 :
                print(f"\n\tCaiu no else do except, codErro: {codErro}\n")

                # Verifica a quantidade de vezes que o bot foi rodado
                if qtdExecucoes > 0 and qtdExecucoes < 4:
                    # Finalizando tarefa parcialmente finalizado
                    self.maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.PARTIALLY_COMPLETED,
                        message=mensagemMaestro
                    )

                    # Enviando email de erro para o cliente
                    subject = f"ERRO ({idBot}) - {descBot}."
                    body = emailErro.htmlEmailErro(descBot, codErro, dataHora, idBot, qtdExecucoes, cnpjFormatado, codEmpresa)
                    email.send_message(subject, body, to, use_html=True)

                    # Adiciona mais 1 a quantidade de execuções do bot
                    qtdExecucoes += 1
                    infosArqTxt += f'|{qtdExecucoes}'

                    print(f'\n\tInfosArqTxt: {infosArqTxt}\n')
                    param = {'dados': infosArqTxt}
                    # Criando nova tarefa com os mesmos parametros
                    self.maestro.create_task(
                        activity_label=nomeBot,
                        parameters=param,
                        test=True
                    )
                else:
                    # Caso a quantidade de execuções for 4, apenas irá finalizar com erro

                    # Enviando email de erro para o cliente
                    subject = f"ERRO ({idBot}) - {descBot}."
                    body = emailErro.htmlEmailErro(descBot, codErro, dataHora, idBot, qtdExecucoes, cnpjFormatado, codEmpresa)
                    email.send_message(subject, body, to, use_html=True)

                    # Finalizando tarefa parcialmente finalizado
                    self.maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.FAILED,
                        message=mensagemMaestro
                    )

                    # Movendo para a pasta de Erro
                    moveErro(nomeArquivoTxt)
            else:
                statusEmail = 'ERRO'
                if codErro == 800:
                    statusEmail = 'ALERTA'

                # Caso seja um erro que não é para reinicar as tarefas, apenas irá finalizar
                subject = f"{statusEmail} ({idBot}) - {descBot}."
                body = emailErro.htmlEmailErro(descBot, codErro, dataHora, idBot, 0, cnpjFormatado, codEmpresa)
                email.send_message(subject, body, to, use_html=True)

                if codErro != 800:
                    # Finalizando tarefa parcialmente finalizado
                    self.maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.FAILED,
                        message=mensagemMaestro
                    )

                    # Movendo para a pasta de Erro
                    moveErro(nomeArquivoTxt)
                else:
                    # Finalizando tarefa parcialmente finalizado
                    self.maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.SUCCESS,
                        message=mensagemMaestro
                    )

                    # Movendo arquivo para a pasta Old
                    moveSucesso(nomeArquivoTxt)
        else:
            # Bloo de código caso não ocorra nenhum erro

            # Zipando arquivo
            files = BotFilesPlugin()
            file_path = [pdf]
            files.zip_files(file_path, nomePastaZip)

            # Enviando arquivo
            ftp.upload_file(nomePastaZip)

            # Enviando email de sucesso para o cliente
            subject = f"SUCESSO ({idBot}) - {descBot}."
            body = emailSucesso.htmlEmailSucesso(descBot, tempExec, dataHora, idBot, cnpjFormatado, codEmpresa)
            files = [nomePastaZip]
            email.send_message(subject, body, to,attachments=files, use_html=True)

            # Removendo arquivos da execução
            os.remove(nomePastaZip)
            os.remove(pdf)

            # Finalizando tarefa com sucesso
            self.maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Arquivo enviado ao TM com sucesso."
            )

            # Movendo arquivo para a pasta Old
            moveSucesso(nomeArquivoTxt)
        finally:
            # Bloco de código que independentemente irá ser executado
            self.wait(2000)
            self.stop_browser()
            ftp.disconnect()

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()
