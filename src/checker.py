from selenium import webdriver
import date_funcs
from selenium.webdriver.common.by import By
from selenium.common import exceptions


str_data = str

def find_last_update_from_process(link: str) -> str_data:
    driver = webdriver.Chrome()
    try: driver.get(link)
    except exceptions.WebDriverException: raise exceptions.WebDriverException("Error solving link")
    try:
        ultima_fase_bloco = driver.find_element(By.ID, 'idProcessoDetalhesBloco4')
        ultima_fase_text = ultima_fase_bloco.find_element(By.CLASS_NAME, 'classSpanDetalhesTexto')
    except exceptions.NoSuchElementException: exceptions.NoSuchElementException("Element not found")
    return ultima_fase_text.text[0:10]

def check_update_from_process(link: str) -> bool:
    last_update: str_data = find_last_update_from_process(link)
    return last_update == date_funcs.get_today()

def get_last_html_from_process(link: str, numero_processo: str) -> str:
    driver = webdriver.Chrome()
    try: driver.get(link)
    except exceptions.WebDriverException: raise exceptions.WebDriverException("Error solving link")
    try:
        html ='''
            <style type="text/css"> #idDescricaoProcesso {
                        background-color: #414f55;
                        background-repeat: no-repeat;
                        border-top: 1px solid #FFFFFF;
                        color: #FFFFFF;
                        font-weight: bold;
                        padding: 1em 0.25em 1em 0.25em;
                        text-align: center;
                    }
                    body {
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                        font-size: 14px;
                        line-height: 1.42857143;
                        color: #333;
                        background-color: #fff;
                    }
                    .classSpanFaseTexto {
                        vertical-align: top;
                        font-weight: bold;
                        padding: 0 0 0 0.5em;
                        display: inline-block;
                        max-width: 70%;
                        word-wrap: break-word;
                    }
                    .classDivFaseLinha {
                        border-bottom: 1px solid;
                        text-align: left;
                        margin: 0.25em;
                        padding: 0.25em 0;
                    }

                    .classDivConteudoPesquisaProcessual {
                        background-color: #FFFFFF;
                        clear: both;
                        font-size: 1em;
                        padding: 0.5em 0;
                        text-align: justify;
                        border: none;
                        min-height: 4em;
                        overflow: hidden;
                    }
                    #idDivAbas {
                        display: block;
                        background-color: #414f55;
                        font-size: 1.1em;
                        overflow: none;
                        padding: 0 0 0 5px;
                        border-style: none;
                        margin-bottom: -1px;
                    }
            </style>

            <ul style="background-color:#f1e501;">
                <li>''' + numero_processo + '''</li>
            </ul>
            <div>
                ''' + geraHtmlDescricaoSTJ(driver) + '''
            </div>
            <div>
                ''' + geraHtmlAbasSTJ(driver) + '''
            </div>
            <div>
                ''' + geraHtmlFasesSTJ(driver, date_funcs.get_str_today()) + '''
            </div>
            '''
    except exceptions.NoSuchElementException: exceptions.NoSuchElementException("Element not found")
    return html
        
        
def geraHtmlFasesSTJ(driver: webdriver.Chrome, ultima_movimentacao: str,):
    elementos = driver.find_elements(By.CLASS_NAME, 'classDivFaseLinha')
    htmlFases1 = [
        elemento.get_attribute('outerHTML') 
        for elemento in elementos
        if 
        date_funcs.str_to_date(ultima_movimentacao) 
        <=
        date_funcs.str_to_date(
            elemento
            .find_element(By.CLASS_NAME, 'clsFaseDataHora')
            .find_element(By.CLASS_NAME, 'classSpanFaseData')
            .get_attribute('innerText')
        )
    ]
    htmlFasesDoDia = ['\n   <div style="background-color:#f1e501;">\n' + fase + '\n   </div>\n' for fase in htmlFases1]
    htmlFases = ('\n').join(htmlFasesDoDia)
    return htmlFases

def geraHtmlAbasSTJ(driver: webdriver.Chrome):
    elemento = driver.find_element(By.ID, 'idDivAbas')
    return elemento.get_attribute('outerHTML')
    
def geraHtmlDescricaoSTJ(driver: webdriver.Chrome):
    elemento = driver.find_element(By.ID, 'idDescricaoProcesso')
    return elemento.get_attribute('outerHTML')
    
with open('teste.html', 'w') as file:
    file.write(get_last_html_from_process("https://processo.stj.jus.br/processo/pesquisa/?termo=Ar+5289&aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&chkordem=DESC&chkMorto=MORTO", "AR 5289"))