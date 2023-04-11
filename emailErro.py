def mensagemErroMaestro(codErro, elemento):
    mensagem = ''
    if codErro == 100:
        mensagem = f'Elemento não encontrado: {elemento}.'
    elif codErro == 200:
        mensagem = 'Quantidade de caracteres do CNPJ incoreta, tem que ser igual a 14.'
    elif codErro == 300:
        mensagem = 'Erro ao baixar o arquivo do site.'
    elif codErro == 400:
        mensagem = 'Erro de FTP.'
    elif codErro == 500:
        mensagem = 'Bot de ecac rodado fora de hora.'
    elif codErro == 600:
        mensagem = 'Erro de captcha.'
    elif codErro == 700:
        mensagem = 'Contribuinte não cadastrado ou dados não conferem.'
    elif codErro == 800:
        mensagem = 'Empresa com pendências.'
    else:
        mensagem = 'Erro inesperado.'

    return mensagem


def possiveisCausas(codErro):
    mensagem = ''
    if codErro == 100:
        mensagem = '<li style="font-size: 1.3em;">Recente atualização no site.</li>'
        mensagem += '<li style="font-size: 1.3em;">Site fora do ar.</li>'
        mensagem += '<li style="font-size: 1.3em;">Site não está sendo carregado corretamente.</li>'
    elif codErro == 200:
        mensagem = '<li style="font-size: 1.3em;">Quantidade de caracteres do CNPJ incoreta, tem que ser igual a 14.</li>'
        mensagem += '<li style="font-size: 1.3em;">CPNJ deve ser preenchido apenas com números.</li>'
        mensagem += '<li style="font-size: 1.3em;">O parâmetro de CNPJ não pode ser vazio ao preencher no TM.</li>'
    elif codErro == 300:
        mensagem = '<li style="font-size: 1.3em;">Erro ao baixar o arquivo do site.</li>'
    elif codErro == 400:
        mensagem = '<li style="font-size: 1.3em;">Erro do bot ao se conectar com o sistema.</li>'
    elif codErro == 500:
        mensagem = '<li style="font-size: 1.3em;">Erro de horário da execução do bot no site da Ecac, os bots apenas rodam depois das 18:00 e antes das 08:00.</li>'
    elif codErro == 600:
        mensagem = '<li style="font-size: 1.3em;">Erro ao resolver o Captcha (não sou um robo).</li>'
    elif codErro == 700:
        mensagem = '<li style="font-size: 1.3em;">Contribuinte não cadastrado ou dados não conferem.</li>'
    elif codErro == 800:
        mensagem = f'<p style="font-size: 1.3em;">ATENÇÃO: EXISTEM PENDÊNCIAS NO RELATÓRIO SITUACIONAL!</br>DIRIJA-SE AO SETOR DE ISS NA PREFEITURA!</br>Nenhuma certidão emitida e válida até o momento para os dados informado.</p>'
    else:
        mensagem = '<li style="font-size: 1.3em;">Erro inesperado.</li>'

    return mensagem


def htmlEmailErro(descBot, codErro, dataHoraExec, idExec, qtdExecucoes, cnpj, codEmpresa):
    html = '<body style="margin: 0; margin: 0; box-sizing: border-box;">'
    html += '<table width="100%" align="center" cellpadding="0" cellspacing="0" style="max-width: 750px; margin: 0 auto;">'
    html += '<tr>'
    html += '<td style="padding: 20px 0 20px 0;background-color: #ccc;" bgcolor="#ccc" align="center">'
    html += '<img src = "https://www.tscti.com.br/wp-content/uploads/2019/03/Logo-TSCTI-300x104.png" alt = "" >'
    html += '</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td style="padding: 20px;" bgcolor="#fff">'
    if codErro == 800:
        html += f'<p style="font-size: 1.5em; font-weight: bold;">Olá, informamos que o seu {descBot} retornou com <span style="color: orange;">um alerta</span>! <br /> Segue algumas informações sobre a execução:</p>'
    else:
        html += f'<p style="font-size: 1.5em; font-weight: bold;">Olá, informamos que o seu {descBot} retornou com <span style="color: red;">erro</span>! <br /> Segue algumas informações sobre a execução:</p>'
    html += '</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td style="padding: 20px;">'
    html += '<table width="100%" align="center" cellpadding="0" cellspacing="0" bgcolor="white" style="max-width: 750px;  margin: 0 auto;">'
    html += '<tr>'
    html += '<td>Data e Hora:</td>'
    html += f'<td align="right" style="padding-bottom: 15px; ">{dataHoraExec}</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td>Código da execução:</td>'
    html += f'<td align="right" style="padding-bottom: 20px; ">{idExec}</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td>CNPJ:</td>'
    html += f'<td align="right" style="padding-bottom: 20px; ">{cnpj}</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td>Código da empresa:</td>'
    html += f'<td align="right" style="padding-bottom: 20px; ">{codEmpresa}</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td>'
    if codErro == 800:
        html += '<h3 style="font-weight: bold; font-size: 1.5em;">Mensagem do alerta do site de extração:</h3>'
        html += '<div>'
        html += f'{possiveisCausas(codErro)}'
        html += '</div>'
    else:
        html += '<h3 style="font-weight: bold; font-size: 1.5em;">Possível(eis) causa(s):</h3>'
        html += '<ul>'
        html += f'{possiveisCausas(codErro)}'
        html += '</ul>'
    html += '</td>'
    html += '</tr>'
    html += '</table>'
    html += '</td>'
    html += '</tr>'

    if codErro == 0 or codErro == 100 or codErro == 300 or codErro == 400 or codErro == 500 or codErro == 600:
        if qtdExecucoes >= 0 and qtdExecucoes < 4:
            html += '<tr>'
            html += '<td style="width: 100%;">'
            html += '<h3 style="font-weight: bold; font-size: 1.3em;text-align: center;">A tarefa será executada novamente em breve.</h3>'
            html += f'<h4 style="font-weight: bold; font-size: 1.2em;text-align: center;">Ela já foi executada {qtdExecucoes} vez(es).</h4>'
            html += '</td>'
            html += '</tr>'
        elif qtdExecucoes == 4:
            html += '<tr>'
            html += '<td style="width: 100%;">'
            html += '<h3 style="font-weight: bold; font-size: 1.3em;text-align: center;">A tarefa já foi executada 4 vezez, iremos verificar o ocorrido.'
            html += '</td>'
            html += '</tr>'

    html += '<tr>'
    html += '<table width = "100%" align = "center" bgcolor = "#ccc" cellpadding = "0" cellspacing = "0" style = "max-width: 750px;  margin: 0 auto;background-color: #ccc;" >'
    html += '<tr>'
    html += '<td  style="padding: 20px;">'
    html += '<img src="https://www.tscti.com.br/wp-content/uploads/2019/03/Logo-TSCTI-300x104.png" alt="">'
    html += '</td>'
    html += '<td>'
    html += '<h2 style="text-align: center; color: black; font-size: 1.2em; font-weight: bold;">Tecnologia | RPA | IA</h2>'
    html += '<p>(11) 3729-7237 | 9.9735-2852</p>'
    html += '<p>Rua Geraldo Campos Moreira, 164, 1º andar <br /> 04571-020 - São Paulo - SP</p>'
    html += '<p><a href="http://www.tscti.com.br/" target="_blank">www.tscti.com.br</a></p>'
    html += '</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td  style="padding: 0 0 20px 0;" align="center" colspan="2">'
    html += '<a href="https://cloudmarketplace.oracle.com/marketplace/pt_BR/listing/72612373" target="_blank">'
    html += '<img width="100px" style="width: 100px" src="https://www.tscti.com.br/wp-content/uploads/2018/01/Oracle-logo.png" alt="">'
    html += '</a>'
    html += '</td>'
    html += '</tr>'
    html += '</table>'
    html += '</tr>'
    html += '</table>'
    html += '</body>'

    return html